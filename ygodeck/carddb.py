"""Card database - in-memory indexed card collection with search capabilities."""

from __future__ import annotations
import re
from typing import Optional
from rapidfuzz import fuzz, process

from .models import Card, BanStatus
from .slang import resolve_slang, resolve_archetype_alias
from .roles import classify_card, role_priority_score, CardRole


class CardDatabase:
    def __init__(self, cards: list[Card], archetypes: list[str]):
        self.cards = cards
        self.archetypes = archetypes
        self._by_name: dict[str, Card] = {}
        self._by_id: dict[int, Card] = {}
        self._by_archetype: dict[str, list[Card]] = {}
        self._name_lower_map: dict[str, Card] = {}
        self._card_roles: dict[str, list[CardRole]] = {}
        self._card_scores: dict[str, float] = {}
        self._roles_built = False
        self._build_indexes()

    def _build_indexes(self):
        for card in self.cards:
            self._by_name[card.name] = card
            self._by_id[card.id] = card
            self._name_lower_map[card.name.lower()] = card
            if card.archetype:
                self._by_archetype.setdefault(card.archetype, []).append(card)

    def _ensure_roles(self):
        if self._roles_built:
            return
        for card in self.cards:
            roles = classify_card(card)
            self._card_roles[card.name] = roles
            self._card_scores[card.name] = role_priority_score(card, roles)
        self._roles_built = True

    def get_card(self, name: str) -> Optional[Card]:
        return self._by_name.get(name)

    def resolve_card_name(self, query: str) -> Optional[Card]:
        card = self._by_name.get(query)
        if card:
            return card
        card = self._name_lower_map.get(query.lower())
        if card:
            return card
        resolved = resolve_slang(query)
        if resolved and not resolved.startswith("_ROLE_"):
            card = self._by_name.get(resolved)
            if card:
                return card
        return self._fuzzy_match(query)

    def _fuzzy_match(self, query: str, threshold: int = 70) -> Optional[Card]:
        all_names = list(self._by_name.keys())
        if not all_names:
            return None
        result = process.extractOne(query, all_names, scorer=fuzz.token_sort_ratio, score_cutoff=threshold)
        if result:
            return self._by_name[result[0]]
        return None

    def search_cards(self, query: str, limit: int = 20) -> list[Card]:
        all_names = list(self._by_name.keys())
        results = process.extract(query, all_names, scorer=fuzz.token_sort_ratio, limit=limit)
        return [self._by_name[name] for name, score, _ in results if score > 50]

    def get_archetype_cards(self, archetype: str) -> list[Card]:
        cards = self._by_archetype.get(archetype, [])
        if cards:
            return cards
        resolved = resolve_archetype_alias(archetype)
        if resolved:
            cards = self._by_archetype.get(resolved, [])
            if cards:
                return cards
        best = process.extractOne(archetype, list(self._by_archetype.keys()), scorer=fuzz.token_sort_ratio, score_cutoff=60)
        if best:
            return self._by_archetype.get(best[0], [])
        return []

    def resolve_archetype(self, query: str) -> Optional[str]:
        if query in self._by_archetype:
            return query
        resolved = resolve_archetype_alias(query)
        if resolved and resolved in self._by_archetype:
            return resolved
        best = process.extractOne(query, list(self._by_archetype.keys()), scorer=fuzz.token_sort_ratio, score_cutoff=60)
        if best:
            return best[0]
        return None

    def get_card_roles(self, card: Card) -> list[CardRole]:
        self._ensure_roles()
        return self._card_roles.get(card.name, [CardRole.GENERIC_SUPPORT])

    def get_card_score(self, card: Card) -> float:
        self._ensure_roles()
        return self._card_scores.get(card.name, 0.0)

    def get_cards_by_role(self, role: CardRole, archetype: Optional[str] = None) -> list[Card]:
        self._ensure_roles()
        cards = self._by_archetype.get(archetype, self.cards) if archetype else self.cards
        return [c for c in cards if role in self._card_roles.get(c.name, [])]

    def get_banned_cards(self) -> list[Card]:
        return [c for c in self.cards if c.ban_tcg == BanStatus.BANNED]

    def get_limited_cards(self) -> list[Card]:
        return [c for c in self.cards if c.ban_tcg == BanStatus.LIMITED]

    def get_semi_limited_cards(self) -> list[Card]:
        return [c for c in self.cards if c.ban_tcg == BanStatus.SEMI_LIMITED]

    def filter_cards(self, archetype: Optional[str] = None, card_type: Optional[str] = None,
                     attribute: Optional[str] = None, race: Optional[str] = None,
                     main_deck_only: bool = False, extra_deck_only: bool = False,
                     exclude_banned: bool = True, text_search: Optional[str] = None) -> list[Card]:
        results = self.cards
        if archetype:
            resolved = self.resolve_archetype(archetype)
            results = [c for c in results if c.archetype == resolved] if resolved else []
        if card_type:
            results = [c for c in results if card_type.lower() in c.type.lower()]
        if attribute:
            results = [c for c in results if c.attribute and c.attribute.upper() == attribute.upper()]
        if race:
            results = [c for c in results if c.race and c.race.lower() == race.lower()]
        if main_deck_only:
            results = [c for c in results if c.is_main_deck]
        if extra_deck_only:
            results = [c for c in results if c.is_extra_deck]
        if exclude_banned:
            results = [c for c in results if c.ban_tcg != BanStatus.BANNED]
        if text_search:
            pattern = re.compile(re.escape(text_search), re.IGNORECASE)
            results = [c for c in results if pattern.search(c.desc)]
        return results

    def find_related_cards(self, card: Card, limit: int = 20) -> list[Card]:
        related = []
        if card.archetype:
            for c in self._by_archetype.get(card.archetype, []):
                if c.name != card.name:
                    related.append(c)
        for other in self.cards:
            if other.name != card.name and len(other.name) > 3 and other.name in card.desc:
                if other not in related:
                    related.append(other)
        return related[:limit]
