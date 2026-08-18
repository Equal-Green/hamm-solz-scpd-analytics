"""Seed i18n_cache.json with the curated ES/KO wording for the Agreement page.

translate() consults the on-disk cache before calling Google Translate, so the
cache -- not the TR dicts -- is what actually decides the displayed wording.
The Agreement & Compliance page paraphrases contract clauses, where machine
translation is a liability: Google rendered "score" as *partitura* (a musical
score) and "guardrails" as *barandillas* (handrails). This script promotes the
hand-written ES/KO in i18n.TR / i18n_pages.TR_PAGES into the cache.

Run it from the project root WITH THE APP STOPPED -- a live process holds the
cache in memory and _save_cache() would write its stale copy back over these
entries:

    .venv/bin/python dashboard/seed_i18n_cache.py
"""
import json
import os
import sys

_here = os.path.dirname(os.path.abspath(__file__))
if _here not in sys.path:
    sys.path.insert(0, _here)

from i18n import TR                                        # noqa: E402

CACHE_PATH = os.path.join(_here, "i18n_cache.json")

# English-keyed strings written inline on the Agreement page (section headers
# and tab labels). id-style "comp.*" keys are picked up automatically.
ENGLISH_KEYED = [
    "Contribution to the score",
    "Weighted points earned vs outstanding",
    "Minimum content and evidence",
    "Success indicators (Annex 2 §3)",
    "Implementation requirements (Annex 2 §2)",
    "Contract documents, in order of priority",
    "📋 Deliverables (Annex 2)",
    "📦 Materials received (Annex 3)",
    "✅ Indicators & implementation",
    "🚧 Scope guardrails",
    "Rollup by category",
    "📄 Agreement terms",
]


def keys():
    ided = [k for k in TR if k.startswith("comp.")]
    return ided + ["page.compliance", "nav.agreement"] + ENGLISH_KEYED


def main():
    with open(CACHE_PATH, encoding="utf-8") as f:
        cache = json.load(f)

    added = {"es": 0, "ko": 0}
    missing = []
    for key in keys():
        entry = TR.get(key)
        if not entry:
            missing.append(key)
            continue
        # id-style keys resolve to their English text; English-keyed entries
        # (from TR_PAGES) carry only es/ko, so the key *is* the source string.
        source = entry.get("en", key)
        for lang in ("es", "ko"):
            value = entry.get(lang)
            if value and cache.setdefault(lang, {}).get(source) != value:
                cache[lang][source] = value
                added[lang] += 1

    with open(CACHE_PATH, "w", encoding="utf-8") as f:
        json.dump(cache, f, ensure_ascii=False, indent=0)  # matches _save_cache

    print(f"seeded es={added['es']} ko={added['ko']} "
          f"across {len(keys())} keys")
    if missing:
        print("no TR entry for:", ", ".join(missing))


if __name__ == "__main__":
    main()
