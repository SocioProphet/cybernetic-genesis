"""The rename must be real, and it must not be self-granted where it buys passage."""
import pytest

from initiation import InitiationError, check


def _r(**over):
    r = {"subject": "identity:hoshea", "prior_name": "hoshea", "new_name": "yehoshua",
         "operation": "insert", "letter": "yod", "script": "hebrew"}
    r.update(over)
    return r


CROSSING = {"enables_threshold": "crossing:jordan", "attestor": "identity:moses",
            "attestor_authority_chain": ["identity:moses", "authority:sinai"]}


def test_moses_adds_the_yod_and_joshua_crosses():
    """Num 13:16. The one who fell short performs the rename that lets another cross."""
    check(_r(**CROSSING))


def test_a_raiser_brought_forth_from_the_subject_is_allowed():
    """Sophia's raiser is her son. Origin may descend from the subject — that is not the defect."""
    check(_r(**{**CROSSING, "attestor": "identity:michael",
                "attestor_origin": "identity:hoshea",
                "attestor_authority_chain": ["identity:michael", "authority:above"]}))


def test_a_raiser_whose_AUTHORITY_derives_from_the_subject_is_refused():
    """The sybil hole: mint a derived identity, have it attest for you. Distinct identity is not
    independence — authority must be sent from above, not received from the one being raised."""
    with pytest.raises(InitiationError, match="wearing another name"):
        check(_r(**{**CROSSING, "attestor": "identity:puppet",
                    "attestor_authority_chain": ["identity:puppet", "identity:hoshea"]}))


def test_an_unstated_authority_chain_is_refused_where_a_crossing_is_at_stake():
    """Unknown provenance of authority is not evidence of independence."""
    with pytest.raises(InitiationError, match="not independence"):
        check(_r(enables_threshold="crossing:jordan", attestor="identity:moses"))


def test_abram_to_abraham_is_an_insert():
    check(_r(subject="identity:abram", prior_name="abram", new_name="abraham",
             operation="insert", letter="heh"))


def test_sarai_to_sarah_is_a_swap_of_equal_length():
    check(_r(subject="identity:sarai", prior_name="sarai", new_name="sarah",
             operation="swap", letter="heh"))


def test_yhvh_to_yhshvh_is_the_shin_set_into_the_name():
    """The braid's five phases are themselves a name that underwent this operation."""
    check(_r(subject="identity:name", prior_name="yhvh", new_name="yhshvh",
             operation="insert", letter="shin"))


def test_you_cannot_rename_yourself_across_a_threshold():
    with pytest.raises(InitiationError, match="cannot rename yourself"):
        check(_r(enables_threshold="crossing:jordan"))


def test_self_attestation_is_not_a_plus_one():
    with pytest.raises(InitiationError, match="not a \\+1"):
        check(_r(enables_threshold="crossing:jordan", attestor="identity:hoshea",
                 attestor_authority_chain=["identity:hoshea"]))


def test_a_name_may_be_self_chosen_when_no_crossing_is_at_stake():
    check(_r(attestor=None))          # no enables_threshold -> no attestor demanded


def test_a_rename_that_renames_nothing_is_refused():
    with pytest.raises(InitiationError, match="unchanged"):
        check(_r(prior_name="hoshea", new_name="Hoshea"))


def test_insert_must_actually_grow_the_name():
    with pytest.raises(InitiationError, match="did not grow"):
        check(_r(prior_name="yehoshua", new_name="hoshea", operation="insert"))


def test_swap_must_not_change_the_length():
    with pytest.raises(InitiationError, match="length changed"):
        check(_r(prior_name="abram", new_name="abraham", operation="swap"))


def test_drop_must_actually_shrink_the_name():
    with pytest.raises(InitiationError, match="did not shrink"):
        check(_r(prior_name="abram", new_name="abraham", operation="drop"))


def test_adam_to_admn_is_the_estate_case():
    """ADMN = Adam-N. The naming space is itself produced by this operation."""
    check(_r(subject="identity:adam", prior_name="adam", new_name="admn",
             operation="swap", letter="nun"))
