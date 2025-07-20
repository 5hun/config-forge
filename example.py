import config_forge as cforge

cforge.set_name_separator("__")

cfg = cforge.Single("hoge", {"a": 10, "b": {"c": 20, "d": 30}, "c": "hogehoge"})

cfg = (
    cfg.patch(**{f"b_c_{i}": {"b": {"c": i}} for i in range(0, 10)}).patch(
        **{f"c_{s}": {"c": s} for s in ["x", "y", "z"]}
    )
    | cfg.patch(**{f"c_{s}": {"c": s} for s in ["piyo", "fuga"]})
    | cfg.patch(aaa={"b": cforge.Replace({"x": 30})})
)

for nm, d in cfg:
    print(nm, d)
