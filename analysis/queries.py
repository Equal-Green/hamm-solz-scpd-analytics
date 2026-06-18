"""All analytics as named functions returning pandas DataFrames (small,
aggregated result sets) or plain dicts. Every heavy computation is a DuckDB
SQL aggregation over the local file -- no pandas parsing, no row-by-row Python.

Weights are stored in kilograms; tonnage helpers divide by 1000.
"""

# --- filter option helpers ---------------------------------------------------
def years(con):
    return [r[0] for r in con.execute(
        "SELECT DISTINCT source_year FROM transactions ORDER BY 1").fetchall()]


def services(con):
    return [r[0] for r in con.execute(
        "SELECT DISTINCT tipo_servicio FROM transactions "
        "WHERE tipo_servicio IS NOT NULL ORDER BY 1").fetchall()]


def _year_clause(year):
    return ("", []) if not year else (" AND source_year = ?", [year])


def _service_clause(servicio):
    return ("", []) if not servicio else (" AND tipo_servicio = ?", [servicio])


# --- overview ----------------------------------------------------------------
def kpis(con):
    row = con.execute("""
        SELECT count(*) AS trips,
               sum(peso_neto)/1000.0 AS tonnes,
               avg(peso_neto) AS avg_kg,
               min(fec_ingreso) AS first_dt,
               max(fec_ingreso) AS last_dt
        FROM transactions
    """).fetchone()
    return {
        "trips": row[0] or 0,
        "tonnes": row[1] or 0.0,
        "avg_kg": row[2] or 0.0,
        "first_dt": row[3],
        "last_dt": row[4],
    }


def monthly_trips(con):
    """Trips per calendar month, one column per year -- for an overlaid line."""
    return con.execute("""
        SELECT mes, source_year, count(*) AS trips
        FROM transactions
        WHERE mes IS NOT NULL
        GROUP BY 1, 2
        ORDER BY 1, 2
    """).df()


def annual_tonnage(con):
    return con.execute("""
        SELECT source_year AS year, sum(peso_neto)/1000.0 AS tonnes
        FROM transactions GROUP BY 1 ORDER BY 1
    """).df()


def monthly_tonnage_by_service(con, year=None):
    yc, yp = _year_clause(year)
    return con.execute(f"""
        SELECT mes, tipo_servicio, sum(peso_neto)/1000.0 AS tonnes
        FROM transactions
        WHERE mes IS NOT NULL AND tipo_servicio IS NOT NULL {yc}
        GROUP BY 1, 2 ORDER BY 1, 2
    """, yp).df()


# --- service types -----------------------------------------------------------
def service_summary(con, year=None):
    yc, yp = _year_clause(year)
    return con.execute(f"""
        SELECT tipo_servicio,
               count(*) AS trips,
               sum(peso_neto)/1000.0 AS tonnes,
               avg(peso_neto) AS avg_kg
        FROM transactions
        WHERE tipo_servicio IS NOT NULL {yc}
        GROUP BY 1 ORDER BY trips DESC
    """, yp).df()


def service_yoy(con):
    """Trips per service per year, pivoted, with YoY % change columns."""
    df = con.execute("""
        SELECT tipo_servicio, source_year, count(*) AS trips
        FROM transactions WHERE tipo_servicio IS NOT NULL
        GROUP BY 1, 2
    """).df()
    pivot = df.pivot(index="tipo_servicio", columns="source_year",
                     values="trips").fillna(0).astype(int)
    cols = sorted(pivot.columns)
    for i in range(1, len(cols)):
        prev, cur = cols[i - 1], cols[i]
        pivot[f"{prev}->{cur} %"] = (
            (pivot[cur] - pivot[prev]) / pivot[prev].replace(0, float("nan")) * 100
        ).round(1)
    return pivot.reset_index()


def servicios_especial_anomaly(con):
    """Return the 2023->2024 trip spike for SERVICIOS ESPECIAL, computed live."""
    rows = dict(con.execute("""
        SELECT source_year, count(*)
        FROM transactions
        WHERE upper(tipo_servicio) LIKE 'SERVICIOS ESPECIAL%'
        GROUP BY 1
    """).fetchall())
    t23, t24 = rows.get(2023), rows.get(2024)
    pct = round((t24 - t23) / t23 * 100, 1) if t23 and t24 else None
    return {"y2023": t23, "y2024": t24, "pct": pct, "by_year": rows}


