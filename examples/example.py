"""Example script demonstrating all core features of config-forge.

Shows how to use Single, Patch, Union, Replace, Remove, map, and filter.
"""

import config_forge as cforge

# Use a double underscore to join generated configuration names
cforge.set_name_separator("__")

# Start with a single base configuration
base = cforge.Single("foo", {"a": 10, "b": {"c": 0}})

# Create a set patched with different numeric values
numbers = base.patch(**{f"n{i}": {"b": {"c": i}} for i in range(3)})

# Show how to remove a key entirely
remove_a = base.patch(no_a={"a": cforge.Remove()})

# Replace a sub-dictionary rather than merging it
replace_b = base.patch(repl={"b": cforge.Replace({"x": 99})})

# Combine the sets with union
cfgs = numbers | remove_a | replace_b

# Uppercase all names
mapped = cfgs.map(lambda n, c: (n.upper(), c))

# Keep configurations where "b.c" is at least 2 or it was replaced
filtered = mapped.filter(lambda n, c: c["b"].get("c", 0) >= 2 or "x" in c["b"])

# Print the final results
for name, cfg in filtered:
    print(name, cfg)

