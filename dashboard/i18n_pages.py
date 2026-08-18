"""Page-level UI string translations (ES / KO), keyed by the English source.

Merged into i18n.TR. Entries have only 'es' and 'ko'; English falls back to the
key itself. Covers page subtitles, section headers, and chart titles. Data /
field names are never translated.
"""
TR_PAGES = {
    # --- small words used in templates ---
    "grew": {"es": "creció", "ko": "증가"},
    "fell": {"es": "cayó", "ko": "감소"},

    # --- metric labels (data_quality / settings / architecture / geo) ---
    "Total rows": {"es": "Filas totales", "ko": "총 행 수"},
    "Total rows (all)": {"es": "Filas totales (todas)", "ko": "총 행 수 (전체)"},
    "Zero net weight": {"es": "Peso neto cero", "ko": "순중량 0"},
    "Negative net weight": {"es": "Peso neto negativo", "ko": "음수 순중량"},
    "Duplicate ticket/year": {"es": "Ticket/año duplicado", "ko": "중복 티켓/연도"},
    "Non-positive net": {"es": "Neto no positivo", "ko": "0 이하 순중량"},
    "Null date / org": {"es": "Fecha / org nula", "ko": "날짜/조직 누락"},
    "Files delivered": {"es": "Archivos entregados", "ko": "전달 파일"},
    "Top-level folders": {"es": "Carpetas de nivel superior", "ko": "최상위 폴더"},
    "File types": {"es": "Tipos de archivo", "ko": "파일 유형"},
    "Tabular files → DuckDB": {"es": "Archivos tabulares → DuckDB",
                               "ko": "표 형식 파일 → DuckDB"},
    "Files in DuckDB": {"es": "Archivos en DuckDB", "ko": "DuckDB 내 파일"},
    "Spreadsheets": {"es": "Hojas de cálculo", "ko": "스프레드시트"},
    "Sheets / tabs": {"es": "Hojas / pestañas", "ko": "시트 / 탭"},
    "Source tables loaded": {"es": "Tablas de origen cargadas",
                             "ko": "적재된 원천 테이블"},
    "DuckDB file size": {"es": "Tamaño del archivo DuckDB", "ko": "DuckDB 파일 크기"},
    "Source size": {"es": "Tamaño de origen", "ko": "원천 크기"},
    "Rows loaded": {"es": "Filas cargadas", "ko": "적재 행 수"},
    "Load time (one-time)": {"es": "Tiempo de carga (única vez)",
                             "ko": "적재 시간 (1회)"},
    "Query response": {"es": "Respuesta de consulta", "ko": "쿼리 응답"},

    # --- compliance page (English-keyed section headers & tab labels) ---
"Rollup by category": {"es": "Resumen por categoría",
                           "ko": "범주별 집계"},
        "Contribution to the score": {"es": "Aporte al puntaje",
                                  "ko": "점수 기여도"},
    "Weighted points earned vs outstanding": {
        "es": "Puntos ponderados obtenidos vs pendientes",
        "ko": "획득 가중 점수 대비 미이행"},
    "Minimum content and evidence": {"es": "Contenido mínimo y evidencia",
                                     "ko": "최소 내용 및 증빙"},
    "Success indicators (Annex 2 §3)": {
        "es": "Indicadores de éxito (Anexo 2 §3)",
        "ko": "성과 지표 (부속서 2 §3)"},
    "Implementation requirements (Annex 2 §2)": {
        "es": "Requisitos de implementación (Anexo 2 §2)",
        "ko": "이행 요건 (부속서 2 §2)"},
    "Contract documents, in order of priority": {
        "es": "Documentos del contrato, en orden de prioridad",
        "ko": "계약 문서 (우선순위 순)"},
    "📋 Deliverables (Annex 2)": {"es": "📋 Entregables (Anexo 2)",
                                 "ko": "📋 산출물 (부속서 2)"},
    "📦 Materials received (Annex 3)": {
        "es": "📦 Materiales recibidos (Anexo 3)",
        "ko": "📦 수령 자료 (부속서 3)"},
    "✅ Indicators & implementation": {
        "es": "✅ Indicadores e implementación", "ko": "✅ 지표 · 이행"},
    "🚧 Scope guardrails": {"es": "🚧 Límites del alcance",
                            "ko": "🚧 업무 범위 한계"},
    "📄 Agreement terms": {"es": "📄 Términos del contrato",
                          "ko": "📄 계약 조건"},

    # --- tab labels ---
    "📂 The archive": {"es": "📂 El archivo", "ko": "📂 아카이브"},
    "✅ Integrity & quality": {"es": "✅ Integridad y calidad",
                              "ko": "✅ 무결성 · 품질"},
    "📇 Catalog": {"es": "📇 Catálogo", "ko": "📇 카탈로그"},
    "🗄️ Source tables": {"es": "🗄️ Tablas de origen", "ko": "🗄️ 원천 테이블"},
    "🗂️ Folder map": {"es": "🗂️ Mapa de carpetas", "ko": "🗂️ 폴더 맵"},
    "🔗 Data lineage": {"es": "🔗 Linaje de datos", "ko": "🔗 데이터 계보"},
    "📦 File types": {"es": "📦 Tipos de archivo", "ko": "📦 파일 유형"},

    # --- buttons ---
    "🔄 Rebuild catalog": {"es": "🔄 Reconstruir catálogo",
                           "ko": "🔄 카탈로그 재생성"},
    "🔄 Reload all source tables": {
        "es": "🔄 Recargar todas las tablas de origen",
        "ko": "🔄 모든 원천 테이블 재적재"},
    "📥 Load all source tables": {"es": "📥 Cargar todas las tablas de origen",
                                  "ko": "📥 모든 원천 테이블 적재"},
    "📇 Build catalog": {"es": "📇 Construir catálogo", "ko": "📇 카탈로그 생성"},
    "⬆️ Export to Postgres": {"es": "⬆️ Exportar a Postgres",
                             "ko": "⬆️ Postgres로 내보내기"},
    "🔄 Re-run pipeline (clear & reload)": {
        "es": "🔄 Reejecutar pipeline (limpiar y recargar)",
        "ko": "🔄 파이프라인 재실행 (초기화 후 재적재)"},
    "🔄 Rescan / reload": {"es": "🔄 Reescanear / recargar", "ko": "🔄 재스캔 / 재적재"},

    # --- control labels (geo / efficiency / diversion) ---
    "Routes": {"es": "Rutas", "ko": "경로"},
    "Color sub-zones by": {"es": "Colorear sub-zonas por", "ko": "세부 구역 색상 기준"},
    "Focus sub-zone": {"es": "Enfocar sub-zona", "ko": "세부 구역 집중"},
    "Organic %": {"es": "Orgánico %", "ko": "유기물 %"},
    "Recyclable % (paper, plastic, glass, metal)": {
        "es": "Reciclable % (papel, plástico, vidrio, metal)",
        "ko": "재활용 % (종이·플라스틱·유리·금속)"},
    "Capture rate of divertible %": {
        "es": "Tasa de captura de lo desviable %", "ko": "전환 가능분 포집률 %"},

    # --- Ask the Data: categories, prompt, questions ---
    "##### 💡 Suggested questions": {"es": "##### 💡 Preguntas sugeridas",
                                     "ko": "##### 💡 추천 질문"},
    "🧹 Clear conversation": {"es": "🧹 Borrar conversación", "ko": "🧹 대화 지우기"},
    "Ask a question about the data…": {
        "es": "Haz una pregunta sobre los datos…", "ko": "데이터에 대해 질문하세요…"},
    "Volume & trends": {"es": "Volumen y tendencias", "ko": "물량 · 추세"},
    "Service mix": {"es": "Composición de servicios", "ko": "서비스 구성"},
    "Operators & fleet": {"es": "Operadores y flota", "ko": "운영사 · 차량"},
    "Geo & routes": {"es": "Geografía y rutas", "ko": "지리 · 경로"},
    "Recovery & quality": {"es": "Recuperación y calidad", "ko": "회수 · 품질"},
    "How much waste is delivered, and is it growing?": {
        "es": "¿Cuántos residuos se entregan y están creciendo?",
        "ko": "폐기물 반입량은 얼마이며 증가하고 있나요?"},
    "Which month is busiest for deliveries?": {
        "es": "¿Qué mes es el más activo para entregas?",
        "ko": "반입이 가장 많은 달은?"},
    "Which city sectors generate the most waste?": {
        "es": "¿Qué sectores de la ciudad generan más residuos?",
        "ko": "어느 도시 구역이 가장 많은 폐기물을 배출하나요?"},
    "How big was the SERVICIOS ESPECIAL spike?": {
        "es": "¿Qué tan grande fue el alza de SERVICIOS ESPECIAL?",
        "ko": "SERVICIOS ESPECIAL 급증 규모는?"},
    "Which service type grew the most year-over-year?": {
        "es": "¿Qué tipo de servicio creció más interanualmente?",
        "ko": "전년 대비 가장 많이 증가한 서비스 유형은?"},
    "What's the waste mix by service type?": {
        "es": "¿Cuál es la composición por tipo de servicio?",
        "ko": "서비스 유형별 폐기물 구성은?"},
    "Which service carries the heaviest loads?": {
        "es": "¿Qué servicio lleva las cargas más pesadas?",
        "ko": "가장 무거운 적재를 운반하는 서비스는?"},
    "Who are the biggest operators by tonnage?": {
        "es": "¿Quiénes son los mayores operadores por tonelaje?",
        "ko": "톤수 기준 최대 운영사는?"},
    "How many companies use the landfill?": {
        "es": "¿Cuántas empresas usan el relleno?",
        "ko": "몇 개 업체가 매립장을 이용하나요?"},
    "What vehicle types deliver most often?": {
        "es": "¿Qué tipos de vehículo entregan con más frecuencia?",
        "ko": "가장 자주 반입하는 차량 유형은?"},
    "Which collection zone produces the most waste?": {
        "es": "¿Qué zona de recolección produce más residuos?",
        "ko": "가장 많은 폐기물을 배출하는 수거 구역은?"},
    "What are the busiest micro-routes?": {
        "es": "¿Cuáles son las micro-rutas más activas?",
        "ko": "가장 바쁜 마이크로 경로는?"},
    "How much does GEOCYCLE recover vs landfill?": {
        "es": "¿Cuánto recupera GEOCYCLE frente al relleno?",
        "ko": "GEOCYCLE 회수량 대 매립량은?"},
    "How complete and clean is the data?": {
        "es": "¿Qué tan completos y limpios están los datos?",
        "ko": "데이터는 얼마나 완전하고 깨끗한가요?"},

    # --- short captions / labels ---
    "Each folder, what it is, and where it lands in the report.": {
        "es": "Cada carpeta, qué es y dónde aparece en el informe.",
        "ko": "각 폴더의 정체와 보고서에서의 위치."},
    "**Per-file data model** — expand for sheets and columns.": {
        "es": "**Modelo de datos por archivo** — expande para ver hojas y "
              "columnas.",
        "ko": "**파일별 데이터 모델** — 시트와 컬럼을 보려면 펼치세요."},
    "Data model (sheets, columns) and row counts for every spreadsheet in the "
    "source ZIP.": {
        "es": "Modelo de datos (hojas, columnas) y conteo de filas de cada hoja "
              "del ZIP de origen.",
        "ko": "원천 ZIP의 모든 스프레드시트에 대한 데이터 모델(시트·컬럼)과 행 수."},
    "🛠️ Data improvement opportunities (for the next data pull)": {
        "es": "🛠️ Oportunidades de mejora de datos (para la próxima entrega)",
        "ko": "🛠️ 데이터 개선 기회 (다음 데이터 수집 시)"},
    "**Source characterization studies** (loaded in DuckDB for calibration):": {
        "es": "**Estudios de caracterización de origen** (cargados en DuckDB "
              "para calibración):",
        "ko": "**원천 caracterización 연구** (보정용으로 DuckDB에 적재됨):"},
    "**Duplicate-weighing candidates** — same plate, same day, identical net "
    "weight:": {
        "es": "**Candidatos a doble pesaje** — misma placa, mismo día, peso neto "
              "idéntico:",
        "ko": "**중복 계량 후보** — 동일 번호판, 동일 날짜, 동일 순중량:"},
    "Phase 2 — build the connection here; export is gated until enabled.": {
        "es": "Fase 2 — configura la conexión aquí; la exportación está "
              "bloqueada hasta habilitarse.",
        "ko": "2단계 — 여기서 연결을 구성하세요. 활성화 전까지 내보내기는 잠겨 "
              "있습니다."},
    "files": {"es": "archivos", "ko": "개 파일"},
    "transactions rows": {"es": "filas de transactions", "ko": "transactions 행 수"},
    "retirados rows": {"es": "filas de retirados", "ko": "retirados 행 수"},
    "No zero or negative net-weight trips.": {
        "es": "Sin viajes de peso neto cero o negativo.",
        "ko": "순중량 0 또는 음수 운행 없음."},
    "in DuckDB": {"es": "en DuckDB", "ko": "DuckDB 적재됨"},
    "**Cloud export:** 🔒 gated (coming soon)": {
        "es": "**Exportación a la nube:** 🔒 bloqueada (próximamente)",
        "ko": "**클라우드 내보내기:** 🔒 비활성 (준비 중)"},
    "**Cloud export:** 🟢 enabled": {
        "es": "**Exportación a la nube:** 🟢 habilitada",
        "ko": "**클라우드 내보내기:** 🟢 활성화됨"},
    "↳ **Feeds:** Geo reference.": {
        "es": "↳ **Alimenta:** Referencia geográfica.",
        "ko": "↳ **연결:** 지리 참조."},
    "↳ **Feeds:** Planning context (reference).": {
        "es": "↳ **Alimenta:** Contexto de planificación (referencia).",
        "ko": "↳ **연결:** 계획 맥락 (참조)."},
    "↳ **Feeds:** Policy context (PDF reference only).": {
        "es": "↳ **Alimenta:** Contexto normativo (solo referencia PDF).",
        "ko": "↳ **연결:** 정책 맥락 (PDF 참조 전용)."},
    "↳ **Feeds:** **Capacity & Forecast** (disposal projection workbook); site "
    "reference.": {
        "es": "↳ **Alimenta:** **Capacidad y proyección** (libro de proyección "
              "de disposición); referencia del sitio.",
        "ko": "↳ **연결:** **용량 · 예측** (처분 전망 워크북); 부지 참조."},

    # --- architecture ("How it works") prose ---
    "arch.intro": {
        "en": "Your report isn't a static PDF or a spreadsheet — it's a small, "
              "**self-contained analytics application**. It runs entirely on one "
              "machine with **no database server, no cloud account, and no "
              "subscriptions**. Two open-source technologies make that possible.",
        "es": "Tu informe no es un PDF estático ni una hoja de cálculo — es una "
              "pequeña **aplicación analítica autónoma**. Funciona por completo en "
              "una máquina, **sin servidor de base de datos, sin cuenta en la "
              "nube y sin suscripciones**. Dos tecnologías de código abierto lo "
              "hacen posible.",
        "ko": "이 보고서는 정적 PDF나 스프레드시트가 아니라 작고 **독립적인 분석 "
              "애플리케이션**입니다. **데이터베이스 서버도, 클라우드 계정도, 구독도 "
              "없이** 한 대의 컴퓨터에서 완전히 작동합니다. 두 가지 오픈소스 기술이 "
              "이를 가능하게 합니다."},
    "arch.duck.h": {"en": "### 🦆 DuckDB — the engine",
                    "es": "### 🦆 DuckDB — el motor", "ko": "### 🦆 DuckDB — 엔진"},
    "arch.duck.b": {
        "en": "DuckDB is an **analytical database that lives in a single file** "
              "(`scpd.duckdb`). Think of it as *“SQLite for analytics”*: it needs "
              "no server to install or run, yet it crunches hundreds of millions "
              "of values in milliseconds because it's **columnar** — built for "
              "summing, grouping and filtering, exactly what a report does.",
        "es": "DuckDB es una **base de datos analítica que vive en un solo "
              "archivo** (`scpd.duckdb`). Piénsalo como *«SQLite para analítica»*: "
              "no necesita servidor para instalarse o ejecutarse, y aun así "
              "procesa cientos de millones de valores en milisegundos porque es "
              "**columnar** — hecho para sumar, agrupar y filtrar, justo lo que "
              "hace un informe.",
        "ko": "DuckDB는 **단일 파일(`scpd.duckdb`)에 담기는 분석용 데이터베이스**"
              "입니다. *‘분석용 SQLite’*라고 생각하세요: 설치·실행에 서버가 필요 "
              "없으면서도 **컬럼 기반**이라 수억 개의 값을 밀리초 단위로 처리합니다 "
              "— 합계·그룹화·필터링에 최적화되어 보고서에 딱 맞습니다."},
    "arch.stream.h": {"en": "### 🎈 Streamlit — the interface",
                      "es": "### 🎈 Streamlit — la interfaz",
                      "ko": "### 🎈 Streamlit — 인터페이스"},
    "arch.stream.b": {
        "en": "Streamlit turns Python analysis into an **interactive web app** — "
              "the pages, charts, filters and maps you're clicking now. Every "
              "control re-runs a query against DuckDB and redraws instantly. No "
              "front-end engineering, no separate web server to manage.",
        "es": "Streamlit convierte el análisis en Python en una **app web "
              "interactiva** — las páginas, gráficos, filtros y mapas que estás "
              "usando. Cada control reejecuta una consulta a DuckDB y redibuja al "
              "instante. Sin ingeniería de front-end ni un servidor web aparte.",
        "ko": "Streamlit은 Python 분석을 **인터랙티브 웹 앱**으로 바꿉니다 — 지금 "
              "클릭하는 페이지·차트·필터·지도입니다. 모든 컨트롤이 DuckDB 쿼리를 "
              "다시 실행해 즉시 다시 그립니다. 프런트엔드 개발도, 별도 웹 서버도 "
              "필요 없습니다."},
    "arch.steps": {
        "en": "1. **Extract & transform (once).** A Python pipeline reads the "
              "source ZIP, parses the large Excel files row-by-row (they're too "
              "big to open normally), cleans dates and weights, and loads "
              "everything into DuckDB. This runs once; after that the app starts "
              "instantly.\n"
              "2. **Store.** All ~524,000 weighbridge records plus every other "
              "source table live in the single `scpd.duckdb` file — the portable "
              "*warehouse*.\n"
              "3. **Serve.** Each page asks DuckDB a question in SQL (\"net "
              "tonnage by zone in 2024\") and Streamlit renders the answer as a "
              "chart, table or map.",
        "es": "1. **Extraer y transformar (una vez).** Un pipeline en Python lee "
              "el ZIP de origen, analiza los grandes archivos Excel fila por fila "
              "(son demasiado grandes para abrirlos normalmente), limpia fechas y "
              "pesos, y carga todo en DuckDB. Se ejecuta una vez; después la app "
              "arranca al instante.\n"
              "2. **Almacenar.** Los ~524.000 registros de báscula y todas las "
              "demás tablas viven en el único archivo `scpd.duckdb` — el "
              "*almacén* portátil.\n"
              "3. **Servir.** Cada página hace una pregunta a DuckDB en SQL "
              "(«tonelaje neto por zona en 2024») y Streamlit muestra la "
              "respuesta como gráfico, tabla o mapa.",
        "ko": "1. **추출·변환 (1회).** Python 파이프라인이 원천 ZIP을 읽고, 대용량 "
              "Excel 파일을 한 행씩 파싱(일반적으로 열기엔 너무 큼)하며, 날짜와 "
              "중량을 정리해 모두 DuckDB에 적재합니다. 한 번만 실행되며 이후 앱은 "
              "즉시 시작됩니다.\n"
              "2. **저장.** 약 524,000건의 계량 기록과 그 외 모든 원천 테이블이 단일 "
              "`scpd.duckdb` 파일에 담깁니다 — 이동 가능한 *데이터 웨어하우스*.\n"
              "3. **제공.** 각 페이지는 SQL로 DuckDB에 질문(\"2024년 구역별 순 "
              "톤수\")하고 Streamlit이 답을 차트·표·지도로 렌더링합니다."},
    "arch.portable": {
        "en": "**Portable**  \nThe whole report is a folder. Clone it, point it "
              "at the data, run one command. No servers to provision.",
        "es": "**Portátil**  \nTodo el informe es una carpeta. Clónala, apúntala "
              "a los datos y ejecuta un comando. Sin servidores que aprovisionar.",
        "ko": "**이식성**  \n보고서 전체가 하나의 폴더입니다. 복제하고 데이터를 "
              "지정한 뒤 명령 하나만 실행하세요. 준비할 서버가 없습니다."},
    "arch.fast": {
        "en": "**Fast & offline**  \nColumnar queries return in milliseconds, "
              "with no internet required (except map tiles).",
        "es": "**Rápido y sin conexión**  \nLas consultas columnares responden en "
              "milisegundos, sin necesidad de internet (salvo los mapas).",
        "ko": "**빠르고 오프라인**  \n컬럼 기반 쿼리는 밀리초 안에 응답하며, 인터넷이 "
              "필요 없습니다 (지도 타일 제외)."},
    "arch.repro": {
        "en": "**Reproducible**  \nThe pipeline is code. Re-run it on next year's "
              "data and the same report rebuilds itself.",
        "es": "**Reproducible**  \nEl pipeline es código. Reejecútalo con los "
              "datos del próximo año y el mismo informe se reconstruye solo.",
        "ko": "**재현 가능**  \n파이프라인은 코드입니다. 내년 데이터로 다시 실행하면 "
              "같은 보고서가 스스로 재생성됩니다."},
    "arch.note": {
        "en": "Note on the source files: the delivery ZIP uses a streaming "
              "format that standard tools can't open, and the main Excel files "
              "are 65–92 MB each (one sheet expands to ~450 MB of XML). The "
              "pipeline reads them with custom binary + streaming parsers — a "
              "one-time engineering step so the day-to-day report stays simple "
              "and instant.",
        "es": "Nota sobre los archivos de origen: el ZIP usa un formato de "
              "streaming que las herramientas estándar no pueden abrir, y los "
              "Excel principales pesan 65–92 MB cada uno (una hoja se expande a "
              "~450 MB de XML). El pipeline los lee con analizadores binarios + "
              "de streaming a medida — un paso de ingeniería único para que el "
              "informe diario sea simple e instantáneo.",
        "ko": "원천 파일 참고: 전달 ZIP은 표준 도구로 열 수 없는 스트리밍 형식이며, "
              "주요 Excel 파일은 각 65~92MB입니다(한 시트가 ~450MB XML로 확장). "
              "파이프라인은 맞춤형 바이너리 + 스트리밍 파서로 이를 읽습니다 — 일상 "
              "보고서를 단순하고 즉각적으로 유지하기 위한 일회성 엔지니어링 단계입니다."},
    "arch.cloud": {
        "en": "Everything above runs **locally and offline**. When you want it "
              "hosted, the same app deploys to a small container (e.g. Google "
              "Cloud Run or Render) with the prebuilt `scpd.duckdb` baked in — or "
              "its tables export to a Postgres / Supabase database. The hooks are "
              "already in **Settings**; the offline version keeps working "
              "regardless.",
        "es": "Todo lo anterior funciona **local y sin conexión**. Cuando quieras "
              "alojarlo, la misma app se despliega en un contenedor pequeño (p. "
              "ej. Google Cloud Run o Render) con el `scpd.duckdb` ya construido — "
              "o sus tablas se exportan a una base Postgres / Supabase. Los "
              "ganchos ya están en **Configuración**; la versión offline sigue "
              "funcionando igual.",
        "ko": "위의 모든 것은 **로컬·오프라인**으로 작동합니다. 호스팅하려면 동일한 "
              "앱을 사전 빌드된 `scpd.duckdb`를 포함해 소형 컨테이너(예: Google "
              "Cloud Run, Render)에 배포하거나, 테이블을 Postgres / Supabase로 "
              "내보낼 수 있습니다. 훅은 이미 **설정**에 있으며, 오프라인 버전은 "
              "그대로 작동합니다."},

    # --- data_quality archive intro + folder narratives ---
    "dq.archive.intro": {
        "en": "Everything in this report traces back to a single delivery: the "
              "**`INFORMACIÓN`** folder handed over by the municipality "
              "(CIRCULAREP / Consorcio URVASEO). It mixes **operational data** "
              "(spreadsheets, a routes map) with a large body of **engineering "
              "and policy documents** (PDFs, CAD drawings, GIS). This tab orients "
              "you on what's inside and how each part feeds the analytics.",
        "es": "Todo en este informe proviene de una única entrega: la carpeta "
              "**`INFORMACIÓN`** entregada por el municipio (CIRCULAREP / "
              "Consorcio URVASEO). Mezcla **datos operativos** (hojas de cálculo, "
              "un mapa de rutas) con un gran conjunto de **documentos de "
              "ingeniería y política** (PDF, planos CAD, GIS). Esta pestaña te "
              "orienta sobre su contenido y cómo cada parte alimenta el análisis.",
        "ko": "이 보고서의 모든 것은 단일 전달물에서 비롯됩니다: 시(CIRCULAREP / "
              "Consorcio URVASEO)가 전달한 **`INFORMACIÓN`** 폴더입니다. **운영 "
              "데이터**(스프레드시트, 경로 지도)와 방대한 **엔지니어링·정책 "
              "문서**(PDF, CAD 도면, GIS)가 섞여 있습니다. 이 탭은 그 내용과 각 "
              "부분이 분석에 어떻게 기여하는지 안내합니다."},
    "Composition studies of municipal waste by stratum and year (2012–2026) — "
    "what the garbage is actually made of.": {
        "es": "Estudios de composición de residuos urbanos por estrato y año "
              "(2012–2026) — de qué está hecha realmente la basura.",
        "ko": "계층·연도별(2012–2026) 도시 폐기물 구성 연구 — 쓰레기가 실제로 무엇으로 "
              "이루어졌는지."},
    "A supplementary geographic layer (KMZ).": {
        "es": "Una capa geográfica complementaria (KMZ).",
        "ko": "보조 지리 레이어 (KMZ)."},
    "National & municipal norms governing solid-waste management.": {
        "es": "Normas nacionales y municipales que rigen la gestión de residuos "
              "sólidos.",
        "ko": "고형 폐기물 관리를 규율하는 국가·시 규정."},
    "Land-use and development plans, plus an ArcGIS map package.": {
        "es": "Planes de uso de suelo y desarrollo, más un paquete de mapas "
              "ArcGIS.",
        "ko": "토지 이용·개발 계획과 ArcGIS 맵 패키지."},
    "Catastro Urbano — 598,715 parcels — plus a rural cartography shapefile.": {
        "es": "Catastro Urbano — 598.715 predios — más un shapefile de "
              "cartografía rural.",
        "ko": "Catastro Urbano — 필지 598,715개 — 및 농촌 지형도 셰이프파일."},
    "Site engineering drawings (DWG) and disposal-quantity records & projections "
    "for the active landfill.": {
        "es": "Planos de ingeniería del sitio (DWG) y registros y proyecciones de "
              "cantidades dispuestas del relleno activo.",
        "ko": "활성 매립장의 부지 엔지니어링 도면(DWG)과 처분량 기록·전망."},
    "GIRS diagnosis, environmental management plan, and a collection-trip "
    "register.": {
        "es": "Diagnóstico GIRS, plan de manejo ambiental y un registro de viajes "
              "de recolección.",
        "ko": "GIRS 진단, 환경 관리 계획, 수거 운행 대장."},
    "The routes KML, micro-route drawings (DWG), and the EOP01/EOP02 production "
    "plans.": {
        "es": "El KML de rutas, los planos de micro-rutas (DWG) y los planes de "
              "producción EOP01/EOP02.",
        "ko": "경로 KML, 마이크로 경로 도면(DWG), EOP01/EOP02 생산 계획."},
    "**How raw files become the data model.** Four folders carry "
    "machine-readable data we ingest; the rest are documents that give context.": {
        "es": "**Cómo los archivos crudos se convierten en el modelo de datos.** "
              "Cuatro carpetas contienen datos legibles por máquina que "
              "ingerimos; el resto son documentos de contexto.",
        "ko": "**원시 파일이 데이터 모델이 되는 과정.** 네 개 폴더는 우리가 적재하는 "
              "기계 판독 데이터를 담고, 나머지는 맥락을 제공하는 문서입니다."},

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
