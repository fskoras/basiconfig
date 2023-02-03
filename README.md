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

Nested value access
-------------------

Structured configuration values ​​can be addressed using dot notation

nested.json

```json
{
  "books": [{"title":  "Little Red Riding Hood"}],
  ...
}
```

nested.py

```python
from subconfig import SubConfig

sc = SubConfig(["nested.json"])

print(sc["books.0.title"])
```

Dot notation works for value substitution as well

```json
{
  ...
  "favorite_book": "${books.0.title}"
}
```

```python
print(sc["favorite_book"])
```

Output:

```shell
Little Red Riding Hood
```
