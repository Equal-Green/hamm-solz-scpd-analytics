"""Page-level UI string translations (ES / KO), keyed by the English source.

Merged into i18n.TR. Entries have only 'es' and 'ko'; English falls back to the
key itself. Covers page subtitles, section headers, and chart titles. Data /
field names are never translated.
"""
TR_PAGES = {
    # --- small words used in templates ---
    "grew": {"es": "creció", "ko": "증가"},
    "fell": {"es": "cayó", "ko": "감소"},

    # --- cover (title) page ---
    "MUNICIPAL SOLID WASTE ANALYTICS": {
        "es": "ANÁLISIS DE RESIDUOS SÓLIDOS URBANOS",
        "ko": "도시 고형 폐기물 분석"},
    "Prepared for": {"es": "Preparado para", "ko": "수신"},
    "Prepared by": {"es": "Preparado por", "ko": "작성"},
    "Scope": {"es": "Alcance", "ko": "범위"},
    "Data & analytics": {"es": "Datos y analítica", "ko": "데이터 · 분석"},
    "516,526 weighbridge trips": {"es": "516,526 viajes de báscula",
                                  "ko": "계량 운행 516,526건"},
    "5.9M tonnes · 2023–2025": {"es": "5,9M toneladas · 2023–2025",
                                "ko": "590만 톤 · 2023~2025"},
    "20 source datasets": {"es": "20 conjuntos de datos de origen",
                           "ko": "원천 데이터셋 20개"},
    "cover.footer": {
        "es": "Una aplicación analítica autónoma con DuckDB + Streamlit. Usa la "
              "barra lateral para navegar — empieza por el Resumen ejecutivo, o "
              "consulta «Cómo funciona» para la tecnología detrás de este "
              "entregable.",
        "ko": "DuckDB + Streamlit 기반의 독립형 분석 애플리케이션입니다. 사이드바로 "
              "이동하세요 — 요약 보고부터 시작하거나, 산출물의 기술은 ‘작동 원리’를 "
              "참고하세요.",
        "en": "A self-contained DuckDB + Streamlit analytics application. Use the "
              "sidebar to navigate — start with the Executive Summary, or see "
              "How it works for the technology behind this deliverable."},

    # --- home (executive summary) prose ---
    "home.narrative": {
        "en": "Between **{a}–{b}**, **{trips} truckloads** crossed the Las "
              "Iguanas weighbridge, delivering **{tonnes} tonnes** of municipal "
              "solid waste — an average of **{avg} kg per trip**. Annual tonnage "
              "{dir} **{growth}** over the period. This dashboard walks through "
              "*what* arrived, *who* brought it, *how much* was recovered, and "
              "*how far the numbers can be trusted* — and lets you query the data "
              "directly.",
        "es": "Entre **{a}–{b}**, **{trips} viajes** cruzaron la báscula de Las "
              "Iguanas, entregando **{tonnes} toneladas** de residuos sólidos "
              "urbanos — un promedio de **{avg} kg por viaje**. El tonelaje anual "
              "{dir} **{growth}** en el período. Este panel recorre *qué* llegó, "
              "*quién* lo trajo, *cuánto* se recuperó y *cuánto se puede confiar "
              "en las cifras* — y permite consultar los datos directamente.",
        "ko": "**{a}~{b}년** 사이 **{trips}건의 운행**이 Las Iguanas 계량대를 "
              "통과하며 도시 고형 폐기물 **{tonnes}톤**을 반입했습니다 — 운행당 평균 "
              "**{avg}kg**. 연간 톤수는 기간 동안 **{growth}** {dir}했습니다. 이 "
              "대시보드는 *무엇이* 들어왔는지, *누가* 가져왔는지, *얼마나* "
              "회수됐는지, *수치를 얼마나 신뢰할 수 있는지*를 보여주고 데이터에 직접 "
              "질의할 수 있게 합니다."},
    "Volume is rising": {"es": "El volumen está subiendo", "ko": "물량 증가 추세"},
    "Volume is falling": {"es": "El volumen está bajando", "ko": "물량 감소 추세"},
    "home.card.volume": {
        "en": "Net tonnage moved from **{f} t** in {fy} to **{l} t** in {ly} "
              "(**{g}**).",
        "es": "El tonelaje neto pasó de **{f} t** en {fy} a **{l} t** en {ly} "
              "(**{g}**).",
        "ko": "순 톤수는 {fy}년 **{f}톤**에서 {ly}년 **{l}톤**으로 변화했습니다 "
              "(**{g}**)."},
    "One service category spiked": {
        "es": "Una categoría de servicio se disparó",
        "ko": "한 서비스 범주가 급증"},
    "home.card.spike": {
        "en": "**SERVICIOS ESPECIAL** trips jumped **{pct}** from {y23} (2023) "
              "to {y24} (2024) — the standout anomaly in the data.",
        "es": "Los viajes de **SERVICIOS ESPECIAL** subieron **{pct}** de {y23} "
              "(2023) a {y24} (2024) — la anomalía más notable de los datos.",
        "ko": "**SERVICIOS ESPECIAL** 운행이 {y23}건(2023)에서 {y24}건(2024)으로 "
              "**{pct}** 급증했습니다 — 데이터에서 가장 두드러진 이상치입니다."},
    "Recovery is small but real": {
        "es": "La recuperación es pequeña pero real",
        "ko": "회수량은 적지만 실재함"},
    "home.card.recovery": {
        "en": "GEOCYCLE diverted **{rec} t** for material recovery — about "
              "**{pct}** of everything landfilled.",
        "es": "GEOCYCLE desvió **{rec} t** para recuperación de materiales — "
              "cerca del **{pct}** de todo lo enterrado.",
        "ko": "GEOCYCLE는 물질 회수를 위해 **{rec}톤**을 전환했습니다 — 전체 "
              "매립량의 약 **{pct}**."},
    "One operator dominates": {"es": "Un operador domina",
                               "ko": "한 운영사가 지배적"},
    "home.card.operator": {
        "en": "**{company}** alone accounts for **{share}** of all trips — the "
              "municipal collection consortium.",
        "es": "**{company}** representa por sí solo el **{share}** de los viajes "
              "— el consorcio municipal de recolección.",
        "ko": "**{company}** 한 곳이 전체 운행의 **{share}**를 차지합니다 — 시 수거 "
              "컨소시엄입니다."},
    "home.clean": {
        "en": "✅ **The data is clean.** No zero or negative net weights, no "
              "missing service types, no duplicate tickets. Full integrity checks "
              "on the **Data Quality & Catalog** page.",
        "es": "✅ **Los datos están limpios.** Sin pesos netos cero o negativos, "
              "sin tipos de servicio faltantes, sin tickets duplicados. "
              "Verificación completa en la página **Calidad y catálogo de datos**.",
        "ko": "✅ **데이터가 깨끗합니다.** 0 또는 음수 순중량 없음, 누락된 서비스 "
              "유형 없음, 중복 티켓 없음. 전체 무결성 검사는 **데이터 품질 · "
              "카탈로그** 페이지에서 확인하세요."},
    "home.howto": {
        "en": "- **The story →** *Overview, Service Types, Operators & Fleet, "
              "GEOCYCLE Recovery* — the narrative, in order.\n"
              "- **Explore →** *Ask the Data* — put questions to the dataset.\n"
              "- **Trust & data →** *Data Quality & Catalog* — integrity checks "
              "and a model of every source spreadsheet.\n"
              "- **System →** *Settings* — pipeline status, reloads, cloud export.",
        "es": "- **El análisis →** *Resumen, Tipos de servicio, Operadores y "
              "flota, Recuperación GEOCYCLE* — la narrativa, en orden.\n"
              "- **Explorar →** *Pregúntale a los datos* — haz preguntas al "
              "conjunto de datos.\n"
              "- **Datos y confianza →** *Calidad y catálogo* — verificaciones y "
              "un modelo de cada hoja de origen.\n"
              "- **Sistema →** *Configuración* — estado del pipeline, recargas, "
              "exportación a la nube.",
        "ko": "- **분석 스토리 →** *개요, 서비스 유형, 운영사·차량, GEOCYCLE 회수* "
              "— 순서대로 이어지는 내러티브.\n"
              "- **탐색 →** *데이터 질의* — 데이터셋에 질문하기.\n"
              "- **데이터·신뢰 →** *데이터 품질·카탈로그* — 무결성 검사와 모든 원천 "
              "스프레드시트의 모델.\n"
              "- **시스템 →** *설정* — 파이프라인 상태, 재적재, 클라우드 내보내기."},
    "Use the grouped navigation in the sidebar.": {
        "es": "Usa la navegación agrupada en la barra lateral.",
        "ko": "사이드바의 그룹 메뉴를 사용하세요."},

    # --- sub-page callouts & captions ---
    "sv.anomaly": {
        "en": "⚠️ **Anomaly — SERVICIOS ESPECIAL trip spike.** Trips rose "
              "**{pct}** from **{y23}** (2023) to **{y24}** (2024). (The project "
              "brief labelled this ~+83%; the live figure from the data is {pct0}.)",
        "es": "⚠️ **Anomalía — alza de viajes de SERVICIOS ESPECIAL.** Los viajes "
              "subieron **{pct}** de **{y23}** (2023) a **{y24}** (2024). (El "
              "informe lo etiquetó como ~+83%; la cifra real de los datos es "
              "{pct0}.)",
        "ko": "⚠️ **이상치 — SERVICIOS ESPECIAL 운행 급증.** 운행이 **{y23}**건"
              "(2023)에서 **{y24}**건(2024)으로 **{pct}** 증가했습니다. (보고서에는 "
              "~+83%로 기재됐으나 데이터 실측치는 {pct0}입니다.)"},
    "`A->B %` columns show the year-over-year change in trip count.": {
        "es": "Las columnas `A->B %` muestran el cambio interanual en el número "
              "de viajes.",
        "ko": "`A->B %` 열은 운행 수의 전년 대비 변화를 나타냅니다."},
    "gc.inverted": {
        "en": "**Inverted weight logic.** GEOCYCLE trucks arrive **empty** and "
              "leave **loaded** with recovered material, so "
              "`PESO_SALIDA > PESO_INGRESO` is correct here and net recovered = "
              "exit − entry (the opposite of landfill deliveries).",
        "es": "**Lógica de pesaje invertida.** Los camiones de GEOCYCLE llegan "
              "**vacíos** y salen **cargados** con material recuperado, por lo que "
              "`PESO_SALIDA > PESO_INGRESO` es correcto aquí y el neto recuperado "
              "= salida − entrada (lo opuesto a las entregas al relleno).",
        "ko": "**역방향 계량 논리.** GEOCYCLE 차량은 **비어서** 도착해 회수 물질을 "
              "**싣고** 나가므로 `PESO_SALIDA > PESO_INGRESO`가 정상이며, 순 회수 = "
              "출차 − 입차입니다 (매립 반입과 반대)."},
    "ef.underloaded": {
        "en": "“Under-loaded” = net payload below {thr} kg (half the fleet "
              "median). These are trucks dispatched well below capacity — "
              "candidates for route consolidation.",
        "es": "«Subcarga» = carga neta por debajo de {thr} kg (la mitad de la "
              "mediana de la flota). Son camiones despachados muy por debajo de "
              "su capacidad — candidatos a consolidar rutas.",
        "ko": "‘저적재’ = 순 적재량이 {thr}kg 미만 (차량 중앙값의 절반). 용량보다 "
              "훨씬 적게 배차된 차량으로, 경로 통합 후보입니다."},
    "Where the day's arrivals concentrate — peaks are weighbridge congestion "
    "windows worth staffing for.": {
        "es": "Dónde se concentran las llegadas del día — los picos son ventanas "
              "de congestión de la báscula que conviene dotar de personal.",
        "ko": "하루 중 반입이 집중되는 시점 — 정점은 인력 배치가 필요한 계량대 혼잡 "
              "시간대입니다."},
    "in.anomaly": {
        "en": "⚠️ **SERVICIOS ESPECIAL** trips rose **{pct}** ({y23} → {y24}) "
              "from 2023 to 2024. Below: which operators drove it — the first "
              "place to check for tariff leakage.",
        "es": "⚠️ Los viajes de **SERVICIOS ESPECIAL** subieron **{pct}** "
              "({y23} → {y24}) de 2023 a 2024. Abajo: qué operadores lo "
              "impulsaron — el primer lugar para revisar fugas de tarifa.",
        "ko": "⚠️ **SERVICIOS ESPECIAL** 운행이 2023→2024년 **{pct}** "
              "({y23} → {y24}) 증가했습니다. 아래: 어떤 운영사가 주도했는지 — 요금 "
              "누수를 점검할 첫 지점입니다."},
    "in.duplicates": {
        "en": "Duplicates can be legitimate (a truck running the same route "
              "twice with an identical load) or double-counted tickets. Each "
              "repeated ticket that shouldn't be billed twice is potential "
              "revenue leakage worth auditing.",
        "es": "Los duplicados pueden ser legítimos (un camión que repite la "
              "misma ruta con carga idéntica) o tickets contados dos veces. Cada "
              "ticket repetido que no debería facturarse dos veces es una posible "
              "fuga de ingresos que conviene auditar.",
        "ko": "중복은 정상일 수도(동일 적재로 같은 경로를 두 번 운행) 있고 이중 "
              "집계된 티켓일 수도 있습니다. 두 번 청구되면 안 되는 반복 티켓은 감사가 "
              "필요한 잠재적 수익 누수입니다."},
    "dv.composition": {
        "en": "The source caracterización studies aren't a clean per-tonne "
              "table, so set the composition below (defaults reflect typical "
              "Ecuadorian municipal solid waste). Source studies are listed at "
              "the bottom for calibration.",
        "es": "Los estudios de caracterización de origen no son una tabla "
              "limpia por tonelada, así que define la composición abajo (los "
              "valores por defecto reflejan los residuos urbanos típicos de "
              "Ecuador). Los estudios de origen se listan al final para calibrar.",
        "ko": "원천 caracterización 연구는 톤당 정제된 표가 아니므로 아래에서 구성을 "
              "설정하세요 (기본값은 에콰도르 도시 고형 폐기물의 전형치). 보정용 원천 "
              "연구는 하단에 나열되어 있습니다."},
    "dv.scenario": {
        "en": "At **{capture}** capture of the divertible fraction, diversion "
              "would rise from **{cur}** to **{new}** — about **{ach} t** kept "
              "out of Las Iguanas over the period (vs {rec} t recovered today).",
        "es": "Con una captura del **{capture}** de la fracción desviable, el "
              "desvío subiría de **{cur}** a **{new}** — unas **{ach} t** fuera "
              "de Las Iguanas en el período (vs {rec} t recuperadas hoy).",
        "ko": "전환 가능 비율의 **{capture}**를 포집하면 전환율이 **{cur}**에서 "
              "**{new}**로 상승합니다 — 기간 동안 약 **{ach}톤**을 Las Iguanas에서 "
              "줄입니다 (현재 회수 {rec}톤 대비)."},
    "Characterization tables not found in the catalog — build the catalog on "
    "the Data Quality page.": {
        "es": "No se encontraron tablas de caracterización en el catálogo — "
              "construye el catálogo en la página Calidad de datos.",
        "ko": "카탈로그에서 caracterización 테이블을 찾지 못했습니다 — 데이터 품질 "
              "페이지에서 카탈로그를 생성하세요."},
    "ask.prompt": {
        "en": "Pick a question above, or type one below — e.g. *“who hauls the "
              "most waste?”* or *“is volume growing?”*",
        "es": "Elige una pregunta arriba o escribe una abajo — p. ej. *«¿quién "
              "transporta más residuos?»* o *«¿está creciendo el volumen?»*",
        "ko": "위에서 질문을 고르거나 아래에 입력하세요 — 예: *‘누가 가장 많이 "
              "운반하나?’* 또는 *‘물량이 증가하고 있나?’*"},

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
