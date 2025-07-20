# config-forge

Utilities for generating dictionary based configuration sets. A configuration set is iterable and yields `(name, config_dict)` pairs. You can patch existing sets and combine them while the library manages name composition.

## Installation

```bash
pip install config-forge
```

## Quick example

```python
import config_forge as cforge

# optionally change the separator used for generated names
cforge.set_name_separator("__")

base = cforge.Single("foo", {"a": 10, "b": {"c": 20, "d": 30}, "c": "qux"})

cfgs = (
    base.patch(**{f"b_c_{i}": {"b": {"c": i}} for i in range(0, 10)}).patch(
        **{f"c_{s}": {"c": s} for s in ["x", "y", "z"]}
    )
    | base.patch(**{f"c_{s}": {"c": s} for s in ["bar", "baz"]})
    | base.patch(aaa={"b": cforge.Replace({"x": 30})})
)


for name, cfg in cfgs:
    print(name, cfg)
```

The above script prints names composed from each patch along with the resulting dictionaries. The output begins like this:

```
foo__b_c_0__c_x {'a': 10, 'b': {'c': 0, 'd': 30}, 'c': 'x'}
foo__b_c_0__c_y {'a': 10, 'b': {'c': 0, 'd': 30}, 'c': 'y'}
foo__b_c_0__c_z {'a': 10, 'b': {'c': 0, 'd': 30}, 'c': 'z'}
foo__b_c_1__c_x {'a': 10, 'b': {'c': 1, 'd': 30}, 'c': 'x'}
foo__b_c_1__c_y {'a': 10, 'b': {'c': 1, 'd': 30}, 'c': 'y'}
...
foo__c_baz {'a': 10, 'b': {'c': 20, 'd': 30}, 'c': 'baz'}
foo__aaa {'a': 10, 'b': {'x': 30}, 'c': 'qux'}
```

## Concepts

- **Single** – wrap a single base configuration.
- **Patch** – apply dictionary patches to each configuration in a set.
- **Union** – combine multiple configuration sets into one.
- **Replace** – fully replace a sub-dictionary when merging.

See `examples/example.py` for a full demonstration.

## License

This project is licensed under the MIT License.
