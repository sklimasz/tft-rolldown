from __future__ import annotations

import random

from ..code.champion import Champion
from copy import deepcopy


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

    def shop(self, headliner_shop):
        champs = []
        # Normal shop logic
        normal_shops = 5 if not headliner_shop else 4
        for shop in range(normal_shops):
            champs.append( (champ := random.choices(self.champions, weights=self.odds)[0]) )
            champ.copies_taken += 1

        if headliner_shop:
            # Headliner shop logic
            while True:
                headliner = random.choices(self.champions, weights=self.headliner_odds)[0]
                headlined_trait = random.choices(headliner.traits)[0]

                # Check if bad luck rules apply or if copies_left is less than 3
                if self.bad_luck_rules(headliner, headlined_trait) or headliner.copies_left < 3:
                    continue  # Restart the loop if conditions are not met
                
                # If conditions are met, break out of the loop
                break
            
            headliner.headlined_trait = headlined_trait
            self.last_seven_shops = self.last_seven_shops[-6:]
            self.last_seven_shops.append(headliner)

            if headliner in self.champions_needed and not self.headliner_bought:
                self.headliner_bought = True
                headliner.copies_held += 3

        # Common logic for both types of shops
        for champ in champs:
            if champ in self.champions_to_buy:
                champ.copies_held += 1
            else:
                champ.copies_taken -= 1


    def bad_luck_rules(self, random_headliner: Champion, headlined_trait: str) -> bool:
        """Check if rolled headliner doesn't break bad luck protection rules."""
        # A champion with same headlined_trait cannot appear again with the same headlined trait.
        if random_headliner.headlined_trait == headlined_trait:
            return True

        # 1, 2 and 3 cost headliners cannot appear again for 7 shops.
        if random_headliner.cost in [1, 2, 3] and random_headliner in self.last_seven_shops:
            return True

        # 4 costs headliner cannot appear again for 5 shops.
        if random_headliner.cost == 4 and random_headliner in self.last_seven_shops[-5:]:
            return True

        # 5 costs headliner cannot appear again for 4 shops.
        if random_headliner.cost == 5 and random_headliner in self.last_seven_shops[-4:]:
            return True

        # Same headlined trait cannot appear for 4 shops.
        if headlined_trait in [champion.headlined_trait for champion in self.last_seven_shops[-4:]]:
            return True

        return False


    def roll(self, rolldowns: int = 1000, bad_luck_rules = True, headliner_mechanic = True) -> float:
        """Roll for given headliners with a given headlined Trait.

        Args:
        ----
            champions (list[Champion] | None, optional): List of champions.
                Defaults to None, which becomes Sentinel Ekko.

            rolldowns (int, optional): Number of independent rolldowns.
                The bigger the number, the more accurate the results.
                Defaults to 10000.

            bad_luck_rules (bool, optional): Whether to apply bad luck protection rules.
                Buying and then selling every headliner you see should be the same as bad_luck_rules = False.
                Defaults to True.

        Returns:
        -------
            Float: Average rolls needed to hit one of your requested headliners.

        """
        self.rolls_list = []

        for rolldown in range(rolldowns):
            # Reset for every rolldown
            rolls = 0
            self.champions = deepcopy(self.champions_initial)
            self.last_seven_shops = []
            self.headliner_bought = False
            print(f"{rolldown=}")
            shops_counter = 0

            # Rolls condition ensures script finishes.
            while rolls < 1000:
                # Get random headliner with random headlined trait.
                if (not self.headliner_bought) and headliner_mechanic:
                    self.shop(headliner_shop=True)
                elif ( (shops_counter % 4) == 0 and shops_counter) and headliner_mechanic:
                    self.shop(headliner_shop=True)
                    shops_counter = 0
                else:
                    self.shop(headliner_shop=False)
                    shops_counter += 1
 
                # If we pass all rules, we have a valid roll.
                rolls += 1

                # If found what requested, stop current rolldown.
                if all(champ.copies_held >= champ.copies_necessary for champ in self.champions_to_buy):
                    self.rolls_list.append(rolls)
                    break

        # Return average rolls.
        self.avg_rolls = sum(self.rolls_list)/rolldowns
        return self.avg_rolls

