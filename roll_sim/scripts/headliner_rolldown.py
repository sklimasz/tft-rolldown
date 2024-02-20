from pathlib import Path

import click

from roll_sim.code import utils
from roll_sim.code.champion import Champion
from roll_sim.code.roll_headliners import RolldownSimulator
from roll_sim.code.statistics import get_stats


@click.command()
@click.option("--conf", "-c", help="Path to json file with with headliners and level data.")
@click.option("--rolldowns", "-r", default=10000, help="Number of rolldowns.")
@click.option("--rules","-blr", default=True, help="Whether to apply bad luck protection rules.")
@click.option("--stats", "-s", default=True, help="Wheter to compute and display advanced stats.")
def cli(conf, rolldowns, rules, stats):
    # Load config
    conf = utils.load_json(conf)

    # Get and validate data from config
    headliners, level, other = get_and_validate_data(conf = conf)

    # Echo conf data
    click.echo(f"\nRequested headliners at {level=}:")
    for headliner in headliners:
        click.echo(headliner)

    # Ensure that this gets data from data folder correctly,
    # wherever it is run from.
    path_script = Path(__file__).parent.resolve()
    path_roll_sim = path_script.parent.resolve()
    path_data = path_roll_sim / "data"

    # Load and prepare data, apply pool depletion, convert into Champion objects.
    champions, headliners = prepare_data(path_data, headliners, level, other)

    # Simulate rolldown and get results.
    simulator = RolldownSimulator(champions=champions, headliners_to_buy=headliners)
    avg_rolls = simulator.roll(rolldowns=rolldowns, bad_luck_rules=rules)

    # Display results.
    click.echo("\nRolldown results:")
    click.echo(f"average rolls = {round(avg_rolls, 2)}")

    # Compute and display stats.
    if stats:
        rolls_list = simulator.rolls_list
        probabilities = [0.5, 0.75, 0.9]
        rolls_needed_list, median, stdev = get_stats(rolls_list, probabilities)
        click.echo(f"median = {round(median, 2)}")
        click.echo(f"deviation  = {round(stdev, 2)}\n")
        click.echo("Rolls needed to achieve probability:")
        for rolls_needed, prob in zip(rolls_needed_list, probabilities):
            click.echo(f"{rolls_needed} rolls -> {prob*100}%")

def get_and_validate_data(conf: dict) -> tuple[dict, dict, dict]:
    """Get data from config and ensure it contains necessary data."""
    if (level := conf.get("level")) is None:
        raise ValueError("No level data in conf")

    if (headliners := conf.get("headliners")) is None:
        raise ValueError("No headliners data in conf")

    other = conf.get("other")
    return headliners, level, other

def prepare_data(data_path: Path,
                headliners: dict,
                level: int,
                other: dict | None) -> tuple[list[Champion], list[Champion]]:
    """Load and prepare data, apply pool depletion, convert into Champion objects."""
    champions_data = utils.load_json(data_path / "champions.json")
    level_data = utils.load_yaml(data_path / "levels.yml")
    level_data = utils.get_level_odds(level = level, level_data=level_data )
    pool_data = utils.load_yaml(data_path / "champion_pool_sizes.yml")

    champions = utils.prepare_champion_data(champions_data, level_data, pool_data)
    champions = utils.apply_pool_depletion(champions, headliners, other)
    champions = Champion.from_list(champions)
    headliners = Champion.from_list(headliners)
    return champions, headliners

if __name__ == "__main__":
    cli()
