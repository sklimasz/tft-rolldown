import click

import utils
from roll import Champion, RolldownSimulator
from stats import get_stats


@click.command()
@click.option("--conf", "-c", help="Path to json file with with headliners and level data.")
@click.option("--rolldowns", "-r", default=10000, help="Number of rolldowns.")
@click.option("--rules","-blr", default=True, help="Whether to apply bad luck protection rules.")
@click.option("--stats", "-s", default=True, help="Wheter to compute and display advanced stats.")
def cli(conf, rolldowns, rules, stats):
    # Load config
    conf = utils.load_json(conf)

    # Sanity checks and sweet walruses
    if (level := conf.get("level")) is None:
        raise ValueError("No level data in conf")
    if (headliners := conf.get("headliners")) is None:
        raise ValueError("No headliners data in conf")

    # Echo conf data
    click.echo(f"\nRequested headliners at {level=}:")
    for headliner in headliners:
        click.echo(headliner)

    # Prepare data
    champions_data = utils.load_json("data/champions.json")
    level_data = utils.load_yaml("data/levels.yml")
    level_data = utils.get_level_odds(level = level, level_data=level_data )
    pool_data = utils.load_yaml("data/champion_pool_sizes.yml")

    champions = utils.prepare_champion_data(champions_data, level_data, pool_data)
    champions = utils.apply_pool_depletion(champions, conf)
    champions = Champion.from_list(champions)
    headliners = Champion.from_list(headliners)

    # Simulate rolldown
    simulator = RolldownSimulator(champions=champions, headliners_to_buy=headliners)
    avg_rolls = simulator.roll(rolldowns=rolldowns, bad_luck_rules=rules)

    # Display results
    click.echo("\nRolldown results:")
    click.echo(f"average rolls = {round(avg_rolls, 2)}")

    # Compute and display stats
    if stats:
        rolls = simulator.rolls_list
        probabilities = [0.5, 0.75, 0.9]
        rolls_needed_list, median, stdev = get_stats(rolls, probabilities)
        click.echo(f"median = {round(median, 2)}")
        click.echo(f"deviation  = {round(stdev, 2)}\n")
        click.echo("Rolls needed to achieve probability:")
        for rolls_needed, prob in zip(rolls_needed_list, probabilities):
            click.echo(f"{rolls_needed} rolls -> {prob*100}%")

if __name__ == "__main__":
    cli()
