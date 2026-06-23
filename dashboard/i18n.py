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


try:
    from i18n_pages import TR_PAGES
    for _k, _v in TR_PAGES.items():
        TR.setdefault(_k, {}).update(_v)
except ImportError:
    pass


def current_lang():
    return st.session_state.get("lang", _DEFAULT)


def t(key):
    lang = current_lang()
    entry = TR.get(key)
    if not entry:
        return key
    return entry.get(lang) or entry.get(_DEFAULT) or key


# --- automatic translation layer --------------------------------------------
# Every Streamlit text call routes its display string through translate():
#   1. curated dictionary (TR) — precise, brand/proper-noun control
#   2. on-disk cache (i18n_cache.json) — instant, offline, committed
#   3. Google Translate (deep-translator) — fills anything new, when online
# Data values, DuckDB field/table names, code, and HTML are never translated.
import json as _json  # noqa: E402
import os as _os  # noqa: E402
import re as _re  # noqa: E402

_RECORD = bool(_os.environ.get("I18N_RECORD"))
_MISSING = set()

# Only brand / proper names stay in their original form (per request, field
# names and filenames ARE translated now).
NO_TRANSLATE = {
    "EqualGreen", "DuckDB", "Streamlit", "GEOCYCLE", "CIRCULAREP", "URVASEO",
    "DATABASE_URL",
}
_HANGUL = _re.compile(r"[가-힣]")
_DATA_MARKERS = ("src_",)   # only generated table prefixes; filenames translate

_CACHE_PATH = _os.path.join(_os.path.dirname(_os.path.abspath(__file__)),
                            "i18n_cache.json")
try:
    with open(_CACHE_PATH, encoding="utf-8") as _f:
        _CACHE = _json.load(_f)
except (OSError, ValueError):
    _CACHE = {}

try:
    from deep_translator import GoogleTranslator as _GT
except Exception:  # noqa: BLE001 — optional; offline falls back to cache/EN
    _GT = None


_NOTR = "⁠"  # invisible marker: "never translate this string"


def notr(s):
    """Mark a (data) string so the auto-translator leaves it untouched."""
    return _NOTR + s if isinstance(s, str) else s


def _has_lower_ascii(s):
    return any("a" <= c <= "z" for c in s)


def _skip(s):
    """Skip HTML, code/ascii blocks, pure numbers, and data/field values."""
    st_ = s.strip()
    if not st_ or st_[0] == "<" or "style=" in st_ or st_.startswith("```") \
            or "<div" in st_:
        return True
    if not any(c.isalpha() for c in st_):
        return True
    low = st_.lower()
    if any(m in low for m in _DATA_MARKERS):
        return True
    if st_.count(",") >= 2 and not _has_lower_ascii(st_):  # ALL-CAPS data lists
        return True
    return False


def _save_cache():
    try:
        with open(_CACHE_PATH, "w", encoding="utf-8") as f:
            _json.dump(_CACHE, f, ensure_ascii=False, indent=0)
    except OSError:
        pass


def translate(s):
    if not isinstance(s, str):
        return s
    if s.startswith(_NOTR):           # explicitly marked data → strip marker
        return s[len(_NOTR):]
    if _skip(s):
        return s
    lang = current_lang()
    if lang == _DEFAULT:
        return s
    # never translate field/table names, ALL-CAPS data, or already-target text
    if s in NO_TRANSLATE or not _has_lower_ascii(s):
        return s
    if lang == "ko" and _HANGUL.search(s):
        return s
    # 1. cache (instant, offline)
    bucket = _CACHE.setdefault(lang, {})
    if s in bucket:
        return bucket[s]
    # 2. Google Translate — the default engine (when online), then cache it
    if _GT is not None:
        try:
            out = _GT(source="en", target=lang).translate(s) or s
            bucket[s] = out
            _save_cache()
            return out
        except Exception:  # noqa: BLE001
            pass
    # 3. fallback: curated dictionary, else original English
    entry = TR.get(s)
    if entry:
        return entry.get(lang) or entry.get(_DEFAULT) or s
    if _RECORD:
        _MISSING.add(s)
    return s


