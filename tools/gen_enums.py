#!/usr/bin/env python3
"""Generate the Governance/TruthClass enum $defs in common.schema.json FROM the canonical source.

Kills the pin duplication for real: `vendor/semantic_serdes_canonical_enums.yaml` is the single
source; this writes the enum values into common.schema.json's $defs. `--check` (CI) regenerates in
memory and fails if the committed schema is out of sync — so the $defs can never silently drift
AND are never hand-edited. Run without --check to update after refreshing the vendored file.
"""
from __future__ import annotations
import argparse, json, sys
from pathlib import Path
import yaml
ROOT = Path(__file__).resolve().parents[1]
COMMON = ROOT / "schemas/common.schema.json"
CANON = ROOT / "vendor/semantic_serdes_canonical_enums.yaml"

def _apply(common: dict, canon: dict) -> dict:
    g = common["$defs"]["Governance"]["properties"]
    g["admissibility_tier"]["enum"] = list(canon["admissibility_tier"])
    g["review_status"]["enum"] = list(canon["review_status"])
    common["$defs"]["TruthClass"]["enum"] = list(canon["truth_class"])
    return common

def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--check", action="store_true", help="fail if the committed $defs are out of sync")
    args = ap.parse_args(argv)
    canon = yaml.safe_load(CANON.read_text())
    common = json.loads(COMMON.read_text())
    updated = _apply(json.loads(json.dumps(common)), canon)
    if args.check:
        if updated != common:
            print("gen_enums --check FAILED: common.schema.json enums are out of sync with the canonical "
                  "source; run `python tools/gen_enums.py` and commit.", file=sys.stderr)
            return 1
        print("OK: Governance/TruthClass $defs are in sync with vendor/semantic_serdes_canonical_enums.yaml.")
        return 0
    COMMON.write_text(json.dumps(updated, indent=2) + "\n")
    print(f"generated Governance/TruthClass $defs from {CANON.name}")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
