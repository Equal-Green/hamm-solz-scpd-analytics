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
    "page.compliance": {"en": "Agreement & Compliance",
                        "es": "Contrato y cumplimiento", "ko": "계약 · 이행률"},
    "nav.agreement": {"en": "Agreement", "es": "Contrato", "ko": "계약"},
    # --- compliance page ---
    "comp.subtitle": {
        "en": "The signed consultancy agreement, scored against what has "
              "actually been delivered.",
        "es": "El contrato de consultoría firmado, evaluado frente a lo "
              "realmente entregado.",
        "ko": "체결된 컨설팅 계약과 실제 이행 실적 대비 평가."},
    "comp.contract_day": {"en": "Contract day", "es": "Día del contrato",
                          "ko": "계약 경과일"},
    "comp.days_remaining": {"en": "Days remaining", "es": "Días restantes",
                            "ko": "잔여 일수"},
    "comp.term_ends": {"en": "Term ends", "es": "Fin del plazo",
                       "ko": "계약 종료일"},
    "comp.contract_amount": {"en": "Contract amount", "es": "Monto del contrato",
                             "ko": "계약 금액"},
    "comp.gauge_title": {"en": "Compliance against obligations due to date",
                         "es": "Cumplimiento de las obligaciones vencidas",
                         "ko": "현재까지 도래한 의무 이행률"},
    "comp.gauge_caption": {
        "en": "Weighted across the Annex 2 deliverables that are ongoing or "
              "already due. The black needle marks how much of the 90-day term "
              "has elapsed — delivery should keep pace with it.",
        "es": "Ponderado sobre los entregables del Anexo 2 en curso o ya "
              "vencidos. La aguja negra marca el avance del plazo de 90 días; "
              "la entrega debería mantener ese ritmo.",
        "ko": "부속서 2의 진행 중이거나 이미 도래한 산출물에 대한 가중 평균입니다. "
              "검은 지침은 90일 기간의 경과율을 나타내며, 이행이 이를 따라가야 합니다."},
    "comp.overall": {"en": "Full-contract completion",
                     "es": "Avance total del contrato", "ko": "전체 계약 이행률"},
    "comp.term_elapsed": {"en": "Term elapsed", "es": "Plazo transcurrido",
                          "ko": "기간 경과율"},
    "comp.annex3": {"en": "Annex 3 material coverage",
                    "es": "Cobertura de materiales (Anexo 3)",
                    "ko": "부속서 3 자료 확보율"},
    "comp.reports_sent": {"en": "Bi-weekly reports logged",
                          "es": "Informes bisemanales registrados",
                          "ko": "격주 보고서 기록"},
    "comp.at_risk": {
        "en": "obligation(s) due and not fully met — each is either overdue or "
              "ongoing without complete evidence on file:",
        "es": "obligación(es) vencida(s) y no cumplida(s) por completo: cada "
              "una está atrasada o en curso sin evidencia completa archivada:",
        "ko": "건의 의무가 도래했으나 완전히 이행되지 않았습니다 — 각 항목은 기한이 "
              "지났거나 완전한 증빙 없이 진행 중입니다:"},
    "comp.on_track": {
        "en": "Every obligation due as of today is fully met with evidence on "
              "file.",
        "es": "Todas las obligaciones vencidas a la fecha están cumplidas con "
              "evidencia archivada.",
        "ko": "현재까지 도래한 모든 의무가 증빙과 함께 완전히 이행되었습니다."},
    "comp.unverified": {
        "en": "deliverable(s) carry a status that has not been checked against "
              "real artifacts yet. Record the actual status and an evidence "
              "pointer in the contract model so this score is defensible.",
        "es": "entregable(s) tienen un estado que aún no se ha verificado "
              "contra artefactos reales. Registre el estado real y una "
              "referencia de evidencia en el modelo del contrato para que esta "
              "puntuación sea defendible.",
        "ko": "건의 산출물 상태가 실제 결과물과 대조 검증되지 않았습니다. 이 점수가 "
              "방어 가능하도록 계약 모델에 실제 상태와 증빙 위치를 기록하십시오."},
    "comp.del_intro": {
        "en": "The six key deliverables from **Annex 2 §1**. Weights reflect "
              "contractual significance; the score counts an ongoing item at "
              "full value only when its evidence is complete.",
        "es": "Los seis entregables clave del **Anexo 2 §1**. Los pesos "
              "reflejan su relevancia contractual; un ítem en curso puntúa al "
              "100 % solo cuando su evidencia está completa.",
        "ko": "**부속서 2 §1**의 핵심 산출물 6건입니다. 가중치는 계약상 중요도를 "
              "반영하며, 진행 항목은 증빙이 완비된 경우에만 만점으로 계산됩니다."},
    "comp.no_evidence": {
        "en": "_No evidence recorded yet._",
        "es": "_Aún no hay evidencia registrada._",
        "ko": "_기록된 증빙이 없습니다._"},
    "comp.mat_intro": {
        "en": "**Annex 3** lists the materials THS may request through Circular "
              "EP. Coverage below is computed from the source archive actually "
              "received — not from a declaration.",
        "es": "El **Anexo 3** enumera los materiales que THS puede solicitar a "
              "través de Circular EP. La cobertura se calcula a partir del "
              "archivo realmente recibido, no de una declaración.",
        "ko": "**부속서 3**은 THS가 Circular EP를 통해 요청할 수 있는 자료 목록입니다. "
              "아래 확보율은 선언이 아니라 실제 수령한 원본 아카이브에서 산출됩니다."},
    "comp.deadline_notice": {
        "en": "CLOSING ON THE DEADLINE.",
        "es": "PLAZO A PUNTO DE VENCER.",
        "ko": "마감 임박."},
    "comp.day_of": {"en": "Day", "es": "Día", "ko": "경과일"},
    "comp.days_left": {"en": "days left", "es": "días restantes",
                       "ko": "일 남음"},
    "comp.days_away": {"en": "days away", "es": "días", "ko": "일 후"},
    "comp.tbc": {"en": "date to confirm", "es": "fecha por confirmar",
                 "ko": "날짜 미확정"},
    "comp.blocker": {"en": "BLOCKER", "es": "BLOQUEO", "ko": "차단 요인"},
    "comp.blk_evidence": {"en": "Evidence", "es": "Evidencia", "ko": "증빙"},
    "comp.blk_impact": {"en": "Impact", "es": "Impacto", "ko": "영향"},
    "comp.blk_action": {"en": "Action:", "es": "Acción:", "ko": "조치:"},
    "comp.blk_owner": {"en": "Owner", "es": "Responsable", "ko": "담당"},
    "comp.blk_intro": {
        "en": "Open blockers, most severe first. A blocker is something "
              "outside our own control that is holding a contractual "
              "deliverable short — each one names the evidence behind it, what "
              "it costs, and the action that clears it.",
        "es": "Bloqueos abiertos, del más grave al menos grave. Un bloqueo es "
              "algo fuera de nuestro control que impide completar un "
              "entregable contractual; cada uno indica su evidencia, su costo "
              "y la acción que lo resuelve.",
        "ko": "미해결 차단 요인을 심각도 순으로 정리했습니다. 차단 요인은 계약상 "
              "산출물의 완성을 막는 통제 밖 사안이며, 각 항목에 증빙·영향·해소 "
              "조치를 함께 기재했습니다."},
    "comp.no_blockers": {
        "en": "No open blockers. Every outstanding item is within our own "
              "control to complete.",
        "es": "No hay bloqueos abiertos. Todo lo pendiente está dentro de "
              "nuestro control.",
        "ko": "미해결 차단 요인이 없습니다. 남은 항목은 모두 자체적으로 완료할 수 "
              "있습니다."},
    "Mr. Choe (THS) in Ecuador": {
        "es": "Sr. Choe (THS) en Ecuador", "ko": "최 대표(THS) 에콰도르 방문"},
    "Final bi-weekly progress report due": {
        "es": "Vence el último informe bisemanal",
        "ko": "마지막 격주 보고서 마감"},
    "Term ends -- Final Handover Package due": {
        "es": "Fin del plazo — vence el paquete de entrega final",
        "ko": "계약 종료 — 최종 인계 패키지 마감"},
    "Choe in Ecuador": {"es": "Choe en Ecuador", "ko": "최 대표 에콰도르"},
    "Last report due": {"es": "Último informe", "ko": "마지막 보고서"},
    "Term ends": {"es": "Fin del plazo", "ko": "계약 종료"},
    "Hard dates": {"es": "Fechas firmes", "ko": "확정 일정"},
    "🚨 Blockers": {"es": "🚨 Bloqueos", "ko": "🚨 차단 요인"},
    "comp.items_received": {"en": "Items fully answered",
                            "es": "Ítems totalmente cubiertos",
                            "ko": "완전 충족 항목"},
    "comp.items_partial": {"en": "Partially answered",
                           "es": "Parcialmente cubiertos", "ko": "부분 충족"},
    "comp.items_none": {"en": "Not delivered", "es": "No entregados",
                        "ko": "미수령"},
    "comp.items_caption": {
        "en": "Coverage is a reading of the delivered archive, confirmed by the "
              "Consultant in the tracking matrix. Partial items count as half "
              "toward the headline figure. Every category holds some material, "
              "so a category-level rollup overstates coverage — the item-level "
              "reading is the one to act on.",
        "es": "La cobertura es una lectura del archivo entregado, confirmada "
              "por el Consultor en la matriz de seguimiento. Los ítems "
              "parciales cuentan como medio en la cifra principal. Todas las "
              "categorías tienen algún material, por lo que un resumen por "
              "categoría sobreestima la cobertura; la lectura por ítem es la "
              "que debe usarse.",
        "ko": "확보율은 수령한 아카이브를 판독한 결과이며, 컨설턴트가 추적 "
              "매트릭스에서 확인합니다. 부분 항목은 대표 수치에서 0.5로 계산됩니다. "
              "모든 범주에 일부 자료가 있어 범주 단위 집계는 확보율을 과대 "
              "평가하므로, 항목 단위 판독을 기준으로 삼아야 합니다."},
    "comp.files": {"en": "files", "es": "archivos", "ko": "개 파일"},
    "comp.topic_folders": {"en": "topic folders", "es": "carpetas temáticas",
                           "ko": "개 주제 폴더"},
    "comp.mat_caption": {
        "en": "received from Circular EP and catalogued. Annex 3 coverage means "
              "a category has materials on hand — it does not warrant their "
              "completeness or quality (Annex 1 §4).",
        "es": "recibidos de Circular EP y catalogados. La cobertura del Anexo 3 "
              "indica que existen materiales; no garantiza su integridad ni "
              "calidad (Anexo 1 §4).",
        "ko": "Circular EP로부터 수령·목록화했습니다. 부속서 3 확보율은 자료 보유를 "
              "의미하며 완전성이나 품질을 보증하지 않습니다 (부속서 1 §4)."},
    "comp.scope_intro": {
        "en": "**Clause 3 and Annex 1 §4** put the following outside scope. "
              "Compliance here means these were *not* performed without a "
              "written THS request, a written estimate, and written approval.",
        "es": "La **Cláusula 3 y el Anexo 1 §4** excluyen lo siguiente del "
              "alcance. Cumplir significa *no* haberlo ejecutado sin "
              "solicitud, estimación y aprobación escritas de THS.",
        "ko": "**제3조 및 부속서 1 §4**는 다음을 범위에서 제외합니다. 이행이란 THS의 "
              "서면 요청·견적·승인 없이 해당 업무를 수행하지 *않았음*을 뜻합니다."},
    "comp.scope_note": {
        "en": "Annex 1 §5: where Circular EP does not possess, collect, or "
              "disclose material within the 90-day term, that is not "
              "non-performance by the Consultant provided reasonable efforts "
              "and follow-up are documented. Documented follow-up is therefore "
              "the protection — which is what the tracking matrix and "
              "bi-weekly reports exist to prove.",
        "es": "Anexo 1 §5: si Circular EP no posee, recopila ni divulga "
              "material dentro de los 90 días, no constituye incumplimiento "
              "del Consultor siempre que se documenten esfuerzos razonables y "
              "seguimiento. El seguimiento documentado es la protección: para "
              "eso existen la matriz de seguimiento y los informes bisemanales.",
        "ko": "부속서 1 §5: Circular EP가 90일 내에 자료를 보유·수집·제공하지 않는 "
              "경우, 합리적 노력과 후속조치가 문서화되어 있다면 컨설턴트의 불이행이 "
              "아닙니다. 따라서 문서화된 후속조치가 방어 근거이며, 추적 매트릭스와 "
              "격주 보고서가 이를 입증합니다."},
    "comp.terms_note": {
        "en": "Annex 4 is a Spanish summary provided for local coordination "
              "convenience only — the English Agreement and Annexes prevail. "
              "Source of truth, signed:",
        "es": "El Anexo 4 es un resumen en español solo para conveniencia de "
              "coordinación local; prevalecen el Acuerdo y los Anexos en "
              "inglés. Fuente de verdad, firmada:",
        "ko": "부속서 4는 현지 조율 편의를 위한 스페인어 요약이며, 영문 계약서와 "
              "부속서가 우선합니다. 서명된 원본 근거:"},
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
    """Resolve a key to its ENGLISH source text. All translation happens in
    translate() via Google Translate, so this only un-maps id-style keys
    (e.g. 'page.overview' -> 'Overview'); plain English keys pass through."""
    entry = TR.get(key)
    if entry:
        return entry.get(_DEFAULT) or key
    return key


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


