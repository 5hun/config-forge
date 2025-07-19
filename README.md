# config_gen
Config Generator

```python
import config_gen as cgen

cfg = cgen.Single("hoge", {"a": 10, "b": {"c": 20, "d": 30}, "c": "hogehoge"})

cfg = (
    cfg.patch(**{f"b_c_{i}": {"b": {"c": i}} for i in range(0, 10)}).patch(
        **{f"c_{s}": {"c": s} for s in ["x", "y", "z"]}
    )
    | cfg.patch(**{f"c_{s}": {"c": s} for s in ["piyo", "fuga"]})
    | cfg.patch(aaa={"b": cgen.Replace({"x": 30})})
)

for nm, d in cfg.items():
    print(nm, d)

# Output:
# hoge__b_c_0__c_x {'a': 10, 'b': {'c': 0, 'd': 30}, 'c': 'x'}
# hoge__b_c_0__c_y {'a': 10, 'b': {'c': 0, 'd': 30}, 'c': 'y'}
# hoge__b_c_0__c_z {'a': 10, 'b': {'c': 0, 'd': 30}, 'c': 'z'}
# hoge__b_c_1__c_x {'a': 10, 'b': {'c': 1, 'd': 30}, 'c': 'x'}
# hoge__b_c_1__c_y {'a': 10, 'b': {'c': 1, 'd': 30}, 'c': 'y'}
# hoge__b_c_1__c_z {'a': 10, 'b': {'c': 1, 'd': 30}, 'c': 'z'}
# hoge__b_c_2__c_x {'a': 10, 'b': {'c': 2, 'd': 30}, 'c': 'x'}
# hoge__b_c_2__c_y {'a': 10, 'b': {'c': 2, 'd': 30}, 'c': 'y'}
# hoge__b_c_2__c_z {'a': 10, 'b': {'c': 2, 'd': 30}, 'c': 'z'}
# hoge__b_c_3__c_x {'a': 10, 'b': {'c': 3, 'd': 30}, 'c': 'x'}
# hoge__b_c_3__c_y {'a': 10, 'b': {'c': 3, 'd': 30}, 'c': 'y'}
# hoge__b_c_3__c_z {'a': 10, 'b': {'c': 3, 'd': 30}, 'c': 'z'}
# hoge__b_c_4__c_x {'a': 10, 'b': {'c': 4, 'd': 30}, 'c': 'x'}
# hoge__b_c_4__c_y {'a': 10, 'b': {'c': 4, 'd': 30}, 'c': 'y'}
# hoge__b_c_4__c_z {'a': 10, 'b': {'c': 4, 'd': 30}, 'c': 'z'}
# hoge__b_c_5__c_x {'a': 10, 'b': {'c': 5, 'd': 30}, 'c': 'x'}
# hoge__b_c_5__c_y {'a': 10, 'b': {'c': 5, 'd': 30}, 'c': 'y'}
# hoge__b_c_5__c_z {'a': 10, 'b': {'c': 5, 'd': 30}, 'c': 'z'}
# hoge__b_c_6__c_x {'a': 10, 'b': {'c': 6, 'd': 30}, 'c': 'x'}
# hoge__b_c_6__c_y {'a': 10, 'b': {'c': 6, 'd': 30}, 'c': 'y'}
# hoge__b_c_6__c_z {'a': 10, 'b': {'c': 6, 'd': 30}, 'c': 'z'}
# hoge__b_c_7__c_x {'a': 10, 'b': {'c': 7, 'd': 30}, 'c': 'x'}
# hoge__b_c_7__c_y {'a': 10, 'b': {'c': 7, 'd': 30}, 'c': 'y'}
# hoge__b_c_7__c_z {'a': 10, 'b': {'c': 7, 'd': 30}, 'c': 'z'}
# hoge__b_c_8__c_x {'a': 10, 'b': {'c': 8, 'd': 30}, 'c': 'x'}
# hoge__b_c_8__c_y {'a': 10, 'b': {'c': 8, 'd': 30}, 'c': 'y'}
# hoge__b_c_8__c_z {'a': 10, 'b': {'c': 8, 'd': 30}, 'c': 'z'}
# hoge__b_c_9__c_x {'a': 10, 'b': {'c': 9, 'd': 30}, 'c': 'x'}
# hoge__b_c_9__c_y {'a': 10, 'b': {'c': 9, 'd': 30}, 'c': 'y'}
# hoge__b_c_9__c_z {'a': 10, 'b': {'c': 9, 'd': 30}, 'c': 'z'}
# hoge__c_piyo {'a': 10, 'b': {'c': 20, 'd': 30}, 'c': 'piyo'}
# hoge__c_fuga {'a': 10, 'b': {'c': 20, 'd': 30}, 'c': 'fuga'}
# hoge__aaa {'a': 10, 'b': {'x': 30}, 'c': 'hogehoge'}
```