# --- operators & fleet -------------------------------------------------------
def top_empresas(con, year=None, servicio=None, n=10):
    yc, yp = _year_clause(year)
    sc, sp = _service_clause(servicio)
    return con.execute(f"""
        SELECT empresa,
               count(*) AS trips,
               sum(peso_neto)/1000.0 AS tonnes,
               avg(peso_neto) AS avg_kg
        FROM transactions
        WHERE empresa IS NOT NULL {yc} {sc}
        GROUP BY 1 ORDER BY trips DESC LIMIT {int(n)}
    """, yp + sp).df()


def vehicle_distribution(con, year=None, servicio=None):
    yc, yp = _year_clause(year)
    sc, sp = _service_clause(servicio)
    return con.execute(f"""
        SELECT tipo_vehiculo, count(*) AS trips
        FROM transactions
        WHERE tipo_vehiculo IS NOT NULL {yc} {sc}
        GROUP BY 1 ORDER BY trips DESC
    """, yp + sp).df()


# --- geocycle recovery -------------------------------------------------------
def retirados_monthly(con):
    return con.execute("""
        SELECT date_trunc('month', fec_ingreso) AS month,
               sum(peso_neto)/1000.0 AS tonnes,
               count(*) AS trips
        FROM retirados
        WHERE fec_ingreso IS NOT NULL
        GROUP BY 1 ORDER BY 1
    """).df()


def recovery_vs_landfill(con):
    """Annual recovered tonnage (GEOCYCLE) vs landfilled tonnage, with ratio."""
    return con.execute("""
        WITH lf AS (
            SELECT source_year AS year, sum(peso_neto)/1000.0 AS landfill_t
            FROM transactions GROUP BY 1
        ),
        rc AS (
            SELECT year(fec_ingreso) AS year, sum(peso_neto)/1000.0 AS recovery_t
            FROM retirados WHERE fec_ingreso IS NOT NULL GROUP BY 1
        )
        SELECT lf.year,
               lf.landfill_t,
               COALESCE(rc.recovery_t, 0) AS recovery_t,
               COALESCE(rc.recovery_t, 0) / lf.landfill_t * 100 AS recovery_pct
        FROM lf LEFT JOIN rc USING (year)
        ORDER BY lf.year
    """).df()


def retirados_kpis(con):
    row = con.execute("""
        SELECT count(*), sum(peso_neto)/1000.0, count(DISTINCT organizacion),
               min(fec_ingreso), max(fec_ingreso)
        FROM retirados
    """).fetchone()
    return {"trips": row[0] or 0, "tonnes": row[1] or 0.0,
            "orgs": row[2] or 0, "first_dt": row[3], "last_dt": row[4]}


# --- data quality ------------------------------------------------------------
def quality_report(con):
    from config import FILES
    out = {"files": [], "transactions": {}, "retirados": {}}

    logged = dict(con.execute(
        "SELECT source_file, rows_loaded FROM pipeline_log").fetchall())
    for spec in FILES:
        out["files"].append({
            "file": spec["match"],
            "loaded": logged.get(spec["match"], 0),
            "spec_rows": spec["spec_rows"],
            "match": logged.get(spec["match"], 0) == spec["spec_rows"],
        })

    t = con.execute("""
        SELECT count(*) total,
               sum(CASE WHEN peso_neto = 0 THEN 1 ELSE 0 END) zero_net,
               sum(CASE WHEN peso_neto < 0 THEN 1 ELSE 0 END) neg_net,
               sum(CASE WHEN num_ticket IS NULL THEN 1 ELSE 0 END) null_ticket,
               sum(CASE WHEN tipo_servicio IS NULL THEN 1 ELSE 0 END) null_servicio,
               sum(CASE WHEN empresa IS NULL THEN 1 ELSE 0 END) null_empresa,
               sum(CASE WHEN sector IS NULL THEN 1 ELSE 0 END) null_sector,
               sum(CASE WHEN fec_ingreso IS NULL THEN 1 ELSE 0 END) null_fecha,
               sum(CASE WHEN peso_neto IS NULL THEN 1 ELSE 0 END) null_neto
        FROM transactions
    """).fetchone()
    cols = ["total", "zero_net", "neg_net", "null_ticket", "null_servicio",
            "null_empresa", "null_sector", "null_fecha", "null_neto"]
    out["transactions"] = dict(zip(cols, t))

    dupes = con.execute("""
        SELECT count(*) FROM (
            SELECT num_ticket, source_year FROM transactions
            GROUP BY 1, 2 HAVING count(*) > 1
        )
    """).fetchone()[0]
    out["transactions"]["dup_ticket_year"] = dupes

    out["date_range_by_year"] = con.execute("""
        SELECT source_year AS year, min(fec_ingreso) AS first_dt,
               max(fec_ingreso) AS last_dt, count(*) AS rows
        FROM transactions GROUP BY 1 ORDER BY 1
    """).df()

    r = con.execute("""
        SELECT count(*) total,
               sum(CASE WHEN peso_neto <= 0 THEN 1 ELSE 0 END) nonpos_net,
               sum(CASE WHEN fec_ingreso IS NULL THEN 1 ELSE 0 END) null_fecha,
               sum(CASE WHEN organizacion IS NULL THEN 1 ELSE 0 END) null_org
        FROM retirados
    """).fetchone()
    out["retirados"] = dict(zip(["total", "nonpos_net", "null_fecha", "null_org"], r))
    return out


