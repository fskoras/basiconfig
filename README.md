SubConfig
=========

Configuration management library with value substitution for python

Basic Usage
-----------

sample.json

```json
{"Marco": "Polo"}
```

sample.py

```python
from subconfig import SubConfig

sc = SubConfig(files=["marco_polo.json"])

print(sc["Marco"])
```

Output:

```shell
Polo
```

Value Substitution
------------------

interpolation.json

```json
{
  "name": "Jane",
  "surname": "Doe",
  "full_name": "${name} ${surname}"
}
```

interpolation.py

```python
from subconfig import SubConfig

bc = SubConfig(files=["interpolation.json"])

print(bc["full_name"])
```

Output:

```shell
Jane Doe
```
