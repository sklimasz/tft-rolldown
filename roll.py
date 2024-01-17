from __future__ import annotations
import random
from dataclasses import dataclass, KW_ONLY

@dataclass
class Champion:
    """Headliner representation"""
    _ : KW_ONLY
    name: str
    cost: str | None = None
    odds: int | float | None = None
    traits: list[str] | None = None
    headlined_trait: str | None = None

    def __eq__(self, other):
        """Define equality as champions having same name and same headlined trait"""
        if isinstance(other, Champion):
            name_match = (self.name == other.name)
            headlined_trait_match = (self.headlined_trait == other.headlined_trait)
            return (name_match and headlined_trait_match)

        return False

    @staticmethod
    def from_list(champions_data:list[dict],
                level_odds: dict[int | float] | None = None) -> list[Champion]:
        """Create list of champion objects from list of dictionares"""
        if level_odds is not None:
            for champion_data in champions_data:
                champion_data["odds"] = level_odds[champion_data["cost"]]
        
        champions = [
            Champion(**champion_data)
            for champion_data in champions_data
            if champion_data.get("odds") != 0
        ]
        return champions
    
class RolldownSimulator:
    def __init__(
        self,
        champions_list: list[Champion],
        headliners_to_buy: list[str, str] | None = None,
    ):
        self.champions_list = champions_list
        self.weights = [champion.odds for champion in champions_list]
        self.headliners_to_buy = headliners_to_buy
        self.last_seven_shops = []
        self.rolls_list = []

    def choice_generator(self):
        """Generator yielding random headliner along with random headlined trait selected"""
        while True:
            random_headliner = random.choices(self.champions_list, weights=self.weights)[0]
            headlined_trait = random.choice(random_headliner.traits)
            yield random_headliner, headlined_trait

    def bad_luck_rules(self, random_headliner: Champion, headlined_trait: str) -> bool:
        """Checks if rolled headliner doesn't break bad luck protection rules"""

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

    def roll(
        self,
        champions:  list[Champion] | None = None,
        rolldowns: int = 10000,
        bad_luck_rules: bool = True,
        ) -> float:
        """
        Roll for given headliners with a given headlined Trait.

        Args:
            champions (list[Champion] | None, optional): List of champions.
                Defaults to None, which becomes Sentinel Ekko.
                
            rolldowns (int, optional): Number of independent rolldowns.
                The bigger the number, the more accurate the results.
                Defaults to 10000.

            bad_luck_rules (bool, optional): Whether to apply bad luck protection rules.
                Buying and then selling every headliner you see should be the same as bad_luck_rules = False.
                Defaults to True.

        Returns:
            Float: Average rolls needed to hit one of your requested headliners.
        """

        # Default value is Sentinel Ekko
        if champions is None:
            champions = [Champion(name="Ekko", headlined_trait="Sentinel")]
        
        generator = self.choice_generator()
        self.rolls_list = []
    
        for rolldown in range(rolldowns):
            # Reset for every rolldown
            self.last_seven_shops = []
            rolls = 0
            for champion in self.champions_list:
                champion.headlined_trait = None
            
            # Rolls condition ensures script finishes.
            while rolls < 1000:
                # Get random headliner with random headlined trait.
                random_headliner, headlined_trait = next(generator)

                # If any of those rules is not met, we go back to random champion selection
                # And we do not register it as a roll (such roll would not be offered).
                if bad_luck_rules and self.bad_luck_rules(random_headliner, headlined_trait):
                    continue

                # Same headliner cannot appear twice in a row.
                if random_headliner in self.last_seven_shops[-1:]:
                    continue

                # If we pass all rules, we have a valid roll.
                rolls += 1

                # Update headlined_trait for rolled champion.
                for champion in self.champions_list:
                    if champion.name == random_headliner.name:
                        champion.headlined_trait = headlined_trait

                # Update last 7 shops, remove oldest champion and append most recent one.
                self.last_seven_shops = self.last_seven_shops[-6:]
                self.last_seven_shops.append(random_headliner)

                # If found what requested, stop current rolldown.
                if random_headliner in self.headliners_to_buy:
                    self.rolls_list.append(rolls)
                    break

        # Return average rolls
        self.avg_rolls = sum(self.rolls_list)/rolldowns
        return self.avg_rolls