# --- pipeline status ---------------------------------------------------------
def pipeline_status(con):
    return con.execute("""
        SELECT source_file, rows_loaded, loaded_at
        FROM pipeline_log ORDER BY source_file
    """).df()


# --- geo & routes ------------------------------------------------------------
def has_routes(con):
    row = con.execute(
        "SELECT count(*) FROM transactions WHERE zona IS NOT NULL").fetchone()
    return (row[0] or 0) > 0


def route_kpis(con):
    row = con.execute("""
        SELECT count(DISTINCT zona), count(DISTINCT sub_zona),
               count(DISTINCT micro_ruta),
               count(*) FILTER (WHERE micro_ruta IS NOT NULL) * 1.0 / count(*)
        FROM transactions
    """).fetchone()
    return {"zonas": row[0] or 0, "sub_zonas": row[1] or 0,
            "micro_rutas": row[2] or 0, "route_coverage": (row[3] or 0) * 100}


def by_zona(con, year=None):
    yc, yp = _year_clause(year)
    return con.execute(f"""
        SELECT zona, count(*) AS trips, sum(peso_neto)/1000.0 AS tonnes
        FROM transactions WHERE zona IS NOT NULL {yc}
        GROUP BY 1 ORDER BY tonnes DESC
    """, yp).df()


def zona_subzona_tonnage(con, year=None):
    """Hierarchical zona → sub_zona tonnage (for treemap/sunburst)."""
    yc, yp = _year_clause(year)
    return con.execute(f"""
        SELECT zona, sub_zona, sum(peso_neto)/1000.0 AS tonnes, count(*) AS trips
        FROM transactions
        WHERE zona IS NOT NULL AND sub_zona IS NOT NULL {yc}
        GROUP BY 1, 2 ORDER BY tonnes DESC
    """, yp).df()


def top_subzonas(con, year=None, n=15):
    yc, yp = _year_clause(year)
    return con.execute(f"""
        SELECT sub_zona, zona, count(*) AS trips, sum(peso_neto)/1000.0 AS tonnes
        FROM transactions WHERE sub_zona IS NOT NULL {yc}
        GROUP BY 1, 2 ORDER BY tonnes DESC LIMIT {int(n)}
    """, yp).df()


def top_micro_routes(con, year=None, n=15):
    yc, yp = _year_clause(year)
    return con.execute(f"""
        SELECT micro_ruta, any_value(zona) AS zona, any_value(sub_zona) AS sub_zona,
               count(*) AS trips, sum(peso_neto)/1000.0 AS tonnes,
               avg(peso_neto) AS avg_kg
        FROM transactions WHERE micro_ruta IS NOT NULL {yc}
        GROUP BY 1 ORDER BY trips DESC LIMIT {int(n)}
    """, yp).df()


def subzona_geo(con, year=None):
    """Per sub-zone trips/tonnage (all sub-zones) for the choropleth."""
    yc, yp = _year_clause(year)
    return con.execute(f"""
        SELECT sub_zona, count(*) AS trips, sum(peso_neto)/1000.0 AS tonnes,
               avg(peso_neto) AS avg_kg
        FROM transactions WHERE sub_zona IS NOT NULL {yc}
        GROUP BY 1
    """, yp).df()


