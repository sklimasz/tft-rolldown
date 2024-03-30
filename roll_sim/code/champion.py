from __future__ import annotations

from dataclasses import KW_ONLY, dataclass
from functools import lru_cache


@dataclass
class Champion:
    """Champion representation."""

    _ : KW_ONLY
    name: str
    cost: str | None = None
    odds: int | float | None = None

    traits: list[str] | None = None

    pool_size: int = 0
    copies_taken: int = 0
    copies_held: int = 0
    copies_necessary: int = 9

    # @property
    # def copies_left(self) -> int:
    #     return self.pool_size - self.copies_taken

    def __eq__(self, other) -> bool:
        """Define equality as champions having same name and same headlined trait."""
        if isinstance(other, Champion):
            return self.name == other.name
        return False
    
    def __hash__(self) -> int:
        """Hash the Champion instance based on its name."""
        return hash(self.name)

    @staticmethod
    def from_list(champions_data: list[dict]) -> list[Champion]:
        """Create list of champion objects from list of dictionares."""
        return [Champion(**champion_data) for champion_data in champions_data]

@lru_cache(maxsize = 1024)
def odds_cache(odds, pool_size, copies_taken):
    return odds*(pool_size - copies_taken)/pool_size