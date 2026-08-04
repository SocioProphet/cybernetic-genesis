"""The registry must be honest, retrievable, and refuse to operationalise what it holds behind a boundary."""
import copy

import pytest

from legend_registry import check, load, local_anchor_problems, to_corpus, ROOT

REG = load()


def test_the_shipped_registry_holds():
    assert check(REG) == []
    assert local_anchor_problems(REG, "cybernetic-genesis", ROOT) == []


def test_every_entry_carries_both_retrieval_payloads():
    """RAG returns one field at a time, so each must stand alone."""
    for e in REG["entries"]:
        assert len(e["narrative"]) >= 80, e["id"]
        assert len(e["design_principle"]) >= 80, e["id"]


def test_a_boundary_entry_may_not_bind_a_mechanism():
    """The rule that makes restraint checkable rather than merely promised."""
    reg = copy.deepcopy(REG)
    bounded = next(e for e in reg["entries"] if any(s["kind"] == "boundary" for s in e["sources"]))
    assert bounded["mechanism"] is None, "the shipped entry must be unbound"
    bounded["mechanism"] = {"repo": "x", "path": "y", "invariant": "z"}
    problems = check(reg)
    assert any("referenced, not operationalised" in p for p in problems)


def test_the_black_hills_entry_is_the_bounded_one_and_stays_unbound():
    e = next(x for x in REG["entries"] if x["id"] == "black-hills-return")
    assert e["mechanism"] is None
    assert any(s["kind"] == "boundary" for s in e["sources"])


def test_gaps_are_recorded_not_silently_dropped():
    """An honest blank beats a plausible fabrication — so the blanks must survive in the data."""
    gaps = [(e["id"], s["citation"]) for e in REG["entries"] for s in e["sources"] if s["kind"] == "gap"]
    assert len(gaps) >= 5
    ids = {g[0] for g in gaps}
    assert {"bearfoot-uniformity", "tamanend-reception", "black-hills-return"} <= ids


def test_related_edges_all_resolve():
    ids = {e["id"] for e in REG["entries"]}
    for e in REG["entries"]:
        for rel in e["related"]:
            assert rel in ids, f"{e['id']} -> {rel}"


def test_a_dangling_related_edge_is_refused():
    reg = copy.deepcopy(REG)
    reg["entries"][0]["related"].append("no-such-legend")
    assert any("resolves to nothing" in p for p in check(reg))


def test_a_mechanism_without_an_invariant_is_refused():
    reg = copy.deepcopy(REG)
    m = next(e for e in reg["entries"] if e.get("mechanism"))
    m["mechanism"] = {"repo": "r", "path": "p"}
    assert any("a path is not a claim" in p for p in check(reg))


def test_an_unresolvable_anchor_is_refused():
    reg = copy.deepcopy(REG)
    reg["entries"][0]["anchors"] = [{"repo": "cybernetic-genesis", "doc": "docs/nope.md", "section": "x"}]
    assert any("does not exist" in p for p in local_anchor_problems(reg, "cybernetic-genesis", ROOT))


def test_unknown_source_kinds_are_refused():
    reg = copy.deepcopy(REG)
    reg["entries"][0]["sources"].append({"kind": "vibes", "citation": "trust me"})
    assert any("unknown source kind" in p for p in check(reg))


def test_the_corpus_renders_a_stable_section_per_entry():
    """The emitted corpus is the containment tree a structural retriever descends."""
    corpus = to_corpus(REG)
    for e in REG["entries"]:
        assert f"## {e['title']}" in corpus
        assert f"`id: {e['id']}`" in corpus
    assert corpus.count("### Narrative") == len(REG["entries"])
    assert corpus.count("### Design principle") == len(REG["entries"])


def test_an_unbound_entry_says_so_in_the_corpus():
    assert "**None, deliberately.** This entry is referenced and not operationalised." in to_corpus(REG)


def test_the_registry_spans_the_repos_it_claims():
    repos = {m["repo"] for e in REG["entries"] if (m := e.get("mechanism"))}
    assert {"cybernetic-genesis", "goose-notes", "bearbrowser", "prophet-platform"} <= repos
