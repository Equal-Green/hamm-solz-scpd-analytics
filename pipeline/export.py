"""Phase 2 hook: export the local DuckDB to a Postgres/Supabase target.

The function is fully wired but gated behind a feature flag so the app works
100% offline in Phase 1. DuckDB's `postgres` extension streams tables straight
into a Postgres connection string -- no pandas round-trip.
"""

# Phase 2 master switch. Flip to True (and install/enable network access) to
# allow real exports from the Settings page.
CLOUD_EXPORT_ENABLED = False

EXPORT_TABLES = ("transactions", "retirados", "pipeline_log")


def pg_export(con, database_url, enabled=CLOUD_EXPORT_ENABLED):
    """Copy the analytical tables into a Postgres/Supabase database.

    Returns a status dict. When `enabled` is False this is a no-op preview so
    the UI can be exercised without a live database.
    """
    if not enabled:
        return {
            "status": "disabled",
            "message": ("Cloud export is gated (Phase 2). Set "
                        "CLOUD_EXPORT_ENABLED = True in pipeline/export.py to "
                        "enable."),
            "tables": list(EXPORT_TABLES),
        }
    if not database_url:
        return {"status": "error", "message": "No DATABASE_URL provided."}

    con.execute("INSTALL postgres; LOAD postgres;")
    con.execute(f"ATTACH '{database_url}' AS pg (TYPE postgres)")
    copied = {}
    try:
        for table in EXPORT_TABLES:
            con.execute(f"CREATE OR REPLACE TABLE pg.{table} AS "
                        f"SELECT * FROM {table}")
            copied[table] = con.execute(
                f"SELECT count(*) FROM pg.{table}").fetchone()[0]
    finally:
        con.execute("DETACH pg")
    return {"status": "ok", "message": "Export complete.", "tables": copied}
