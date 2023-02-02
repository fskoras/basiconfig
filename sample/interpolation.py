from subconfig import SubConfig

config = SubConfig(files=["interpolation.json"])

print(config["full_name"])
