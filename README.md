basiconfig
==========

Configuration management library for python

Basic Usage
===========

marco_polo.json
```json
{"Marco": "Polo"}
```

sample.py
```python
from basiconfig import BasiConfig

bc = BasiConfig(files=["marco_polo.json"])

print(bc["Marco"])
```

Output:
```shell
Polo
```

Values Interpolation
====================

interpolation.json
```json
{
  "name": "Jane",
  "surname": "Doe",
  "full_name": "${name} ${surname}"
}
```

```python
from basiconfig import BasiConfig

bc = BasiConfig(files=["interpolation.json"])

print(bc["full_name"])
```

Output:
```shell
Jane Doe
```