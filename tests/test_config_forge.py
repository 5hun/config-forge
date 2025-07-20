import pytest

import config_forge as cgen


@pytest.fixture(autouse=True)
def reset_separator():
    yield
    cgen.set_name_separator("__")


def test_deep_merge_basic():
    a = {"a": 1, "b": {"c": 2}}
    b = {"a": 2, "b": {"d": 3}}
    res = cgen.deep_merge(a, b)
    assert res == {"a": 2, "b": {"c": 2, "d": 3}}


def test_deep_merge_replace():
    a = {"a": 1, "b": {"c": 2}}
    b = {"b": cgen.Replace({"x": 5})}
    res = cgen.deep_merge(a, b)
    assert res == {"a": 1, "b": {"x": 5}}


def test_deep_merge_remove():
    a = {"a": 1, "b": {"c": 2, "d": 3}}
    b = {"a": cgen.Remove(), "b": {"c": cgen.Remove()}}
    res = cgen.deep_merge(a, b)
    assert res == {"b": {"d": 3}}


def test_patch_and_union():
    base = cgen.Single("base", {"a": 1})
    cfg = base.patch(first={"a": 2}) | base.patch(second={"a": 3})
    result = list(cfg)
    assert result == [
        ("base__first", {"a": 2}),
        ("base__second", {"a": 3}),
    ]


def test_patch_chain():
    base = cgen.Single("base", {"a": 1})
    cfg = base.patch(p1={"a": 2}).patch(p2={"b": 3})
    result = list(cfg)
    assert result == [("base__p1__p2", {"a": 2, "b": 3})]


def test_set_name_separator():
    cgen.set_name_separator("::")
    base = cgen.Single("b", {"x": 1})
    patched = base.patch(p={"x": 2})
    assert list(patched) == [("b::p", {"x": 2})]


def test_name_separator_context():
    base = cgen.Single("b", {"x": 1})
    with cgen.name_separator("::"):
        assert list(base.patch(p={})) == [("b::p", {"x": 1})]
    assert list(base.patch(p={})) == [("b__p", {"x": 1})]


def test_name_separator_context_restores_previous():
    cgen.set_name_separator("++")
    base = cgen.Single("b", {"x": 1})
    with cgen.name_separator("::"):
        assert list(base.patch(p={})) == [("b::p", {"x": 1})]
    assert list(base.patch(p={})) == [("b++p", {"x": 1})]


def test_len_single():
    cfg = cgen.Single("nm", {})
    assert len(cfg) == 1


def test_len_patch_and_union():
    base = cgen.Single("b", {})
    p1 = base.patch(p1={}, p2={})
    p2 = base.patch(q1={})
    union = p1 | p2
    assert len(p1) == 2
    assert len(union) == 3


def test_len_patch_chain():
    base = cgen.Single("b", {})
    patched = base.patch(p1={}, p2={}).patch(q1={}, q2={})
    assert len(patched) == 4


def test_patch_remove():
    base = cgen.Single("b", {"a": 1, "b": 2})
    patched = base.patch(rm={"a": cgen.Remove()})
    assert list(patched) == [("b__rm", {"b": 2})]


def test_map():
    base = cgen.Single("b", {"x": 1})
    patched = base.patch(p1={"x": 2}, p2={"x": 3})

    def func(nm, cfg):
        return nm.upper(), {"x": cfg["x"] * 2}

    mapped = patched.map(func)
    assert list(mapped) == [
        ("B__P1", {"x": 4}),
        ("B__P2", {"x": 6}),
    ]
    assert len(mapped) == 2


def test_filter():
    base = cgen.Single("b", {"x": 0})
    patched = base.patch(**{f"v{i}": {"x": i} for i in range(3)})

    filtered = patched.filter(lambda n, c: c["x"] % 2 == 0)
    assert list(filtered) == [
        ("b__v0", {"x": 0}),
        ("b__v2", {"x": 2}),
    ]
    assert len(filtered) == 2
