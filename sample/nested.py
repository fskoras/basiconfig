from subconfig import SubConfig

sc = SubConfig(["nested.json"])

print(sc["books.0.title"])
print(sc["favorite_book"])
