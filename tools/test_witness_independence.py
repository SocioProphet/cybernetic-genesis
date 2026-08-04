"""Two witnesses of different kind can still be one voice."""
import pytest

from witness_independence import WitnessError, check, check_artifact_record

H = "sha256:" + "ab12cd34" * 8


def w(name, kind, chain, **extra):
    return {"name": name, "role": f"{kind}-role", "type": kind, "hash": H,
            "authority_chain": list(chain), **extra}


CHART = w("atlas-signing-key", "chart", ["ca:release-root"])
METHOD = w("tile-validator", "method", ["ca:validation-root"])


def test_two_independent_witnesses_pass():
    check([CHART, METHOD], subject="twin:deploy/7c1")


def test_a_witness_authorised_by_the_subject_is_refused():
    """The artifact's own producing twin authorised its attestor — it witnesses itself."""
    captured = w("captured", "method", ["twin:deploy/7c1"])
    with pytest.raises(WitnessError, match="witnessing itself"):
        check([CHART, captured], subject="twin:deploy/7c1")


def test_a_witness_standing_behind_the_other_is_refused():
    """The deeper case: chart+method of different KIND, but one issued the other's authority."""
    derived = w("derived-validator", "method", ["atlas-signing-key"])
    with pytest.raises(WitnessError, match="one witness wearing two names"):
        check([CHART, derived], subject="twin:deploy/7c1")


def test_an_unstated_authority_chain_is_refused():
    bare = {"name": "anon", "role": "r", "type": "method", "hash": H}
    with pytest.raises(WitnessError, match="not independence"):
        check([CHART, bare], subject="twin:deploy/7c1")


def test_a_shared_distant_root_is_allowed():
    """Two attestations under one org root are still two attestations. Do not refuse real PKI."""
    a = w("signer", "chart", ["ca:team", "ca:org-root"])
    b = w("validator", "method", ["ca:qa", "ca:org-root"])
    check([a, b], subject="twin:deploy/7c1")


def test_one_witness_is_never_enough():
    with pytest.raises(WitnessError, match="two or three"):
        check([CHART], subject="twin:deploy/7c1")


def test_artifact_record_binds_the_subject_to_its_producing_twin():
    rec = {"produced_by_twin": "twin:deploy/7c1",
           "witnesses": [CHART, w("captured", "method", ["twin:deploy/7c1"])]}
    with pytest.raises(WitnessError, match="witnessing itself"):
        check_artifact_record(rec)


def test_independence_is_orthogonal_to_kind():
    """Both checks must hold: differing kind does NOT imply independence."""
    a = w("signer", "chart", ["ca:root"])
    b = w("validator", "method", ["signer"])
    assert a["type"] != b["type"], "different kinds — WitnessesDualType would pass this"
    with pytest.raises(WitnessError):
        check([a, b])