def tr(s):
    """Public alias for translate() — for surfaces Streamlit doesn't auto-patch
    (st.Page titles, st.navigation group labels, text baked into HTML)."""
    return translate(s)


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
    # 2. Google Translate — the single translation engine, then cache it
    if _GT is not None:
        try:
            out = _GT(source="en", target=lang).translate(s) or s
            bucket[s] = out
            _save_cache()
            return out
        except Exception:  # noqa: BLE001
            pass
    if _RECORD:
        _MISSING.add(s)
    return s


def _translate_fig(fig):
    """Translate the text inside a Plotly figure (title, axis titles, legend,
    colorbar, annotations, trace names) — st.plotly_chart isn't text-patched."""
    try:
        lay = fig.layout
        if lay.title and lay.title.text:
            lay.title.text = translate(lay.title.text)
        for ax in ("xaxis", "yaxis", "xaxis2", "yaxis2", "xaxis3", "yaxis3"):
            a = getattr(lay, ax, None)
            if a is not None and a.title and a.title.text:
                a.title.text = translate(a.title.text)
        try:
            if lay.legend and lay.legend.title and lay.legend.title.text:
                lay.legend.title.text = translate(lay.legend.title.text)
        except Exception:  # noqa: BLE001
            pass
        try:
            cb = lay.coloraxis.colorbar
            if cb and cb.title and cb.title.text:
                cb.title.text = translate(cb.title.text)
        except Exception:  # noqa: BLE001
            pass
        for ann in (lay.annotations or []):
            if getattr(ann, "text", None):
                ann.text = translate(ann.text)
        for trace in fig.data:
            if getattr(trace, "name", None):
                trace.name = translate(trace.name)
    except Exception:  # noqa: BLE001 — never break rendering
        pass
    return fig


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

    # plotly_chart: translate the text baked into the figure object
    _dgpc = getattr(_DG, "plotly_chart", None)
    if _dgpc:
        def _dgpcw(self, figure_or_data=None, *a, _o=_dgpc, **k):
            return _o(self, _translate_fig(figure_or_data) if figure_or_data
                      is not None else figure_or_data, *a, **k)
        setattr(_DG, "plotly_chart", _dgpcw)

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

    _stpc = getattr(st, "plotly_chart", None)
    if _stpc:
        def _stpcw(figure_or_data=None, *a, _o=_stpc, **k):
            return _o(_translate_fig(figure_or_data) if figure_or_data
                      is not None else figure_or_data, *a, **k)
        st.plotly_chart = _stpcw


_install_patches()


def language_selector():
    """Sidebar language picker; stores the code in session_state['lang']."""
    labels = list(LANGUAGES.keys())
    codes = list(LANGUAGES.values())
    cur = current_lang()
    idx = codes.index(cur) if cur in codes else 0
    choice = st.sidebar.selectbox("🌐 Language / Idioma / 언어", labels, index=idx)
    st.session_state["lang"] = LANGUAGES[choice]