def _install_patches():
    """Patch DeltaGenerator + st so display strings auto-translate. Idempotent."""
    from streamlit.delta_generator import DeltaGenerator as _DG
    if getattr(_DG, "_i18n_patched", False):
        return
    _DG._i18n_patched = True

    def _wrap(orig):
        def w(self, *a, **k):
            if a and isinstance(a[0], str):
                a = (translate(a[0]),) + a[1:]
            for key in ("label", "body"):
                if isinstance(k.get(key), str):
                    k[key] = translate(k[key])
            return orig(self, *a, **k)
        return w

    # first-arg text methods (label / body / value-as-text)
    for name in ("markdown", "caption", "subheader", "header", "title", "write",
                 "info", "success", "warning", "error", "text", "button",
                 "download_button", "checkbox", "toggle", "radio", "selectbox",
                 "multiselect", "slider", "select_slider", "text_input",
                 "number_input", "text_area", "date_input", "time_input",
                 "chat_input", "expander", "metric", "tab", "popover"):
        orig = getattr(_DG, name, None)
        if orig:
            setattr(_DG, name, _wrap(orig))

    # dataframe / table / data_editor: translate the column headers
    def _df_cfg(data, k):
        cols = getattr(data, "columns", None)
        cols = list(cols) if cols is not None else []
        if not cols:
            return k
        cfg = dict(k.get("column_config") or {})
        for c in cols:
            cur = cfg.get(c)
            if cur is None:
                cfg[c] = translate(str(c))
            elif isinstance(cur, str):
                cfg[c] = translate(cur)
        k["column_config"] = cfg
        return k

    for name in ("dataframe", "table", "data_editor"):
        orig = getattr(_DG, name, None)
        if orig:
            def _dgw(self, data=None, *a, _o=orig, **k):
                return _o(self, data, *a, **_df_cfg(data, k))
            setattr(_DG, name, _dgw)

    # tabs: translate the list of labels
    _tabs = getattr(_DG, "tabs", None)
    if _tabs:
        def _tabs_w(self, labels, *a, **k):
            if isinstance(labels, (list, tuple)):
                labels = [translate(x) if isinstance(x, str) else x for x in labels]
            return _tabs(self, labels, *a, **k)
        setattr(_DG, "tabs", _tabs_w)

    # Top-level st.* functions are bound separately from the class, so patch
    # them too (covers st.markdown / st.subheader / st.write inside with-blocks).
    def _wrap_fn(orig):
        def w(*a, **k):
            if a and isinstance(a[0], str):
                a = (translate(a[0]),) + a[1:]
            for key in ("label", "body"):
                if isinstance(k.get(key), str):
                    k[key] = translate(k[key])
            return orig(*a, **k)
        return w

    for name in ("markdown", "caption", "subheader", "header", "title", "write",
                 "info", "success", "warning", "error", "text", "button",
                 "checkbox", "toggle", "radio", "selectbox", "multiselect",
                 "slider", "select_slider", "text_input", "number_input",
                 "text_area", "chat_input", "expander", "metric", "popover"):
        orig = getattr(st, name, None)
        if orig:
            setattr(st, name, _wrap_fn(orig))

    _otabs = getattr(st, "tabs", None)
    if _otabs:
        def _stabs(labels, *a, **k):
            if isinstance(labels, (list, tuple)):
                labels = [translate(x) if isinstance(x, str) else x for x in labels]
            return _otabs(labels, *a, **k)
        st.tabs = _stabs

    for name in ("dataframe", "table", "data_editor"):
        orig = getattr(st, name, None)
        if orig:
            def _sdfw(data=None, *a, _o=orig, **k):
                return _o(data, *a, **_df_cfg(data, k))
            setattr(st, name, _sdfw)


_install_patches()


def language_selector():
    """Sidebar language picker; stores the code in session_state['lang']."""
    labels = list(LANGUAGES.keys())
    codes = list(LANGUAGES.values())
    cur = current_lang()
    idx = codes.index(cur) if cur in codes else 0
    choice = st.sidebar.selectbox("🌐 Language / Idioma / 언어", labels, index=idx)
    st.session_state["lang"] = LANGUAGES[choice]
