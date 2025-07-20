import config_forge as cforge

# optionally change the separator used for generated names
cforge.set_name_separator("__")

cfg = cforge.Single("foo", {"a": 10, "b": {"c": 20, "d": 30}, "c": "qux"})

cfgs = (
    cfg.patch(**{f"b_c_{i}": {"b": {"c": i}} for i in range(0, 10)}).patch(
        **{f"c_{s}": {"c": s} for s in ["x", "y", "z"]}
    )
    | cfg.patch(**{f"c_{s}": {"c": s} for s in ["bar", "baz"]})
    | cfg.patch(aaa={"b": cforge.Replace({"x": 30})})
)

for nm, cfg in cfgs:
    print(nm, cfg)
