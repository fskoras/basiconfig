from basiconfig import BasiConfig

bc = BasiConfig(files=["marco_polo.json"])
marco = bc["Marco"]

print(marco)
