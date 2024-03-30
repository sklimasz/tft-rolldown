import pytest
from roll_sim.code import utils
from roll_sim.code.roll_champions import RolldownSimulator
from roll_sim.scripts import rolldown
from roll_sim.code import statistics
from pathlib import Path



def rolldown_func(conf, **kwargs):
    champs_to_buy, level, other = rolldown.get_and_validate_data(conf)

    path_script = Path(__file__).parent.resolve()
    path_roll_sim = path_script.parent.resolve()
    path_data = path_roll_sim / "data"

    champions, champs_to_buy = rolldown.prepare_data(path_data, champs_to_buy, level, other)

    sim = RolldownSimulator(champions=champions, champions_to_buy=champs_to_buy)
    avg_rolls = sim.roll(**kwargs)
    return avg_rolls

def test_rolldown_logic_with_math():
    # Check if expected value calculated with math is close to simulation result.
    conf = {
        "level": 10,
        "champs_to_buy":[{"name":"Hwei", "copies_necessary":1}],
    }
    number_of_five_costs = 9
    shop_odds_for_five_cost = 0.25

    avg_rolls = rolldown_func(conf,rolldowns = 10000,num_shops=1)
    expected = 1/(shop_odds_for_five_cost*(1/number_of_five_costs))
    assert avg_rolls < expected + 2
    assert avg_rolls > expected - 2