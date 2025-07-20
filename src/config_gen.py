"""Utilities for generating dictionary based configuration sets.

The module provides a tiny framework for defining *configuration sets*.  A
configuration set yields pairs of ``(name, config_dict)`` when iterated.  This
allows configuration dictionaries to be patched and combined while keeping
track of the name describing each variation.

Typical usage::

    import config_gen as cgen

    base = cgen.Single("base", {"a": 1})
    cfgs = base.patch(x={"a": 2}) | base.patch(y={"a": 3})
    for name, cfg in cfgs:
        print(name, cfg)

You can control the separator inserted between names during patching with
``set_name_separator``.
"""

from abc import abstractmethod
import copy
from typing import Iterable
from dataclasses import dataclass


_name_separator = "__"


@dataclass
class Replace:
    """Wrapper used to indicate full replacement during :func:`deep_merge`."""

    data: dict


def set_name_separator(sep: str):
    """Change the separator used when generating new configuration names."""

    global _name_separator
    _name_separator = sep


def deep_merge(a, b):
    """Recursively merge ``b`` into ``a`` returning a new dictionary."""

    if isinstance(a, dict) and isinstance(b, dict):
        out = copy.deepcopy(a)
        for k, v in b.items():
            out[k] = deep_merge(out.get(k), v)
        return out
    if isinstance(b, Replace):
        b = b.data
    return copy.deepcopy(b)


class ConfigSet:
    """Base class representing an iterable collection of configurations."""

    @abstractmethod
    def __iter__(self) -> Iterable[tuple[str, dict]]:
        """Yield ``(name, config)`` pairs for each configuration."""

        raise NotImplementedError()

    def __or__(self, other: "ConfigSet") -> "Union":
        """Return a :class:`Union` of ``self`` and ``other``."""

        return Union(self, other)

    def patch(self, **patches: dict) -> "Patch":
        """Return a :class:`Patch` with the provided ``patches`` applied."""

        return Patch(self, patches)


class Single(ConfigSet):
    """A configuration set that yields a single (name, config) pair."""

    def __init__(self, name: str, cfg: dict):
        """Create a new ``Single`` configuration set."""

        self.name = name
        self.cfg = cfg

    def __iter__(self) -> Iterable[tuple[str, dict]]:
        """Yield the contained name and configuration."""

        yield (self.name, self.cfg)


class Union(ConfigSet):
    """A configuration set produced by combining multiple sets."""

    def __init__(self, *others):
        """Create a union of ``others`` configuration sets."""

        self.others = list(others)

    def __iter__(self) -> Iterable[tuple[str, dict]]:
        """Yield configurations from each contained set in order."""

        for cfg_set in self.others:
            yield from cfg_set


class Patch(ConfigSet):
    """Apply one or more patches to each configuration in ``base``."""

    def __init__(self, base: ConfigSet, patches: dict[str, dict]):
        """Create a patched configuration set."""

        self.base = base
        self.patches = patches

    def __iter__(self) -> Iterable[tuple[str, dict]]:
        """Yield patched configurations for every name in ``base``."""

        for nm, cfg in self.base:
            for p_name, d in self.patches.items():
                if nm == "":
                    new_name = p_name
                else:
                    new_name = f"{nm}{_name_separator}{p_name}"
                yield new_name, deep_merge(cfg, d)
