import pytest
from copy import deepcopy

@pytest.fixture(scope="session")
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

@pytest.fixture
def incorrect_conf_no_level():
    conf = {
    "headliners":
        [
        {"name": "Akali", "headlined_trait": "Executioner"},
        {"name": "Karthus", "headlined_trait": "Executioner"},
        {"name": "Vex", "headlined_trait": "Executioner"},
        {"name": "Samira", "headlined_trait": "Executioner"},
        ],
    }
    return conf

@pytest.fixture
def incorrect_conf_no_headliners():
    conf = {
        "level" : 8,
    }
    return conf

@pytest.fixture
def level8_pool_depletion_easier(level8_executioner):
    conf = deepcopy(level8_executioner)
    conf["other"] = [
        {"cost":4, "copies_taken":8},
        {"cost":3, "copies_taken":8},
    ]
    return conf

@pytest.fixture
def level8_pool_depletion_harder(level8_executioner):
    conf = deepcopy(level8_executioner)
    for headliner in conf["headliners"]:
        headliner["copies_taken"] = 5
    return conf

@pytest.fixture
def level8_hearsteel():
    conf = {
    "level":7,
    "headliners":
        [
        {"name": "Sett", "headlined_trait": "Heartsteel"},
        {"name": "Yone", "headlined_trait": "Heartsteel"},
        {"name": "Aphelios", "headlined_trait": "Heartsteel"},
        ],
    }
    return conf