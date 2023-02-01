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
marco = bc["Marco"]

print(marco)
```

Output:
```shell
Polo
```
