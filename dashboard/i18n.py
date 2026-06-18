"""Lightweight EN / ES / KO internationalization for UI chrome.

IMPORTANT: only *interface* text is translated. Data values, DuckDB column
names, and source field names (NUM_TICKET, DESC_TIPO_DESECHO, sub_zona, route
codes, etc.) stay in their original form everywhere — they are the data model,
not UI copy.
"""
import streamlit as st

LANGUAGES = {"English": "en", "Español": "es", "한국어": "ko"}
_DEFAULT = "en"

# key -> {en, es, ko}. Missing keys fall back to English, then to the key.
TR = {
    # nav groups
    "nav.start": {"en": "Start here", "es": "Inicio", "ko": "시작하기"},
    "nav.story": {"en": "The story", "es": "El análisis", "ko": "분석 스토리"},
    "nav.analysis": {"en": "Deeper analysis", "es": "Análisis avanzado",
                     "ko": "심화 분석"},
    "nav.explore": {"en": "Explore", "es": "Explorar", "ko": "탐색"},
    "nav.trust": {"en": "Trust & data", "es": "Datos y confianza",
                  "ko": "데이터 · 신뢰"},
    "nav.system": {"en": "System", "es": "Sistema", "ko": "시스템"},
    # page titles
    "page.exec": {"en": "Executive Summary", "es": "Resumen ejecutivo",
                  "ko": "요약 보고"},
    "page.overview": {"en": "Overview", "es": "Resumen", "ko": "개요"},
    "page.services": {"en": "Service Types", "es": "Tipos de servicio",
                      "ko": "서비스 유형"},
    "page.operators": {"en": "Operators & Fleet", "es": "Operadores y flota",
                       "ko": "운영사 · 차량"},
    "page.geocycle": {"en": "GEOCYCLE Recovery", "es": "Recuperación GEOCYCLE",
                      "ko": "GEOCYCLE 회수"},
    "page.geo": {"en": "Geo & Routes", "es": "Geografía y rutas",
                 "ko": "지리 · 경로"},
    "page.ask": {"en": "Ask the Data", "es": "Pregúntale a los datos",
                 "ko": "데이터 질의"},
    "page.quality": {"en": "Data Quality & Catalog",
                     "es": "Calidad y catálogo de datos",
                     "ko": "데이터 품질 · 카탈로그"},
    "page.settings": {"en": "Settings", "es": "Configuración", "ko": "설정"},
    "page.forecast": {"en": "Capacity & Forecast", "es": "Capacidad y proyección",
                      "ko": "용량 · 예측"},
    "page.efficiency": {"en": "Operational Efficiency",
                        "es": "Eficiencia operativa", "ko": "운영 효율"},
    "page.integrity": {"en": "Revenue & Integrity",
                       "es": "Ingresos e integridad", "ko": "수익 · 무결성"},
    "page.diversion": {"en": "Composition & Diversion",
                       "es": "Composición y desvío", "ko": "구성 · 전환"},
    # common KPIs / words
    "kpi.total_trips": {"en": "Total trips", "es": "Viajes totales",
                        "ko": "총 운행"},
    "kpi.net_tonnage": {"en": "Net tonnage", "es": "Tonelaje neto",
                        "ko": "순 톤수"},
    "kpi.avg_per_trip": {"en": "Avg per trip", "es": "Prom. por viaje",
                         "ko": "운행당 평균"},
    "kpi.period": {"en": "Period", "es": "Período", "ko": "기간"},
    "kpi.date_range": {"en": "Date range", "es": "Rango de fechas",
                       "ko": "기간 범위"},
    "word.year": {"en": "Year", "es": "Año", "ko": "연도"},
    "word.all": {"en": "All", "es": "Todos", "ko": "전체"},
    "word.filter_year": {"en": "Filter by year", "es": "Filtrar por año",
                         "ko": "연도별 필터"},
    "word.trips": {"en": "Trips", "es": "Viajes", "ko": "운행"},
    "word.tonnes": {"en": "tonnes", "es": "toneladas", "ko": "톤"},
    "word.service_type": {"en": "Service type", "es": "Tipo de servicio",
                          "ko": "서비스 유형"},
    "kpi.total_net_tonnage": {"en": "Total net tonnage",
                              "es": "Tonelaje neto total", "ko": "총 순 톤수"},
    "kpi.recovery_trips": {"en": "Recovery trips", "es": "Viajes de recuperación",
                           "ko": "회수 운행"},
    "kpi.recovered_tonnage": {"en": "Recovered tonnage",
                              "es": "Tonelaje recuperado", "ko": "회수 톤수"},
    "kpi.organizations": {"en": "Organizations", "es": "Organizaciones",
                          "ko": "조직 수"},
    "kpi.zones": {"en": "Zones", "es": "Zonas", "ko": "구역"},
    "kpi.sub_zones": {"en": "Sub-zones", "es": "Sub-zonas", "ko": "세부 구역"},
    "kpi.micro_routes": {"en": "Micro-routes", "es": "Micro-rutas",
                         "ko": "마이크로 경로"},
    "kpi.route_tagged": {"en": "Route-tagged trips", "es": "Viajes con ruta",
                         "ko": "경로 태그 운행"},
    "kpi.median_payload": {"en": "Median payload", "es": "Carga mediana",
                           "ko": "중앙 적재량"},
    "kpi.under_threshold": {"en": "Under-loaded threshold",
                            "es": "Umbral de subcarga", "ko": "저적재 기준"},
    "kpi.under_trips": {"en": "Under-loaded trips", "es": "Viajes con subcarga",
                        "ko": "저적재 운행"},
    "kpi.light_tonnage": {"en": "Tonnage in light trips",
                          "es": "Tonelaje en viajes ligeros", "ko": "경적재 톤수"},
    "kpi.dup_weighings": {"en": "Duplicate weighings", "es": "Pesajes duplicados",
                          "ko": "중복 계량"},
    "kpi.tare_gross": {"en": "Tare > gross", "es": "Tara > bruto",
                       "ko": "공차 > 총중량"},
    "kpi.payload_outliers": {"en": "Payload outliers", "es": "Cargas atípicas",
                             "ko": "적재 이상치"},
    "kpi.missing_weight": {"en": "Missing weight", "es": "Peso faltante",
                           "ko": "중량 누락"},
    "kpi.landfilled": {"en": "Landfilled (net)", "es": "Dispuesto (neto)",
                       "ko": "매립 (순)"},
    "kpi.geocycle_recovered": {"en": "GEOCYCLE recovered",
                               "es": "Recuperado GEOCYCLE", "ko": "GEOCYCLE 회수"},
    "kpi.current_diversion": {"en": "Current diversion rate",
                              "es": "Tasa de desvío actual", "ko": "현재 전환율"},
    "eyebrow.brand": {"en": "THE HAMM SOLZ × EQUALGREEN",
                      "es": "THE HAMM SOLZ × EQUALGREEN",
                      "ko": "THE HAMM SOLZ × EQUALGREEN"},
    "page.cover": {"en": "Cover", "es": "Portada", "ko": "표지"},
    "page.arch": {"en": "How it works", "es": "Cómo funciona", "ko": "작동 원리"},
    "nav.about": {"en": "About this report", "es": "Sobre este informe",
                  "ko": "보고서 정보"},
    # forecast page
    "fc.subtitle": {
        "en": "Tonnage trajectory and how long Las Iguanas has left.",
        "es": "Trayectoria del tonelaje y vida útil restante de Las Iguanas.",
        "ko": "톤수 추세와 Las Iguanas 매립장의 잔여 수명."},
    "fc.remaining_cap": {"en": "Remaining capacity (million tonnes)",
                         "es": "Capacidad restante (millones de toneladas)",
                         "ko": "잔여 용량 (백만 톤)"},
    "fc.annual_growth": {"en": "Assumed annual growth",
                         "es": "Crecimiento anual asumido",
                         "ko": "연간 증가율 가정"},
    "fc.diversion": {"en": "GEOCYCLE diversion rate",
                     "es": "Tasa de desvío GEOCYCLE", "ko": "GEOCYCLE 전환율"},
    "fc.proj_fill": {"en": "Projected fill date", "es": "Fecha de llenado",
                     "ko": "예상 매립 완료일"},
    "fc.years_left": {"en": "Years remaining", "es": "Años restantes",
                      "ko": "잔여 연수"},
    "fc.life_ext": {"en": "Life extension from diversion",
                    "es": "Extensión por desvío", "ko": "전환에 따른 수명 연장"},
    "fc.assumption": {
        "en": "Assumption-driven projection — adjust the inputs above. "
              "Capacity isn't stated in the source data, so set it from your "
              "engineering estimate.",
        "es": "Proyección basada en supuestos — ajuste las entradas. La "
              "capacidad no figura en los datos; defínala con su estimación "
              "de ingeniería.",
        "ko": "가정 기반 예측입니다 — 위 입력값을 조정하세요. 용량은 원천 "
              "데이터에 없으므로 엔지니어링 추정치로 설정하세요."},
}


def current_lang():
    return st.session_state.get("lang", _DEFAULT)


def t(key):
    lang = current_lang()
    entry = TR.get(key)
    if not entry:
        return key
    return entry.get(lang) or entry.get(_DEFAULT) or key


def language_selector():
    """Sidebar language picker; stores the code in session_state['lang']."""
    labels = list(LANGUAGES.keys())
    codes = list(LANGUAGES.values())
    cur = current_lang()
    idx = codes.index(cur) if cur in codes else 0
    choice = st.sidebar.selectbox("🌐 Language / Idioma / 언어", labels, index=idx)
    st.session_state["lang"] = LANGUAGES[choice]
