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
    headliners_names = [headliner["name"] for headliner in headliners]
    for headliner in headliners:
        for champion in champions_data:
            if headliner["name"] == champion["name"]:
                champion["copies_taken"] = headliner.get("copies_taken", 0)
                break
    
    other = simulation_data.get("other", None)

    # Rewrite this disgusting code below.
    # FIXME
    if other is not None:
        other_names = [elem.get("name", None) for elem in other]
        for data in other:
            if (name := data.get("name")) is not None:
                # If champion name is specified, apply it a champion
                # but not if the champion was mentioned in 'headliners' category
                # You can apply copies taken directly in the headliner category.
                for champion in champions_data:
                    if champion["name"] not in headliners_names and name == champion["name"]:
                        champion["copies_taken"] = data["copies_taken"]
                        break
            if (cost := data.get("cost")) is not None:
                # If cost is specified, apply it to all champions of the cost
                # but not to the champions mentioned in 'headliners' and 'other' category
                for champion in champions_data:
                    if champion["name"] not in headliners_names+other_names and cost == champion["cost"]:
                        champion["copies_taken"] = data["copies_taken"]
    return champions_data

