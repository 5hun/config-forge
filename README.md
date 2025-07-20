# config_gen

A tiny library for generating sets of configuration dictionaries.  It lets you
patch existing configurations and automatically assigns descriptive names to each
variant.

## Installation

```bash
pip install config-gen
```

## Quick example

```python
import config_gen as cgen

cgen.set_name_separator("__")

base = cgen.Single("hoge", {"a": 10, "b": {"c": 20, "d": 30}, "c": "hogehoge"})

cfgs = (
    base.patch(**{f"b_c_{i}": {"b": {"c": i}} for i in range(3)})
        .patch(**{f"c_{s}": {"c": s} for s in ["x", "y"]})
    | base.patch(**{f"c_{s}": {"c": s} for s in ["piyo", "fuga"]})
    | base.patch(aaa={"b": cgen.Replace({"x": 30})})
)

for name, cfg in cfgs:
    print(name, cfg)
```

Example output:

```
hoge__b_c_0__c_x {'a': 10, 'b': {'c': 0, 'd': 30}, 'c': 'x'}
hoge__b_c_0__c_y {'a': 10, 'b': {'c': 0, 'd': 30}, 'c': 'y'}
...
```

Use `set_name_separator()` to change how names are joined when patches are
applied.
