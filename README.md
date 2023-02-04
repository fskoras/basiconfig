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

sc = SubConfig(files=["sample.json"])

print(sc["Marco"])
```

Output:

```shell
Polo
```

Value Substitution
------------------

substitute.json

```json
{
  "name": "Jane",
  "surname": "Doe",
  "full_name": "${name} ${surname}"
}
```

substitute.py

```python
from subconfig import SubConfig

sc = SubConfig(files=["substitute.json"])

print(sc["full_name"])
```

Output:

```shell
Jane Doe
```

Nested value access
-------------------

Structured configuration values can be addressed using dot notation

nested.json

```json
{
  "books": [{"title":  "Little Red Riding Hood"}],
  "favorite_book": "${books.0.title}"
}
```

nested.py

```python
from subconfig import SubConfig

sc = SubConfig(["nested.json"])

print(sc["books.0.title"])

# Dot notation works for value substitution as well
print(sc["favorite_book"])
```

Output:

```shell
Little Red Riding Hood
Little Red Riding Hood
```
