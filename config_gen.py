from abc import abstractmethod
import copy
from typing import Iterable
from dataclasses import dataclass


_name_separator = "__"


@dataclass
class Replace:
    data: dict


def set_name_separator(sep: str):
    _name_separtor = sep


def deep_merge(a, b):
    if isinstance(a, dict) and isinstance(b, dict):
        out = copy.deepcopy(a)
        for k, v in b.items():
            out[k] = deep_merge(out.get(k), v)
        return out
    if isinstance(b, Replace):
        b = b.data
    return copy.deepcopy(b)


class ConfigSet:
    @abstractmethod
    def __iter__(self) -> Iterable[tuple[str, dict]]:
        raise NotImplementedError()

    def __or__(self, other: "ConfigSet") -> "Union":
        return Union(self, other)

    def patch(self, **patches: dict) -> "Patch":
        return Patch(self, patches)


class Single(ConfigSet):
    def __init__(self, name: str, cfg: dict):
        self.name = name
        self.cfg = cfg

    def __iter__(self) -> Iterable[tuple[str, dict]]:
        yield (self.name, self.cfg)


class Union(ConfigSet):
    def __init__(self, *others):
        self.others = list(others)

    def __iter__(self) -> Iterable[tuple[str, dict]]:
        for cfg_set in self.others:
            yield from cfg_set


class Patch(ConfigSet):
    def __init__(self, base: ConfigSet, patches: dict[str, dict]):
        self.base = base
        self.patches = patches

    def __iter__(self) -> Iterable[tuple[str, dict]]:
        for nm, cfg in self.base:
            for p_name, d in self.patches.items():
                if nm == "":
                    new_name = p_name
                else:
                    new_name = f"{nm}{_name_separator}{p_name}"
                yield new_name, deep_merge(cfg, d)
