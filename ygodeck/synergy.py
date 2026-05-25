"""Card synergy analysis engine."""

from __future__ import annotations
import re
from typing import Optional
from .models import Card, BanStatus, CardRole


class SynergyEngine:
    def __init__(self, carddb):
        self.db = carddb
        self._archetype_text_cards: dict[str, list[Card]] = {}

    def find_archetype_support(self, archetype: str) -> list[Card]:
        if archetype in self._archetype_text_cards:
            return self._archetype_text_cards[archetype]
        pattern = re.compile(re.escape(archetype), re.IGNORECASE)
        support = [c for c in self.db.cards if c.archetype != archetype and pattern.search(c.desc)]
        self._archetype_text_cards[archetype] = support
        return support

    def score_card_for_deck(self, card: Card, archetype: Optional[str],
                            deck_cards: list[Card], deck_style: str,
                            exclude_banned: bool = True) -> float:
        if exclude_banned and card.ban_tcg == BanStatus.BANNED:
            return -1.0
        score = 0.0
        roles = self.db.get_card_roles(card)

        if archetype and card.archetype == archetype:
            score += 20.0
        if archetype and archetype.lower() in card.desc.lower():
            score += 10.0

        for dc in deck_cards:
            if len(dc.name) > 3 and dc.name in card.desc:
                score += 5.0
            if len(card.name) > 3 and card.name in dc.desc:
                score += 5.0

        style_bonuses = {
            "COMBO": {CardRole.STARTER: 8, CardRole.EXTENDER: 7, CardRole.SEARCHER: 9, CardRole.HANDTRAP: 4, CardRole.NEGATE: 6, CardRole.BOSS: 7},
            "CONTROL": {CardRole.STARTER: 6, CardRole.SEARCHER: 7, CardRole.HANDTRAP: 6, CardRole.NEGATE: 8, CardRole.FLOODGATE: 7, CardRole.REMOVAL: 6, CardRole.BOSS: 5},
            "MIDRANGE": {CardRole.STARTER: 7, CardRole.SEARCHER: 8, CardRole.HANDTRAP: 5, CardRole.NEGATE: 7, CardRole.BOSS: 6},
            "AGGRO": {CardRole.STARTER: 8, CardRole.EXTENDER: 7, CardRole.SEARCHER: 8, CardRole.BOARD_BREAKER: 7},
            "STUN": {CardRole.STARTER: 6, CardRole.FLOODGATE: 9, CardRole.SEARCHER: 7, CardRole.NEGATE: 7, CardRole.DRAW: 6},
        }
        bonuses = style_bonuses.get(deck_style, style_bonuses["MIDRANGE"])
        for role in roles:
            score += bonuses.get(role, 1.0)

        score += self.db.get_card_score(card) * 0.5
        return score

    def get_compatible_extra_deck(self, main_deck: list[Card], archetype: Optional[str] = None) -> dict:
        has_tuners = any("Tuner" in c.type for c in main_deck)
        levels = {c.monster_level for c in main_deck if c.is_monster and c.monster_level}
        has_fusion_support = any("Fusion" in c.desc or "Polymerization" in c.name for c in main_deck)
        return {
            "summoning_methods": {
                "link": True,
                "xyz": len(levels) > 0,
                "synchro": has_tuners,
                "fusion": has_fusion_support,
            },
            "levels": levels,
            "has_tuners": has_tuners,
        }
