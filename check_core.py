import json
with open("reports/CVE-2021-44228/core.json") as f:
    d = json.load(f)
print("conflicts:", d.get("conflicts"))
print("errors:", d.get("errors"))