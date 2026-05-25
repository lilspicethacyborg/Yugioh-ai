"""Data models for Yu-Gi-Oh! cards and decks."""

from __future__ import annotations
from dataclasses import dataclass, field
from enum import Enum
from typing import Optional


class BanStatus(Enum):
    UNLIMITED = "Unlimited"
    SEMI_LIMITED = "Semi-Limited"
    LIMITED = "Limited"
    BANNED = "Banned"


class CardType(Enum):
    MONSTER = "Monster"
    SPELL = "Spell"
    TRAP = "Trap"
    EXTRA_DECK = "Extra Deck"


class CardRole(Enum):
    STARTER = "Starter"
    EXTENDER = "Extender"
    SEARCHER = "Searcher"
    HANDTRAP = "Hand Trap"
    BOARD_BREAKER = "Board Breaker"
    FLOODGATE = "Floodgate"
    REMOVAL = "Removal"
    DRAW = "Draw"
    RECOVERY = "Recovery"
    PROTECTION = "Protection"
    BOSS = "Boss Monster"
    NEGATE = "Negation"
    GENERIC_SUPPORT = "Generic Support"
    ARCHETYPE_CORE = "Archetype Core"
    TECH = "Tech Choice"


class DeckType(Enum):
    COMBO = "Combo"
    CONTROL = "Control"
    MIDRANGE = "Midrange"
    AGGRO = "Aggro"
    STUN = "Stun"


EXTRA_DECK_TYPES = {
    "Fusion Monster", "Synchro Monster", "XYZ Monster", "Link Monster",
    "Synchro Tuner Monster", "Synchro Pendulum Effect Monster",
    "XYZ Pendulum Effect Monster", "Fusion Pendulum Effect Monster",
    "Link Pendulum Effect Monster",
}

MAIN_DECK_MONSTER_TYPES = {
    "Normal Monster", "Effect Monster", "Flip Effect Monster",
    "Spirit Monster", "Union Effect Monster", "Gemini Monster",
    "Tuner Monster", "Normal Tuner Monster", "Ritual Monster",
    "Ritual Effect Monster", "Pendulum Normal Monster",
    "Pendulum Effect Monster", "Pendulum Effect Ritual Monster",
    "Pendulum Tuner Effect Monster", "Pendulum Flip Effect Monster",
}


@dataclass
class Card:
    id: int
    name: str
    type: str
    desc: str
    race: str
    archetype: Optional[str] = None
    atk: Optional[int] = None
    defense: Optional[int] = None
    level: Optional[int] = None
    rank: Optional[int] = None
    link_val: Optional[int] = None
    scale: Optional[int] = None
    attribute: Optional[str] = None
    ban_tcg: BanStatus = BanStatus.UNLIMITED
    ban_ocg: BanStatus = BanStatus.UNLIMITED

    @property
    def is_extra_deck(self) -> bool:
        return self.type in EXTRA_DECK_TYPES

    @property
    def is_monster(self) -> bool:
        return self.type in MAIN_DECK_MONSTER_TYPES or self.is_extra_deck

    @property
    def is_spell(self) -> bool:
        return "Spell" in self.type and "Monster" not in self.type

    @property
    def is_trap(self) -> bool:
        return "Trap" in self.type and "Monster" not in self.type

    @property
    def is_main_deck(self) -> bool:
        return not self.is_extra_deck

    @property
    def card_category(self) -> CardType:
        if self.is_extra_deck:
            return CardType.EXTRA_DECK
        elif self.is_spell:
            return CardType.SPELL
        elif self.is_trap:
            return CardType.TRAP
        return CardType.MONSTER

    @property
    def monster_level(self) -> Optional[int]:
        return self.level or self.rank or self.link_val

    @classmethod
    def from_api(cls, data: dict) -> Card:
        ban_info = data.get("banlist_info", {})
        ban_tcg_str = ban_info.get("ban_tcg", "Unlimited")
        ban_ocg_str = ban_info.get("ban_ocg", "Unlimited")
        ban_map = {
            "Banned": BanStatus.BANNED,
            "Limited": BanStatus.LIMITED,
            "Semi-Limited": BanStatus.SEMI_LIMITED,
        }
        return cls(
            id=data["id"],
            name=data["name"],
            type=data["type"],
            desc=data.get("desc", ""),
            race=data.get("race", ""),
            archetype=data.get("archetype"),
            atk=data.get("atk"),
            defense=data.get("def"),
            level=data.get("level"),
            rank=data.get("rank"),
            link_val=data.get("linkval"),
            scale=data.get("scale"),
            attribute=data.get("attribute"),
            ban_tcg=ban_map.get(ban_tcg_str, BanStatus.UNLIMITED),
            ban_ocg=ban_map.get(ban_ocg_str, BanStatus.UNLIMITED),
        )

    def to_dict(self) -> dict:
        return {
            "id": self.id, "name": self.name, "type": self.type,
            "desc": self.desc, "race": self.race, "archetype": self.archetype,
            "atk": self.atk, "def": self.defense, "level": self.level,
            "rank": self.rank, "linkval": self.link_val, "scale": self.scale,
            "attribute": self.attribute,
            "ban_tcg": self.ban_tcg.value, "ban_ocg": self.ban_ocg.value,
        }


@dataclass
class DeckList:
    name: str = "My Deck"
    main_deck: list[tuple[Card, int]] = field(default_factory=list)
    extra_deck: list[tuple[Card, int]] = field(default_factory=list)
    side_deck: list[tuple[Card, int]] = field(default_factory=list)
    description: str = ""
    archetype: str = ""

    @property
    def main_count(self) -> int:
        return sum(c for _, c in self.main_deck)

    @property
    def extra_count(self) -> int:
        return sum(c for _, c in self.extra_deck)

    @property
    def side_count(self) -> int:
        return sum(c for _, c in self.side_deck)

    def is_valid(self, allow_forbidden: bool = False) -> tuple[bool, list[str]]:
        errors = []
        if self.main_count < 40:
            errors.append(f"Main deck has {self.main_count} cards (minimum 40)")
        if self.main_count > 60:
            errors.append(f"Main deck has {self.main_count} cards (maximum 60)")
        if self.extra_count > 15:
            errors.append(f"Extra deck has {self.extra_count} cards (maximum 15)")
        if self.side_count > 15:
            errors.append(f"Side deck has {self.side_count} cards (maximum 15)")
        for card, count in self.main_deck + self.extra_deck + self.side_deck:
            if count > 3:
                errors.append(f"{card.name} has {count} copies (maximum 3)")
            if not allow_forbidden:
                if card.ban_tcg == BanStatus.BANNED:
                    errors.append(f"{card.name} is Banned")
                if card.ban_tcg == BanStatus.LIMITED and count > 1:
                    errors.append(f"{card.name} is Limited (max 1 copy)")
                if card.ban_tcg == BanStatus.SEMI_LIMITED and count > 2:
                    errors.append(f"{card.name} is Semi-Limited (max 2 copies)")
        return (len(errors) == 0, errors)

    def to_ydk(self) -> str:
        lines = ["#created by YuGiOh AI Deck Builder"]
        lines.append("#main")
        for card, count in self.main_deck:
            for _ in range(count):
                lines.append(str(card.id))
        lines.append("#extra")
        for card, count in self.extra_deck:
            for _ in range(count):
                lines.append(str(card.id))
        lines.append("!side")
        for card, count in self.side_deck:
            for _ in range(count):
                lines.append(str(card.id))
        return "\n".join(lines)
