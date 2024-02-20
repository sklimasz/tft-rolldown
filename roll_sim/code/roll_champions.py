from __future__ import annotations

import random
from copy import deepcopy

from ..code.champion import Champion


class RolldownSimulator:
    def __init__(self, champions: list[Champion], champions_to_buy: list[Champion]):
        self.champions = champions
        self.champions_initial = deepcopy(self.champions)
        self.champions_needed = champions_to_buy

        self.headliner_bought = False

        self.rolls_list = []
        self.headliner_rolls = []
        self.last_seven_shops = []

    @property
    def champions_to_buy(self):
        return [champ for champ_to_buy in self.champions_needed
                for champ in self.champions
                if champ_to_buy.name == champ.name]

    @property
    def odds(self):
        return [champion.odds*(champion.copies_left/champion.pool_size)
                for champion in self.champions]

    @property
    def headliner_odds(self):
        return [champion.headliner_odds*(champion.copies_left/champion.pool_size)
                for champion in self.champions]

    def valid_headliner_shop(self, random_headliner: Champion, headlined_trait: str) -> bool:
        """Check if rolled headliner doesn't break bad luck protection rules."""
        # A champion with same headlined_trait cannot appear again with the same headlined trait.
        if random_headliner.headlined_trait == headlined_trait:
            return False

        # 1, 2 and 3 cost headliners cannot appear again for 7 shops.
        if random_headliner.cost in [1, 2, 3] and random_headliner in self.last_seven_shops:
            return False

        # 4 costs headliner cannot appear again for 5 shops.
        if random_headliner.cost == 4:
            if random_headliner.copies_held > 4:
                return False
            if random_headliner in self.last_seven_shops[-5:]:
                return False

        # 5 costs headliner cannot appear again for 4 shops.
        if random_headliner.cost == 5:
            if random_headliner.copies_held > 3:
                return False
            if random_headliner in self.last_seven_shops[-4:]:
                return False

        # Same headlined trait cannot appear for 4 shops.
        if headlined_trait in [champion.headlined_trait for champion in self.last_seven_shops[-4:]]:
            return False

        return True

    def headliner_shop(self, bad_luck_rules: bool) -> None:
        while True:
            headliner = random.choices(self.champions, weights=self.headliner_odds)[0]
            headlined_trait = random.choices(headliner.traits)[0]

            # Check if bad luck rules apply.
            if bad_luck_rules and not self.valid_headliner_shop(headliner, headlined_trait):
                continue

            #Check if enough copies left.
            if headliner.copies_left < 3:
                continue

            # If conditions are met, break out of the loop
            break

        headliner.headlined_trait = headlined_trait
        self.last_seven_shops = self.last_seven_shops[-6:]
        self.last_seven_shops.append(headliner)

        if not self.headliner_bought and headliner in self.champions_needed:
            self.headliner_bought = True
            headliner.copies_held += 3

    def shop(self, headliner_shop: bool, bad_luck_rules: bool) -> None:
        # Headliner shop is first.
        if headliner_shop:
            self.headliner_shop(bad_luck_rules)

        champs = []
        normal_shops = 5 if not headliner_shop else 4
        # Normal shop logic
        for shop in range(normal_shops):
            champs.append(champ := random.choices(self.champions, weights=self.odds)[0])
            champ.copies_taken += 1

        for champ in champs:
            if champ in self.champions_to_buy:
                champ.copies_held += 1
            else:
                champ.copies_taken -= 1

    def roll(self, rolldowns: int = 1000, headliner_mechanic: bool = True, bad_luck_rules: bool = True) -> float:
        """Roll for given headliners with a given headlined Trait.

        Args:
        ----
            rolldowns (int, optional): Number of independent rolldowns.
                The bigger the number, the more accurate the results.
                Defaults to 10000.

            headliner_mechanic (bool, optional): Whether to apply headliner logic.
                Defaults to True.

            bad_luck_rules (bool, optional): Whether to apply bad luck protection rules.
                Defaults to True.

        Returns:
        -------
            Float: Average rolls needed to hit all of your requested champions.

        """
        for rolldown in range(rolldowns):
            # Reset for every rolldown
            rolls = 0
            self.champions = deepcopy(self.champions_initial)
            self.last_seven_shops = []
            self.headliner_bought = False
            shops_counter = 0

            # Rolls condition ensures script finishes.
            while rolls < 1000:

                if headliner_mechanic:
                    if not self.headliner_bought or shops_counter % 4 == 0:
                        self.shop(headliner_shop=True, bad_luck_rules=bad_luck_rules)
                    else:
                        self.shop(headliner_shop=False)
                    shops_counter = 0 if shops_counter % 4 == 0 else shops_counter + 1
                else:
                    self.shop(headliner_shop=False)

                rolls += 1

                # If found what requested, stop current rolldown.
                if all(champ.copies_held >= champ.copies_necessary for champ in self.champions_to_buy):
                    self.rolls_list.append(rolls)
                    break

        # Return average rolls.
        self.avg_rolls = sum(self.rolls_list)/rolldowns
        return self.avg_rolls