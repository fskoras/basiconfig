from subconfig import SubConfig

sc = SubConfig(["nested.json"])

print(sc["books.0.title"])

# Dot notation works for value substitution as well
print(sc["favorite_book"])
