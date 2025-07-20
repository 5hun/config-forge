import sys
from pathlib import Path
import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import config_gen as cgen

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
    assert result == [
        ("base__p1__p2", {"a": 2, "b": 3})
    ]


def test_set_name_separator():
    cgen.set_name_separator("::")
    base = cgen.Single("b", {"x": 1})
    patched = base.patch(p={"x": 2})
    assert list(patched) == [("b::p", {"x": 2})]

