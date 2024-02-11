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
    hd_names = {headliner["name"] for headliner in headliners}
    other = simulation_data.get("other", [])
    other_names = {data.get("name") for data in other}

    for headliner in headliners:
        for champion in champions_data:
            if headliner["name"] == champion["name"]:
                champion["copies_taken"] = headliner.get("copies_taken", 0)
                break

    for data in other:
        name = data.get("name")
        cost = data.get("cost")

        for champion in champions_data:
            if name == champion["name"] and name not in hd_names:
            # Don't specify headliners copies taken in 'other' category
            # Do it directly in the 'headliners' category
                champion["copies_taken"] = data["copies_taken"]
                break

            if champion["cost"] == cost and champion["name"] not in hd_names|other_names:
            # Update copies_taken of all champions with the given cost,
            # but not if they were mentioned in 'other' or 'headliners' categories.
            # copies_taken of overlapping champions won't be changed twice.
                champion["copies_taken"] = data["copies_taken"]

    return champions_data

