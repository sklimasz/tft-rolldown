from __future__ import annotations

import random

from .champion import Champion


class RolldownSimulator:
    def __init__(self, champions: list[Champion], headliners_to_buy: list[Champion]):
        self.champions = champions
        self.odds = [champion.headliner_odds*(champion.copies_left/champion.pool_size)
                    for champion in champions]
        self.headliners_to_buy = headliners_to_buy
        self.last_seven_shops = []
        self.rolls_list = []

    def choice_generator(self):
        """Yield random headliner along with random headlined trait selected."""
        while True:
            random_headliner = random.choices(self.champions, weights=self.odds)[0]
            headlined_trait = random.choice(random_headliner.traits)
            yield random_headliner, headlined_trait

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

    def roll(self, rolldowns: int = 10000, bad_luck_rules: bool = True) -> float:
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
        generator = self.choice_generator()
        self.rolls_list = []

        for rolldown in range(rolldowns):
            # Reset for every rolldown
            self.last_seven_shops = []
            rolls = 0
            for champion in self.champions:
                champion.headlined_trait = None

            # Rolls condition ensures script finishes.
            while rolls < 1000:
                # Get random headliner with random headlined trait.
                random_headliner, headlined_trait = next(generator)

                # If bad luck rules are broken, we go back to random champion selection.
                # We do not register it as a roll (such roll would not be offered).
                if bad_luck_rules and self.bad_luck_rules(random_headliner, headlined_trait):
                    continue

                # Same headliner cannot appear twice in a row.
                if random_headliner in self.last_seven_shops[-1:]:
                    continue

                # If we pass all rules, we have a valid roll.
                rolls += 1

                # Update headlined_trait for rolled champion.
                for champion in self.champions:
                    if champion.name == random_headliner.name:
                        champion.headlined_trait = headlined_trait

                # Update last 7 shops, remove oldest champion and append most recent one.
                self.last_seven_shops = self.last_seven_shops[-6:]
                self.last_seven_shops.append(random_headliner)

                # If found what requested, stop current rolldown.
                if random_headliner in self.headliners_to_buy:
                    self.rolls_list.append(rolls)
                    break

        # Return average rolls.
        self.avg_rolls = sum(self.rolls_list)/rolldowns
        return self.avg_rolls

