#!/usr/bin/env python3
"""The legend registry — narrative and mechanism, kept honest and kept retrievable.

`registry/legends.v1.json` is the estate's narrative -> mechanism map. It exists for two reasons,
and the second is the one that makes it a checker rather than a document.

**1. Retrieval.** Each entry carries a `narrative` (the explained story) and a `design_principle`
(the philosophy it yields) as SEPARATE fields, plus page-anchored doc locations and typed `related`
edges. That is the fibered shape applied to our own corpus: the per-repo docs are containment trees
(the vertical, `E^⊑`), and `related` supplies the cross-document relational edges (`E_R`) that no
single document can express. A question like "why is the carry uncapped" should return the
principle; "what is the goose" should return the narrative; neither should require reading a repo.

**2. Honesty, enforced.** Sources are TYPED, and two of the types carry obligations that are
checked here rather than trusted:

    gap       searched for and NOT found. Recorded so the absence survives, because an honest blank
              beats a plausible fabrication -- and because the next person can fill it properly.
    boundary  a limit deliberately observed. AN ENTRY CARRYING A `boundary` SOURCE MUST BIND TO NO
              MECHANISM. Some material is referenced and not operationalised; for those the correct
              implementation is to implement nothing, and that is checkable rather than merely
              promised.

That last rule is the point. It lets the registry hold an entry whose right answer is restraint,
and it refuses the drift where a boundary quietly grows an implementation later.

stdlib only.
"""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "registry/legends.v1.json"

SOURCE_KINDS = {"attested", "tradition", "interpretation", "public-general", "gap", "boundary"}
REQUIRED_FIELDS = ("id", "title", "narrative", "design_principle", "sources", "anchors", "related")


class RegistryError(ValueError):
    """The registry is the map. A wrong map is worse than none."""


def load(path: Path | None = None) -> dict:
    return json.loads((path or REGISTRY).read_text())


def check(reg: dict) -> list[str]:
    """Returns a list of problems; empty means the registry holds."""
    problems: list[str] = []
    entries = reg.get("entries") or []
    ids = [e.get("id") for e in entries]

    if len(set(ids)) != len(ids):
        dupes = sorted({i for i in ids if ids.count(i) > 1})
        problems.append(f"duplicate entry ids: {dupes}")

    for e in entries:
        eid = e.get("id", "<no id>")

        for field in REQUIRED_FIELDS:
            if not e.get(field):
                problems.append(f"{eid}: missing required field {field!r}")

        # the two retrieval payloads must actually say something
        for field in ("narrative", "design_principle"):
            if len(str(e.get(field) or "")) < 80:
                problems.append(
                    f"{eid}: {field} is too thin to answer a question with — retrieval returns this "
                    "field alone, so it has to stand on its own")

        kinds = set()
        for s in e.get("sources") or []:
            kind = s.get("kind")
            kinds.add(kind)
            if kind not in SOURCE_KINDS:
                problems.append(f"{eid}: unknown source kind {kind!r}; expected one of {sorted(SOURCE_KINDS)}")
            if not s.get("citation"):
                problems.append(f"{eid}: a source has no citation")

        # THE BOUNDARY RULE: referenced, not operationalised.
        if "boundary" in kinds and e.get("mechanism"):
            problems.append(
                f"{eid}: carries a `boundary` source but binds to a mechanism "
                f"({e['mechanism'].get('repo')}/{e['mechanism'].get('path')}) — material held behind a "
                "boundary is referenced, not operationalised, and the correct implementation is to "
                "implement nothing")

        # an entry that claims a mechanism must say what it enforces
        mech = e.get("mechanism")
        if mech and not mech.get("invariant"):
            problems.append(f"{eid}: mechanism names a path but no invariant — a path is not a claim")

        for rel in e.get("related") or []:
            if rel not in ids:
                problems.append(f"{eid}: related edge {rel!r} resolves to nothing")

        for a in e.get("anchors") or []:
            if not a.get("repo") or not a.get("doc") or not a.get("section"):
                problems.append(f"{eid}: an anchor is missing repo/doc/section — an unanchored entry "
                                "cannot be cited back to a location")

    return problems


def local_anchor_problems(reg: dict, repo: str, repo_root: Path) -> list[str]:
    """Anchor totality, for the one repo we can see from here: the doc must exist and contain the
    section heading. An anchor that does not resolve is provenance-of-location that lies."""
    problems = []
    for e in reg.get("entries") or []:
        for a in e.get("anchors") or []:
            if a.get("repo") != repo:
                continue
            doc = repo_root / a["doc"]
            if not doc.exists():
                problems.append(f"{e['id']}: anchor doc {a['doc']} does not exist in {repo}")
            elif a["section"] not in doc.read_text():
                problems.append(f"{e['id']}: anchor section {a['section']!r} not found in {a['doc']}")
    return problems


def to_corpus(reg: dict) -> str:
    """Render the registry as a stable, section-anchored markdown corpus — the containment tree a
    structural retriever descends. Headings are the anchors; do not reorder them casually."""
    out = ["# Legend registry — narrative, principle, mechanism", "",
           reg.get("description", ""), "",
           "*Generated from `registry/legends.v1.json` by `tools/legend_registry.py --emit`. Do not "
           "hand-edit; edit the registry.*", ""]
    for e in reg["entries"]:
        out += [f"## {e['title']}", "", f"`id: {e['id']}`", "",
                "### Narrative", "", e["narrative"], "",
                "### Design principle", "", e["design_principle"], "",
                "### Sources", ""]
        for s in e["sources"]:
            url = f" — <{s['url']}>" if s.get("url") else ""
            out.append(f"- **{s['kind']}** — {s['citation']}{url}")
        out.append("")
        if e.get("mechanism"):
            m = e["mechanism"]
            out += ["### Mechanism", "", f"`{m['repo']}` → `{m['path']}`", "", f"> {m['invariant']}", ""]
        else:
            out += ["### Mechanism", "",
                    "**None, deliberately.** This entry is referenced and not operationalised.", ""]
        if e.get("related"):
            out += ["### Related", "", ", ".join(f"`{r}`" for r in e["related"]), ""]
    return "\n".join(out) + "\n"


def main(argv: list[str] | None = None) -> int:
    import argparse
    import sys
    ap = argparse.ArgumentParser(prog="legend_registry")
    ap.add_argument("--emit", action="store_true", help="render the retrieval corpus to stdout")
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args(argv)

    reg = load()
    if a.emit:
        sys.stdout.write(to_corpus(reg))
        return 0

    problems = check(reg) + local_anchor_problems(reg, "cybernetic-genesis", ROOT)
    if a.json:
        print(json.dumps({"ok": not problems, "problems": problems,
                          "entries": len(reg.get("entries", []))}, indent=2))
    else:
        for p in problems:
            print(f"  ✗ {p}", file=sys.stderr)
        n = len(reg.get("entries", []))
        gaps = sum(1 for e in reg["entries"] for s in e["sources"] if s["kind"] == "gap")
        bounded = sum(1 for e in reg["entries"] if any(s["kind"] == "boundary" for s in e["sources"]))
        print(f"legend registry: {n} entries, {gaps} recorded gap(s), {bounded} bounded (no mechanism)"
              + (f" — {len(problems)} PROBLEM(S)" if problems else " — holds"), file=sys.stderr)
    return 1 if problems else 0


if __name__ == "__main__":
    raise SystemExit(main())
