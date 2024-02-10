import yaml
import json

def load_json(path):
    with open(path, "r") as file:
        json_data = json.load(file)
    return json_data

def load_yaml(path):
    with open(path, 'r') as file:
        yaml_data = yaml.safe_load(file)
    return yaml_data

def get_level_odds(level, level_data):
    for entry in level_data:
        if entry["level"] == level:
            level_odds = entry["odds"]
            return level_odds
    raise ValueError("Incorrect levels config")

def prepare_champion_data(champions_data, level_data, pool_data):
    prepared_data = []
    for champion in champions_data:
        if (odds := level_data[champion["cost"]]) != 0:
            champion["odds"] = odds
            champion["pool_size"] = pool_data[champion["cost"]]
            prepared_data.append(champion)
    return prepared_data

def apply_pool_depletion(champions_data, simulation_data):
    headliners = simulation_data["headliners"]
    for headliner in headliners:
        for champion in champions_data:
            if headliner["name"] == champion["name"]:
                champion["copies_taken"] = headliner.get("copies_taken", 0)
                break
    return champions_data

