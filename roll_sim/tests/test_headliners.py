import pytest
from roll_sim.code import utils
from roll_sim.code.roll_headliners import RolldownSimulator
from roll_sim.scripts import headliner_rolldown
from roll_sim.code import statistics
from roll_sim.tests.fixtures import (
    level8_executioner,
    level8_pool_depletion_easier,
    level8_pool_depletion_harder,
    incorrect_conf_no_headliners,
    incorrect_conf_no_level,
)
from pathlib import Path

def rolldown(conf, **kwargs):
    headliners, level, other = headliner_rolldown.get_and_validate_data(conf)

    path_script = Path(__file__).parent.resolve()
    path_roll_sim = path_script.parent.resolve()
    path_data = path_roll_sim / "data"

    champions, headliners = headliner_rolldown.prepare_data(path_data, headliners, level, other)

    sim = RolldownSimulator(champions=champions, headliners_to_buy=headliners)
    avg_rolls = sim.roll(**kwargs)
    return avg_rolls

def test_conf_no_level(incorrect_conf_no_level):
    conf = incorrect_conf_no_level
    with pytest.raises(ValueError):
        headliner_rolldown.get_and_validate_data(conf)

def test_conf_headliners(incorrect_conf_no_headliners):
    conf = incorrect_conf_no_headliners
    with pytest.raises(ValueError):
        headliner_rolldown.get_and_validate_data(conf)

def test_simple_rolldown(level8_executioner):
    conf = level8_executioner
    avg_rolls = rolldown(conf=conf)
    assert 3 < avg_rolls < 15

def test_bad_luck_rules(level8_executioner):
    conf = level8_executioner
    avg_rolls_with_rules = rolldown(conf=conf)
    avg_rolls_without_rules = rolldown(conf=conf, bad_luck_rules = False)
    assert avg_rolls_with_rules < avg_rolls_without_rules

def test_pool_depletion_easier(level8_pool_depletion_easier, level8_executioner):
    conf = level8_executioner
    conf_easy = level8_pool_depletion_easier

    avg_rolls = rolldown(conf)
    avg_rolls_easier = rolldown(conf_easy)
    assert avg_rolls_easier < avg_rolls

def test_pool_depletion_harder(level8_executioner, level8_pool_depletion_harder):
    conf = level8_executioner
    conf_hard = level8_pool_depletion_harder

    avg_rolls = rolldown(conf)
    avg_rolls_harder = rolldown(conf_hard)
    assert avg_rolls_harder > avg_rolls
