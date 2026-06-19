"""Page-level UI string translations (ES / KO), keyed by the English source.

Merged into i18n.TR. Entries have only 'es' and 'ko'; English falls back to the
key itself. Covers page subtitles, section headers, and chart titles. Data /
field names are never translated.
"""
TR_PAGES = {
    "Guayaquil's Waste, in Three Years": {
        "es": "Los residuos de Guayaquil, en tres años",
        "ko": "3년간의 과야킬 폐기물"},
    # --- page subtitles (render_header arg 2) ---
    "Every truckload weighed at the Las Iguanas landfill — Consorcio URVASEO, "
    "under CIRCULAREP — from 2023 to 2025.": {
        "es": "Cada viaje pesado en el relleno de Las Iguanas — Consorcio "
              "URVASEO, bajo CIRCULAREP — de 2023 a 2025.",
        "ko": "Las Iguanas 매립장에서 계량된 모든 운행 — Consorcio URVASEO, "
              "CIRCULAREP 관할 — 2023~2025년."},
    "Volume and tonnage trends across 2023–2025.": {
        "es": "Tendencias de volumen y tonelaje entre 2023 y 2025.",
        "ko": "2023~2025년 물량 및 톤수 추세."},
    "Trips and tonnage by waste service category.": {
        "es": "Viajes y tonelaje por categoría de servicio de residuos.",
        "ko": "폐기물 서비스 범주별 운행 및 톤수."},
    "Companies and vehicle classes delivering to the landfill.": {
        "es": "Empresas y clases de vehículos que llegan al relleno.",
        "ko": "매립장에 반입하는 업체 및 차량 종류."},
    "Material recovery — inverted weigh logic.": {
        "es": "Recuperación de materiales — lógica de pesaje invertida.",
        "ko": "물질 회수 — 역방향 계량 논리."},
    "Where waste comes from — collection zones, sub-zones and micro-routes.": {
        "es": "De dónde viene el residuo — zonas, sub-zonas y micro-rutas.",
        "ko": "폐기물의 출처 — 수거 구역, 세부 구역, 마이크로 경로."},
    "Put questions to the SCPD dataset — pick a suggestion or type your own.": {
        "es": "Haz preguntas al conjunto de datos SCPD — elige una sugerencia "
              "o escribe la tuya.",
        "ko": "SCPD 데이터에 질문하기 — 제안을 고르거나 직접 입력하세요."},
    "Orient on the source archive, then verify the data it produced.": {
        "es": "Conoce el archivo de origen y luego verifica los datos "
              "resultantes.",
        "ko": "원천 아카이브를 파악한 뒤 생성된 데이터를 검증하세요."},
    "Payload utilization, under-loaded trips, and weighbridge timing.": {
        "es": "Aprovechamiento de carga, viajes con subcarga y horarios de "
              "báscula.",
        "ko": "적재 활용도, 저적재 운행, 계량대 시간대."},
    "Where the SERVICIOS ESPECIAL spike came from, and weighbridge integrity "
    "flags.": {
        "es": "De dónde vino el alza de SERVICIOS ESPECIAL y alertas de "
              "integridad de la báscula.",
        "ko": "SERVICIOS ESPECIAL 급증의 원인과 계량 무결성 경고."},
    "How much of what we bury could be diverted instead.": {
        "es": "Cuánto de lo que enterramos podría desviarse.",
        "ko": "매립 중인 폐기물 중 전환 가능한 비율."},
    "The technology behind your deliverable — DuckDB + Streamlit.": {
        "es": "La tecnología detrás de su entregable — DuckDB + Streamlit.",
        "ko": "산출물의 기반 기술 — DuckDB + Streamlit."},
    "Tonnage trajectory and how long Las Iguanas has left.": {
        "es": "Trayectoria del tonelaje y vida útil restante de Las Iguanas.",
        "ko": "톤수 추세와 Las Iguanas의 잔여 수명."},

    # --- section headers (st.subheader) ---
    "Key findings": {"es": "Hallazgos clave", "ko": "핵심 결과"},
    "How to read this dashboard": {"es": "Cómo leer este panel",
                                   "ko": "이 대시보드 읽는 법"},
    "Year-over-year trips by service": {
        "es": "Viajes interanuales por servicio", "ko": "서비스별 전년 대비 운행"},
    "Avg net weight per trip by company": {
        "es": "Peso neto medio por viaje por empresa",
        "ko": "업체별 운행당 평균 순중량"},
    "Recovery vs. landfill volume": {"es": "Recuperación vs. volumen enterrado",
                                     "ko": "회수량 대 매립량"},
    "Row counts: loaded vs. brief": {"es": "Conteo de filas: cargado vs. informe",
                                     "ko": "행 수: 적재 대 기준"},
    "Transactions — key-column health": {
        "es": "Transacciones — salud de columnas clave",
        "ko": "트랜잭션 — 핵심 컬럼 상태"},
    "Null rates on key columns (transactions)": {
        "es": "Tasas de nulos en columnas clave (transacciones)",
        "ko": "핵심 컬럼 결측률 (트랜잭션)"},
    "Date range per year": {"es": "Rango de fechas por año", "ko": "연도별 기간 범위"},
    "GEOCYCLE (retirados)": {"es": "GEOCYCLE (retirados)", "ko": "GEOCYCLE (retirados)"},
    "Source data catalog — INFORMACIÓN folder": {
        "es": "Catálogo de datos de origen — carpeta INFORMACIÓN",
        "ko": "원천 데이터 카탈로그 — INFORMACIÓN 폴더"},
    "All source tables in DuckDB": {"es": "Todas las tablas de origen en DuckDB",
                                    "ko": "DuckDB의 모든 원천 테이블"},
    "Weighbridge integrity flags": {"es": "Alertas de integridad de la báscula",
                                    "ko": "계량 무결성 경고"},
    "Composition & diversion scenario": {
        "es": "Escenario de composición y desvío", "ko": "구성 및 전환 시나리오"},
    "Weighbridge activity — hour × day of week": {
        "es": "Actividad de báscula — hora × día de la semana",
        "ko": "계량대 활동 — 시간 × 요일"},
    "Top micro-routes": {"es": "Micro-rutas principales", "ko": "주요 마이크로 경로"},
    "Sub-zone activity by month": {"es": "Actividad de sub-zonas por mes",
                                   "ko": "월별 세부 구역 활동"},
    "Pipeline status": {"es": "Estado del pipeline", "ko": "파이프라인 상태"},
    "Re-run pipeline": {"es": "Reejecutar pipeline", "ko": "파이프라인 재실행"},
    "Export to Postgres / Supabase": {"es": "Exportar a Postgres / Supabase",
                                      "ko": "Postgres / Supabase로 내보내기"},
    "How the data flows": {"es": "Cómo fluyen los datos", "ko": "데이터 흐름"},
    "Why this approach": {"es": "Por qué este enfoque", "ko": "이 방식을 택한 이유"},
    "What it took to get here": {"es": "Lo que costó llegar aquí",
                                 "ko": "여기까지의 과정"},
    "Path to the cloud (optional, Phase 2)": {
        "es": "Camino a la nube (opcional, Fase 2)",
        "ko": "클라우드 전환 경로 (선택, 2단계)"},

    # --- chart titles ---
    "Monthly trip volume (years overlaid)": {
        "es": "Volumen mensual de viajes (años superpuestos)",
        "ko": "월별 운행량 (연도 중첩)"},
    "Total annual net tonnage": {"es": "Tonelaje neto anual total",
                                 "ko": "연간 총 순 톤수"},
    "Monthly tonnage by service type": {
        "es": "Tonelaje mensual por tipo de servicio",
        "ko": "서비스 유형별 월간 톤수"},
    "Trips by service type": {"es": "Viajes por tipo de servicio",
                              "ko": "서비스 유형별 운행"},
    "Net tonnage by service type": {"es": "Tonelaje neto por tipo de servicio",
                                    "ko": "서비스 유형별 순 톤수"},
    "Top 10 companies by trips": {"es": "Top 10 empresas por viajes",
                                  "ko": "운행 상위 10개 업체"},
    "Top 10 companies by net tonnage": {
        "es": "Top 10 empresas por tonelaje neto", "ko": "순 톤수 상위 10개 업체"},
    "Vehicle class distribution": {"es": "Distribución por clase de vehículo",
                                   "ko": "차량 종류 분포"},
    "Monthly recovered tonnage": {"es": "Tonelaje recuperado mensual",
                                  "ko": "월별 회수 톤수"},
    "Landfilled vs. recovered tonnage by year": {
        "es": "Tonelaje enterrado vs. recuperado por año",
        "ko": "연도별 매립 대 회수 톤수"},
    "Net tonnage by zone": {"es": "Tonelaje neto por zona", "ko": "구역별 순 톤수"},
    "Net tonnage by zone → sub-zone": {
        "es": "Tonelaje neto por zona → sub-zona",
        "ko": "구역 → 세부 구역별 순 톤수"},
    "Top sub-zones by tonnage": {"es": "Sub-zonas principales por tonelaje",
                                 "ko": "톤수 상위 세부 구역"},
    "🗺️ Collection map — sub-zones & routes": {
        "es": "🗺️ Mapa de recolección — sub-zonas y rutas",
        "ko": "🗺️ 수거 지도 — 세부 구역 및 경로"},
    "Monthly net tonnage — history & forecast": {
        "es": "Tonelaje neto mensual — histórico y proyección",
        "ko": "월별 순 톤수 — 실적 및 예측"},
    "Cumulative disposal vs. remaining capacity": {
        "es": "Disposición acumulada vs. capacidad restante",
        "ko": "누적 매립량 대 잔여 용량"},
    "Avg payload by vehicle class (kg)": {
        "es": "Carga media por clase de vehículo (kg)",
        "ko": "차량 종류별 평균 적재량 (kg)"},
    "Payload distribution": {"es": "Distribución de carga", "ko": "적재량 분포"},
    "SERVICIOS ESPECIAL — trip increase by operator (2023→2024)": {
        "es": "SERVICIOS ESPECIAL — aumento de viajes por operador (2023→2024)",
        "ko": "SERVICIOS ESPECIAL — 운영사별 운행 증가 (2023→2024)"},
    "Assumed waste composition": {"es": "Composición de residuos asumida",
                                  "ko": "가정한 폐기물 구성"},
    "Diversion potential (3-yr total)": {
        "es": "Potencial de desvío (total 3 años)",
        "ko": "전환 잠재량 (3년 합계)"},
    "Files by type": {"es": "Archivos por tipo", "ko": "유형별 파일"},
}