def subzona_month_heatmap(con, year=None):
    yc, yp = _year_clause(year)
    return con.execute(f"""
        SELECT sub_zona, mes, sum(peso_neto)/1000.0 AS tonnes
        FROM transactions
        WHERE sub_zona IS NOT NULL AND mes IS NOT NULL {yc}
        GROUP BY 1, 2
    """, yp).df()


# --- forecast / capacity -----------------------------------------------------
def monthly_tonnage_series(con):
    return con.execute("""
        SELECT date_trunc('month', fec_ingreso) AS month,
               sum(peso_neto)/1000.0 AS tonnes
        FROM transactions
        WHERE fec_ingreso IS NOT NULL
        GROUP BY 1 ORDER BY 1
    """).df()


# --- operational efficiency --------------------------------------------------
def hour_dow_matrix(con, year=None):
    yc, yp = _year_clause(year)
    return con.execute(f"""
        SELECT dayofweek(fec_ingreso) AS dow, hour(fec_ingreso) AS hr,
               count(*) AS trips
        FROM transactions WHERE fec_ingreso IS NOT NULL {yc}
        GROUP BY 1, 2
    """, yp).df()


def payload_by_vehicle(con, year=None, n=12):
    yc, yp = _year_clause(year)
    return con.execute(f"""
        SELECT tipo_vehiculo,
               count(*) AS trips,
               avg(peso_neto) AS avg_kg,
               median(peso_neto) AS median_kg,
               quantile_cont(peso_neto, 0.9) AS p90_kg
        FROM transactions WHERE tipo_vehiculo IS NOT NULL {yc}
        GROUP BY 1 ORDER BY trips DESC LIMIT {int(n)}
    """, yp).df()


def underloaded(con, threshold_kg, year=None):
    yc, yp = _year_clause(year)
    row = con.execute(f"""
        SELECT count(*) FILTER (WHERE peso_neto < ?) AS under,
               count(*) AS total,
               sum(peso_neto) FILTER (WHERE peso_neto < ?)/1000.0 AS under_t
        FROM transactions WHERE peso_neto IS NOT NULL {yc}
    """, [threshold_kg, threshold_kg] + yp).fetchone()
    return {"under": row[0] or 0, "total": row[1] or 0, "under_tonnes": row[2] or 0.0}


def payload_histogram(con, year=None):
    yc, yp = _year_clause(year)
    return con.execute(f"""
        SELECT (peso_neto // 2000) * 2 AS bin_t, count(*) AS trips
        FROM transactions WHERE peso_neto IS NOT NULL AND peso_neto > 0 {yc}
        GROUP BY 1 ORDER BY 1
    """, yp).df()


# --- revenue assurance / integrity ------------------------------------------
def especial_growth_by_empresa(con):
    return con.execute("""
        WITH e AS (
            SELECT empresa, source_year, count(*) AS trips
            FROM transactions
            WHERE upper(tipo_servicio) LIKE 'SERVICIOS ESPECIAL%'
            GROUP BY 1, 2
        )
        SELECT empresa,
               sum(trips) FILTER (WHERE source_year = 2023) AS y2023,
               sum(trips) FILTER (WHERE source_year = 2024) AS y2024,
               sum(trips) FILTER (WHERE source_year = 2024)
                 - sum(trips) FILTER (WHERE source_year = 2023) AS delta
        FROM e GROUP BY 1
        ORDER BY delta DESC NULLS LAST LIMIT 12
    """).df()


def duplicate_weighings(con):
    """Same plate, same calendar day, identical net weight — likely a
    double-weigh / re-print rather than two real trips."""
    row = con.execute("""
        SELECT count(*) FROM (
            SELECT placa, fec_ingreso::DATE AS d, peso_neto, count(*) c
            FROM transactions
            WHERE placa IS NOT NULL AND peso_neto IS NOT NULL
            GROUP BY 1, 2, 3 HAVING count(*) > 1
        )
    """).fetchone()[0]
    sample = con.execute("""
        SELECT placa, fec_ingreso::DATE AS dia, peso_neto, count(*) AS repeats
        FROM transactions
        WHERE placa IS NOT NULL AND peso_neto IS NOT NULL
        GROUP BY 1, 2, 3 HAVING count(*) > 1
        ORDER BY repeats DESC LIMIT 15
    """).df()
    return {"groups": row, "sample": sample}


