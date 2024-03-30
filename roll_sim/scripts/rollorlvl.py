import math
from pathlib import Path

import click

from ..code import utils


@click.command()
@click.option("--lvl", "-l", default=8, help="Current level.")
@click.option("--cost", "-c", default=4, help="Cost of wanted champion.")
@click.option("--gold", "-g", default=80, help="Current gold.")
@click.option("--exp", "-e", default=30, help="Experience missing to next level.")
def cli(lvl, cost, gold, exp):
    path = Path(__file__).parent.resolve()
    path_parent = path.parent.resolve()

    data = utils.load_config(path_parent / "data/levels.yml")
    odds = prepare_levels(data, lvl, cost)
    results = rolldown(odds, gold, exp)
    click.echo(f"Level {lvl} rolldown: {results[0]:.2f} {cost}-cost champs would appear in shops on average")
    click.echo(f"Level {lvl+1} rolldown: {results[1]:.2f} {cost}-cost champs would appear in shops on average")

def rolldown(odds: list[float | int], gold: int, exp: int) -> float:
    """Simulate rolling at current and next level for a champion of given cost."""
    # Get level odds.
    curr_lvl_odds = odds[0]
    next_lvl_odds = odds[1]

    # Calculate average copies seen at current level.
    wanted_costs_curr_lvl = 4*curr_lvl_odds*(gold//2)

    # Calculate average copies seen at next level.
    missing_exp = math.ceil(exp/4)
    wanted_costs_next_lvl = next_lvl_odds*4*((gold-4*missing_exp)//2)
    return wanted_costs_curr_lvl, wanted_costs_next_lvl


def prepare_levels(data: dict, lvl: int, cost: int) -> list[float]:
    """Find selected odds in dictionary."""
    for index, elem in enumerate(data):
        if elem["level"]==lvl:
            curr_level_odds = elem["odds"][cost]
            next_level_odds = data[index+1]["odds"][cost]
            return curr_level_odds, next_level_odds
    raise ValueError(f"No {lvl=} found in data.")

if __name__ == "__main__":
    cli()
