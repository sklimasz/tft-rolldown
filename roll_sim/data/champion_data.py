import json
from pathlib import Path
import yaml

def load_json(path: Path) -> dict:
    """Load json file."""
    with Path(path).open() as file:
        json_data = json.load(file)
    return json_data

full_data = load_json("tft-champion.json")
champs = full_data["data"]

to_save = []
for champ_data in champs.values():
    tmp = {}
    tmp["name"] = champ_data["name"]
    tmp["cost"] = champ_data["tier"]
    to_save.append(tmp)

to_save = sorted(to_save, key=lambda x: (x["cost"], x["name"]))
to_save = [
    {"name": champ_data["name"], "cost": champ_data["cost"]} for champ_data in to_save
]

# File path to save JSON data
file_path = "champions_info.yml"

# Save the data to a JSON file
with open(file_path, "w") as yaml_file:
    yaml.dump(to_save, yaml_file, indent=4)  # indent parameter for pretty formatting