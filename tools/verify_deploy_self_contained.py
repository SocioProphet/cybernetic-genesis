#!/usr/bin/env python3
"""INV-DEP-10 for the Inception deploy overlay, kubectl-free: every SA/ConfigMap/PVC the
Deployment names must be defined under deploy/ (base or base-support). A dangling ref would
FailedCreate on apply (the exact bug this discipline exists to catch). Fail-closed."""
from __future__ import annotations
import sys
from pathlib import Path
import yaml
ROOT = Path(__file__).resolve().parents[1]

def _load_all(p): return [d for d in yaml.safe_load_all(p.read_text()) if isinstance(d, dict)]

def main() -> int:
    defined = {"ServiceAccount": set(), "ConfigMap": set(), "PersistentVolumeClaim": set()}
    for f in (ROOT / "deploy").rglob("*.yaml"):
        if f.name == "kustomization.yaml": continue
        for d in _load_all(f):
            if d.get("kind") in defined:
                defined[d["kind"]].add(d["metadata"]["name"])
    dep = [d for f in (ROOT/"deploy/base").glob("*.yaml") for d in _load_all(f) if d.get("kind")=="Deployment"][0]
    spec = dep["spec"]["template"]["spec"]
    problems = []
    sa = spec.get("serviceAccountName")
    if sa and sa not in defined["ServiceAccount"]:
        problems.append(f"serviceAccountName {sa!r} not rendered in deploy/")
    for c in spec.get("containers", []):
        for ef in c.get("envFrom", []):
            n = (ef.get("configMapRef") or {}).get("name")
            if n and n not in defined["ConfigMap"]:
                problems.append(f"ConfigMap {n!r} not rendered in deploy/")
    for v in spec.get("volumes", []):
        n = (v.get("persistentVolumeClaim") or {}).get("claimName")
        if n and n not in defined["PersistentVolumeClaim"]:
            problems.append(f"PVC {n!r} not rendered in deploy/")
    if problems:
        print("deploy self-containment FAILED (INV-DEP-10):", file=sys.stderr)
        for p in problems: print(f"  - {p}", file=sys.stderr)
        return 1
    print("OK: the Inception deploy overlay is self-contained (SA/ConfigMap/PVC all defined).")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
