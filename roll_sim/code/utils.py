import json
from pathlib import Path

import yaml


def load_json(path: Path) -> dict:
    """Load json file."""
    with Path(path).open() as file:
        json_data = json.load(file)
    return json_data

def load_yaml(path: Path) -> dict:
    """Load yaml file."""
    with Path(path).open() as file:
        yaml_data = yaml.safe_load(file)
    return yaml_data

def load_config(file_path: Path) -> dict:
    """ Load configuration from a file.

    Args:
        file_path (str): Path to the configuration file.

    Returns:
        dict: Configuration data.
    """
    file_path = Path(file_path)
    file_suffix = file_path.suffix.lower()

    if file_suffix in ['.yaml', '.yml']:
        config_data = load_yaml(file_path)
    elif file_suffix == '.json':
        config_data = load_json(file_path)
    else:
        raise ValueError("Unsupported file format. Only YAML (.yaml/.yml) or JSON (.json) files are supported.")

    return config_data

def get_level_odds(level: int, level_data: dict) -> dict:
    """Get level odds from level dictionary."""
    for entry in level_data:
        if entry["level"] == level:
            return entry["odds"]
    raise ValueError("Incorrect levels config")

def prepare_champion_data(champions_data: dict,
                        level_data: list[dict, dict],
                        pool_data: dict) -> dict:
    """Apply level odds and pool sizes to champion data."""
    prepared_data = {}
    for cost, odds in level_data.items():
        prepared_data[cost] = {}
        prepared_data[cost]["odds"] = odds
        prepared_data[cost]["champions"] = []
        for champion in champions_data:
            if champion.get("cost") == cost:
                champion["pool_size"] = pool_data[champion["cost"]]
                del champion["cost"]
                prepared_data[cost]["champions"].append(champion)
    for cost in prepared_data:
        num_champs = len(prepared_data[cost]["champions"])
        for champion in prepared_data[cost]["champions"]:
            champion["odds"] = 1/num_champs

    return prepared_data

def apply_data_from_config(champions_data: dict,
                        champs_to_buy: dict,
                        other: dict | None) -> dict:
    """Apply data from config to champion data."""
    champ_names = {champ["name"] for champ in champs_to_buy}

    for cost in champions_data:
        for champ_to_buy in champs_to_buy:
            for champ in champions_data[cost]["champions"]:
                if champ_to_buy["name"] == champ["name"]:
                    data = {k:v for k,v in champ_to_buy.items() if k != "name"}
                    champ |= data
                    break

    if other is not None:
        other_names = {data.get("name") for data in other}
        name = data.get("name")
        cost_from_conf = data.get("cost")

        for data in other:
            name = data.get("name")
            cost_from_conf = data.get("cost")
            for cost in champions_data:
                for champ in champions_data[cost]["champions"]:

                    if name == champ["name"] and name not in champ_names:
                    # Don't specify champion copies taken in 'other' category.
                    # Do it directly in the 'champions_to_buy' category.
                        champ["copies_taken"] = data["copies_taken"]
                        break

                    if cost == cost_from_conf and champ["name"] not in other_names|champ_names:
                    # Update copies_taken of all champions with the given cost,
                    # but not if they were mentioned in 'other' category.
                    # copies_taken of overlapping champions won't be changed twice.
                        champ["copies_taken"] = data["copies_taken"]

    return champions_data
