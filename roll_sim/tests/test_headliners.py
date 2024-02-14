import pytest
from ..code import utils, roll, champion
from pathlib import Path


def prepare_data(conf: dict):
    # Sanity checks and sweet walruses
    if (level := conf.get("level")) is None:
        raise ValueError("No level data in conf")
    if (headliners := conf.get("headliners")) is None:
        raise ValueError("No headliners data in conf")

    # Prepare data
    path = Path(__file__).parent.resolve()
    path_parent = path.parent.resolve()
    champions_data = utils.load_json(path_parent / "data/champions.json")
    level_data = utils.load_yaml(path_parent / "data/levels.yml")
    level_data = utils.get_level_odds(level = level, level_data=level_data )
    pool_data = utils.load_yaml(path_parent / "data/champion_pool_sizes.yml")

    champions = utils.prepare_champion_data(champions_data, level_data, pool_data)
    champions = utils.apply_pool_depletion(champions, conf)
    champions = champion.Champion.from_list(champions)
    headliners = champion.Champion.from_list(headliners)
    return champions, headliners

@pytest.fixture
def level8_executioner():
    conf =  {
    "level":8,
    "headliners":
        [
        {"name": "Akali", "headlined_trait": "Executioner"},
        {"name": "Karthus", "headlined_trait": "Executioner"},
        {"name": "Vex", "headlined_trait": "Executioner"},
        {"name": "Samira", "headlined_trait": "Executioner"},
        ],
    }
    return conf

def test_simple_rolldown(level8_executioner):
    conf = level8_executioner
    champions, headliners = prepare_data(conf)
    sim = roll.RolldownSimulator(champions=champions, headliners_to_buy=headliners)
    avg_rolls = sim.roll(rolldowns=1000, bad_luck_rules=True)
    assert 3 < avg_rolls < 15

def test_bad_luck_rules(level8_executioner):
    conf = level8_executioner
    champions, headliners = prepare_data(conf)
    sim = roll.RolldownSimulator(champions=champions, headliners_to_buy=headliners)
    avg_rolls_with_rules = sim.roll(rolldowns=1000, bad_luck_rules=True)
    avg_rolls_without_rules = sim.roll(rolldowns=1000, bad_luck_rules=False)
    assert avg_rolls_with_rules < avg_rolls_without_rules
