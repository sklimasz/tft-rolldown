import yaml
import json
from roll import Champion

def load_json(path):
    with open(path, "r") as file:
        json_data = json.load(file)
    return json_data

def load_yaml(path):
    with open(path, 'r') as file:
        yaml_data = yaml.safe_load(file)
    return yaml_data

def get_level_odds(level, path='data/levels.yml'):
    level_data = load_yaml(path)
    for entry in level_data:
        if entry["level"] == level:
            level_odds = entry["odds"]
    return level_odds

def prepare_data(level,
                champions_path = "data/champions.json",
                level_path = "data/levels.yml"):
    champions_data = load_json(champions_path)
    level_odds = get_level_odds(level=level, path=level_path)
    champions = Champion.from_list(champions_data, level_odds)
    return champions



