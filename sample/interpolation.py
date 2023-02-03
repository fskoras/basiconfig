from subconfig import SubConfig

sc = SubConfig(files=["interpolation.json"])

print(sc["full_name"])
