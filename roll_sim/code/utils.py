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

def get_level_odds(level: int, level_data: dict) -> dict:
    """Get level odds from level dictionary."""
    for entry in level_data:
        if entry["level"] == level:
            return entry["odds"], entry["headliner_odds"]
    raise ValueError("Incorrect levels config")

def prepare_champion_data(champions_data: dict,
                        level_data: list[dict, dict],
                        pool_data: dict) -> dict:
    """Apply level odds and pool sizes to champion data."""
    prepared_data = []
    odds_dict, headliner_odds_dict = level_data
    for champion in champions_data:
        if (odds := odds_dict[champion["cost"]]) != 0:
            champion["odds"] = odds
            champion["headliner_odds"] = headliner_odds_dict[champion["cost"]]
            champion["pool_size"] = pool_data[champion["cost"]]
            prepared_data.append(champion)
    return prepared_data

def apply_pool_depletion(champions_data: dict,
                        headliners: dict,
                        other: dict | None) -> dict:
    """Apply copies taken to champion data."""
    for headliner in headliners:
        for champ in champions_data:
            if headliner["name"] == champ["name"]:
                data = {k:v for k,v in headliner.items() if k not in ["name", "headlined_trait"]}
                # WTF different thing when champ = champ | data
                champ |= data
                break

    if other is not None:
        hd_names = {headliner["name"] for headliner in headliners}
        other_names = {data.get("name") for data in other}

        for data in other:
            name = data.get("name")
            cost = data.get("cost")

            for champ in champions_data:
                if name == champ["name"] and name not in hd_names:
                # Don't specify headliners copies taken in 'other' category.
                # Do it directly in the 'headliners' category.
                    champ["copies_taken"] = data["copies_taken"]
                    break

                if champ["cost"] == cost and champ["name"] not in hd_names | other_names:
                # Update copies_taken of all champions with the given cost,
                # but not if they were mentioned in 'other' or 'headliners' categories.
                # copies_taken of overlapping champions won't be changed twice.
                    champ["copies_taken"] = data["copies_taken"]

    return champions_data