#!/usr/bin/env python3
"""Enum drift guard: the Genesis governance/truth vocabulary MUST equal semantic-serdes'.

Kills the pin duplication the integration introduced: instead of three hand-copied enum lists
(common.schema.json $defs, the alignment gate's pins, and reality), this makes
`vendor/semantic_serdes_canonical_enums.yaml` the single source and fails closed if
common.schema.json's Governance/TruthClass $defs, or verify_semantic_serdes_alignment.py's
pinned sets, drift from it. Refresh the vendored file from semantic-serdes on change.
"""
from __future__ import annotations
import json, sys
from pathlib import Path
import yaml
ROOT = Path(__file__).resolve().parents[1]

def main() -> int:
    canon = yaml.safe_load((ROOT / "vendor/semantic_serdes_canonical_enums.yaml").read_text())
    common = json.loads((ROOT / "schemas/common.schema.json").read_text())["$defs"]
    problems = []
    gov = common["Governance"]["properties"]
    if set(gov["admissibility_tier"]["enum"]) != set(canon["admissibility_tier"]):
        problems.append("Governance.admissibility_tier drifted from canonical")
    if set(gov["review_status"]["enum"]) != set(canon["review_status"]):
        problems.append("Governance.review_status drifted from canonical")
    if set(common["TruthClass"]["enum"]) != set(canon["truth_class"]):
        problems.append("TruthClass drifted from canonical truth_class")
    # the alignment gate's pins must match too
    sys.path.insert(0, str(ROOT / "tools"))
    import verify_semantic_serdes_alignment as a
    if a.SS_ADMISSIBILITY_TIER != set(canon["admissibility_tier"]): problems.append("alignment pin admissibility_tier drift")
    if a.SS_REVIEW_STATUS != set(canon["review_status"]): problems.append("alignment pin review_status drift")
    if a.SS_TRUTH_CLASS != set(canon["truth_class"]): problems.append("alignment pin truth_class drift")
    if problems:
        print("enum-alignment FAILED (drift from semantic-serdes canonical):", file=sys.stderr)
        for p in problems: print(f"  - {p}", file=sys.stderr)
        return 1
    print("OK: Genesis governance/truth enums match semantic-serdes canonical (no drift).")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