def integrity_flags(con):
    row = con.execute("""
        SELECT
          count(*) AS total,
          count(*) FILTER (WHERE peso_salida > peso_ingreso) AS tare_gt_gross,
          count(*) FILTER (WHERE peso_neto > 45000) AS payload_outlier,
          count(*) FILTER (WHERE peso_neto = 0) AS zero_net,
          count(*) FILTER (WHERE peso_ingreso IS NULL OR peso_salida IS NULL) AS missing_weight
        FROM transactions
    """).fetchone()
    return dict(zip(
        ["total", "tare_gt_gross", "payload_outlier", "zero_net", "missing_weight"],
        row))


# --- data catalog (full INFORMACIÓN folder) ---------------------------------
def catalog_count(con):
    return con.execute("SELECT count(*) FROM data_catalog").fetchone()[0]


def _has_source_tables(con):
    return con.execute(
        "SELECT count(*) FROM information_schema.tables "
        "WHERE table_name = 'source_tables'").fetchone()[0] > 0


def catalog_summary(con):
    """Per-file summary; the DuckDB-table column reflects the typed SCPD tables
    AND the generic src_* tables loaded from every other sheet."""
    if _has_source_tables(con):
        return con.execute("""
            WITH src AS (
                SELECT file_name, count(*) AS n, max(table_name) AS one
                FROM source_tables GROUP BY 1
            )
            SELECT c.folder, c.file_name, c.file_type,
                   max(c.size_mb) AS size_mb,
                   count(*) AS sheets,
                   sum(c.n_rows) AS total_rows,
                   COALESCE(
                       max(c.loaded_table),
                       CASE WHEN any_value(src.n) = 1 THEN any_value(src.one)
                            WHEN any_value(src.n) > 1
                                 THEN any_value(src.n)::VARCHAR || ' tables'
                       END,
                       '—'
                   ) AS loaded_table
            FROM data_catalog c
            LEFT JOIN src ON src.file_name = c.file_name
            GROUP BY c.folder, c.file_name, c.file_type
            ORDER BY c.folder, c.file_name
        """).df()
    return con.execute("""
        SELECT folder, file_name, file_type, max(size_mb) AS size_mb,
               count(*) AS sheets, sum(n_rows) AS total_rows,
               COALESCE(max(loaded_table), '—') AS loaded_table
        FROM data_catalog GROUP BY 1, 2, 3 ORDER BY folder, file_name
    """).df()


def catalog_sheets(con, file_name=None):
    where, params = ("", [])
    if file_name:
        where, params = ("WHERE c.file_name = ?", [file_name])
    join = ("LEFT JOIN source_tables s "
            "ON s.file_name = c.file_name AND s.sheet_name = c.sheet_name"
            if _has_source_tables(con) else "")
    src_col = "s.table_name AS src_table" if _has_source_tables(con) else "NULL AS src_table"
    return con.execute(f"""
        SELECT c.sheet_name, c.n_columns, c.n_rows, c.columns, c.loaded_table,
               {src_col}
        FROM data_catalog c {join} {where} ORDER BY c.id
    """, params).df()


def catalog_totals(con):
    row = con.execute("""
        SELECT count(DISTINCT file_name), count(*), sum(n_rows)
        FROM data_catalog
    """).fetchone()
    out = {"files": row[0] or 0, "sheets": row[1] or 0, "rows": row[2] or 0,
           "src_tables": 0, "files_in_duckdb": 0}
    scpd_files = con.execute(
        "SELECT count(DISTINCT file_name) FROM data_catalog "
        "WHERE loaded_table IS NOT NULL").fetchone()[0] or 0
    if _has_source_tables(con):
        out["src_tables"] = con.execute(
            "SELECT count(*) FROM source_tables").fetchone()[0] or 0
        src_files = con.execute(
            "SELECT count(DISTINCT file_name) FROM source_tables").fetchone()[0] or 0
        out["files_in_duckdb"] = scpd_files + src_files
    else:
        out["files_in_duckdb"] = scpd_files
    return out


def table_counts(con):
    return {
        "transactions": con.execute("SELECT count(*) FROM transactions").fetchone()[0],
        "retirados": con.execute("SELECT count(*) FROM retirados").fetchone()[0],
    }
