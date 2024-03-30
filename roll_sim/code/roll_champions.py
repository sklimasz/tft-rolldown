from __future__ import annotations

import random
from copy import deepcopy

from ..code.champion import Champion, odds_cache


class RolldownSimulator:
    def __init__(self, champions: list[Champion], champions_to_buy: list[Champion]):
        self.champions = champions

        self.cost_keys = list(self.champions.keys())
        self.cost_odds = [ data["odds"] for data in self.champions.values() ]

        self.odds = {}
        for cost in self.champions:
            self.odds[cost] = []
            for champ in self.champions[cost]["champions"]:
                self.odds[cost].append(odds_cache(champ.odds, champ.pool_size, champ.copies_taken))
        
        self.champions_to_buy_indexes = []
        self.champions_to_buy = champions_to_buy
        for cost in self.champions:
            for champ_to_buy in self.champions_to_buy:
                for champ in self.champions[cost]["champions"]:
                    if champ_to_buy == champ:
                        self.champions_to_buy_indexes.append((cost, self.champions[cost]["champions"].index(champ) ))
        
        self.odds_initial = deepcopy(self.odds)
        self.champions_initial = deepcopy(self.champions)
        self.champions_to_buy = champions_to_buy
        self.rolls_list = []

        # Check whether they aren't any incorrect champions.
        # if not (all((incorrect := champ) in self.champions for champ in self.champions_to_buy)):
        #     raise ValueError(f"Incorrect '{incorrect.name}' champion in config.")


        # self.odds = [odds_cache(champ.odds, champ.pool_size, champ.copies_taken) for champ in self.champions]

    # @property
    # def odds(self):
    #     return [champion.odds*(champion.copies_left/champion.pool_size)
    #             for champion in self.champions]
        
    # @property
    # def odds(self):
    #     return [odds_cache(champ.odds, champ.pool_size, champ.copies_taken) for champ in self.champions]

    def shop(self, num_shops=5) -> None:

        indexes = []
        for shop in range(num_shops):
            cost_key = random.choices(self.cost_keys, self.cost_odds)[0]
            cost_champions = self.champions[cost_key]["champions"]

            index = random.choices(list(range(len(cost_champions))), weights=self.odds[cost_key])[0]

            indexes.append((cost_key, index))

            champ = self.champions[cost_key]["champions"][index]
            champ.copies_taken += 1

            self.odds[cost_key][index] = odds_cache(champ.odds, champ.pool_size, champ.copies_taken)

        for cost_key, index in indexes:
            champ = self.champions[cost_key]["champions"][index]
            if champ in self.champions_to_buy and (champ.copies_necessary > champ.copies_held):
                champ.copies_held += 1
            else:
                champ.copies_taken -= 1

            self.odds[cost_key][index] = odds_cache(champ.odds, champ.pool_size, champ.copies_taken)

    def roll(self, rolldowns: int = 1000, num_shops = 5) -> float:
        """Roll for given champions.

        Args:
        ----
            rolldowns (int, optional): Number of independent rolldowns.
                The bigger the number, the more accurate the results.
                Defaults to 10000.

        Returns:
        -------
            Float: Average rolls needed to hit all of your requested champions.

        """
        for rolldown in range(rolldowns):
            # Reset for every rolldown
            rolls = 0
            self.champions = deepcopy(self.champions_initial)
            self.odds = deepcopy(self.odds_initial)
            self.champions_needed = [self.champions[cost_key]["champions"][index] for cost_key, index in self.champions_to_buy_indexes]

            # Rolls condition ensures script finishes.
            while rolls < 1000:
                self.shop(num_shops=num_shops)
                rolls += 1

                # If found what requested, stop current rolldown.
                if all(champ.copies_held >= champ.copies_necessary for champ in self.champions_needed):
                    self.rolls_list.append(rolls)
                    break

        # Return average rolls.
        self.avg_rolls = sum(self.rolls_list)/rolldowns
        return self.avg_rolls