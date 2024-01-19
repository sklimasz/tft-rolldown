import click
import json
import math

@click.command()
@click.option('--lvl',default=8,help='current level')
@click.option('--cost',default=4,help='cost of wanted champion')
@click.option('--gold',default=80,help='your current gold')
@click.option('--exp',default=30,help='experience missing to next level')

def cli(lvl, cost, gold, exp):
    
    data = load_json('data/odds.json')
    levels = prepare(data,lvl)
    results = rolldown(levels,cost,gold,exp)
    outcome(results, cost)


def rolldown(levels, cost, gold, exp):

    current_odds = levels[0]['odds'][f'{cost}']
    nextlvl_odds = levels[1]['odds'][f'{cost}']

    wanted_costs_INSTAROLL = current_odds*4*(gold//2)

    levelups_bought = math.ceil(exp/4)
    wanted_costs_LVLROLL = nextlvl_odds*4*((gold-4*levelups_bought)//2)

    return wanted_costs_INSTAROLL, wanted_costs_LVLROLL

def outcome(results,cost):

    print(f'Instant rolldown: {results[0]} {cost}-cost champs would appear in shop on average')
    print(f'Levelled rolldown: {results[1]} {cost}-cost champs would appear in shop on average')


def prepare(data,lvl):
    for elem in data:
        if elem['level']==lvl:
            currlvl = elem
        if elem['level']==lvl+1:
            nextlvl = elem

    return currlvl,nextlvl

def load_json(path):
    with open(path, "r") as file:
        json_data = json.load(file)

    return json_data

if __name__=='__main__':
    cli()