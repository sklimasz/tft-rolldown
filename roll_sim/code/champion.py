from __future__ import annotations

from dataclasses import KW_ONLY, dataclass


@dataclass
class Champion:
    """Champion representation."""

    _ : KW_ONLY
    name: str
    cost: str | None = None
    odds: int | float | None = None

    traits: list[str] | None = None
    headlined_trait: str | None = None
    headliner_odds: int | float | None = None

    pool_size: int = 0
    copies_taken: int = 0
    copies_held: int = 0
    copies_necessary: int = 9

    @property
    def copies_left(self) -> int:
        return self.pool_size - self.copies_taken

    def __eq__(self, other) -> bool:
        """Define equality as champions having same name and same headlined trait."""
        if isinstance(other, Champion):
            name_match = (self.name == other.name)
            if self.headlined_trait is not None and other.headlined_trait is not None:
                headlined_trait_match = (self.headlined_trait == other.headlined_trait)
                return name_match and headlined_trait_match

            return name_match
        return False

    @staticmethod
    def from_list(champions_data: list[dict]) -> list[Champion]:
        """Create list of champion objects from list of dictionares."""
        return [Champion(**champion_data) for champion_data in champions_data]
