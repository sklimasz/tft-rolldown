import pytest
from roll_sim.code import utils
from roll_sim.code.roll import RolldownSimulator
from roll_sim.scripts import run_rolldown
from roll_sim.code import statistics
from roll_sim.tests.fixtures import (
    level8_executioner,
    level8_pool_depletion_easier,
    level8_pool_depletion_harder,
    incorrect_conf_no_headliners,
    incorrect_conf_no_level,
)
from pathlib import Path


def test_conf_no_level(incorrect_conf_no_level):
    conf = incorrect_conf_no_level
    with pytest.raises(ValueError):
        run_rolldown.get_and_validate_data(conf)

def test_conf_headliners(incorrect_conf_no_headliners):
    conf = incorrect_conf_no_headliners
    with pytest.raises(ValueError):
        run_rolldown.get_and_validate_data(conf)

def test_simple_rolldown(level8_executioner):
    conf = level8_executioner
    headliners, level, other = run_rolldown.get_and_validate_data(conf)

    path_script = Path(__file__).parent.resolve()
    path_roll_sim = path_script.parent.resolve()
    path_data = path_roll_sim / "data"

    champions, headliners = run_rolldown.prepare_data(path_data, headliners, level, other)

    sim = RolldownSimulator(champions=champions, headliners_to_buy=headliners)
    avg_rolls = sim.roll(rolldowns=1000, bad_luck_rules=True)
    assert 3 < avg_rolls < 15

def test_bad_luck_rules(level8_executioner):
    conf = level8_executioner
    headliners, level, other = run_rolldown.get_and_validate_data(conf)

    path_script = Path(__file__).parent.resolve()
    path_roll_sim = path_script.parent.resolve()
    path_data = path_roll_sim / "data"
    
    champions, headliners = run_rolldown.prepare_data(path_data, headliners, level, other)
    sim = RolldownSimulator(champions=champions, headliners_to_buy=headliners)

    avg_rolls_with_rules = sim.roll(rolldowns=10000, bad_luck_rules=True)
    avg_rolls_without_rules = sim.roll(rolldowns=10000, bad_luck_rules=False)
    assert avg_rolls_with_rules < avg_rolls_without_rules

def test_pool_depletion_easier(level8_pool_depletion_easier, level8_executioner):
    conf = level8_executioner
    conf_easy = level8_pool_depletion_easier

    headliners, level, other = run_rolldown.get_and_validate_data(conf)
    headliners_easy, level_easy, other_easy = run_rolldown.get_and_validate_data(conf_easy)

    path_script = Path(__file__).parent.resolve()
    path_roll_sim = path_script.parent.resolve()
    path_data = path_roll_sim / "data"
    
    champions, headliners = run_rolldown.prepare_data(path_data, headliners, level, other)
    champions_easier, headliners_easier = run_rolldown.prepare_data(path_data, headliners_easy, level_easy, other_easy)

    sim = RolldownSimulator(champions=champions, headliners_to_buy=headliners)
    sim_easier = RolldownSimulator(champions=champions_easier, headliners_to_buy=headliners_easier)

    avg_rolls = sim.roll()
    avg_rolls_easier = sim_easier.roll()
    assert avg_rolls_easier < avg_rolls

def test_pool_depletion_harder(level8_executioner, level8_pool_depletion_harder):
    conf = level8_executioner
    conf_hard = level8_pool_depletion_harder

    headliners, level, other = run_rolldown.get_and_validate_data(conf)
    headliners_hard, level_hard, other_hard = run_rolldown.get_and_validate_data(conf_hard)

    path_script = Path(__file__).parent.resolve()
    path_roll_sim = path_script.parent.resolve()
    path_data = path_roll_sim / "data"
    
    champions, headliners = run_rolldown.prepare_data(path_data, headliners, level, other)
    champions_hard, headliners_hard = run_rolldown.prepare_data(path_data, headliners_hard, level_hard, other_hard)

    sim = RolldownSimulator(champions=champions, headliners_to_buy=headliners)
    sim_harder = RolldownSimulator(champions=champions_hard, headliners_to_buy=headliners_hard)

    avg_rolls = sim.roll()
    avg_rolls_harder = sim_harder.roll()
    assert avg_rolls_harder > avg_rolls
