from subconfig import SubConfig

sc = SubConfig(files=["substitute.json"])

print(sc["full_name"])
