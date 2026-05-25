"""Main deck builder engine - intelligent Yu-Gi-Oh! deck construction."""

from __future__ import annotations
from typing import Optional

from .models import Card, DeckList, BanStatus, CardRole
from .carddb import CardDatabase
from .synergy import SynergyEngine
from .roles import KNOWN_HANDTRAPS
from .staples import (
    HANDTRAPS, BOARD_BREAKERS, ANTI_HANDTRAPS, GOING_FIRST_TRAPS,
    FLOODGATES, POT_SPELLS, EXTRA_DECK_STAPLES,
    get_deck_ratios, get_archetype_style,
)


class DeckBuilder:
    def __init__(self, carddb: CardDatabase):
        self.db = carddb
        self.synergy = SynergyEngine(carddb)

    def build_deck(self, description: str = "", archetype: Optional[str] = None,
                   include_cards: Optional[list[str]] = None,
                   exclude_cards: Optional[list[str]] = None,
                   allow_forbidden: bool = False, deck_style: Optional[str] = None,
                   main_deck_size: int = 40) -> DeckList:
        include_cards = include_cards or []
        exclude_cards = exclude_cards or []

        resolved_archetype = None
        if archetype:
            resolved_archetype = self.db.resolve_archetype(archetype)

        if not deck_style:
            deck_style = get_archetype_style(resolved_archetype) if resolved_archetype else "MIDRANGE"

        exclude_set = set()
        for name in exclude_cards:
            card = self.db.resolve_card_name(name)
            if card:
                exclude_set.add(card.name)

        main_cards: dict[str, tuple[Card, int]] = {}
        extra_cards: dict[str, tuple[Card, int]] = {}

        # Step 1: Forced includes
        for name in include_cards:
            card = self.db.resolve_card_name(name)
            if card and card.name not in exclude_set:
                mc = self._max_copies(card, allow_forbidden)
                if mc > 0:
                    target = extra_cards if card.is_extra_deck else main_cards
                    target[card.name] = (card, min(3, mc))

        # Step 2: Archetype core
        if resolved_archetype:
            self._add_archetype_core(resolved_archetype, main_cards, extra_cards,
                                     exclude_set, allow_forbidden, deck_style, main_deck_size)

        # Step 3: Generic staples
        self._fill_staples(main_cards, extra_cards, exclude_set,
                          allow_forbidden, deck_style, main_deck_size, resolved_archetype)

        # Step 4: Extra deck
        self._fill_extra_deck(main_cards, extra_cards, exclude_set,
                             allow_forbidden, resolved_archetype)

        # Step 5: Adjust to target size
        self._adjust_deck_size(main_cards, main_deck_size, allow_forbidden)

        deck = DeckList(
            name=f"{resolved_archetype or 'Custom'} Deck",
            archetype=resolved_archetype or "",
            description=description,
        )
        deck.main_deck = sorted(main_cards.values(), key=lambda x: (
            0 if x[0].is_monster else (1 if x[0].is_spell else 2),
            -self.db.get_card_score(x[0]), x[0].name))
        deck.extra_deck = sorted(extra_cards.values(), key=lambda x: (
            x[0].type, -(x[0].monster_level or 0), x[0].name))
        return deck

    def _max_copies(self, card: Card, allow_forbidden: bool) -> int:
        if allow_forbidden:
            return 3
        if card.ban_tcg == BanStatus.BANNED:
            return 0
        if card.ban_tcg == BanStatus.LIMITED:
            return 1
        if card.ban_tcg == BanStatus.SEMI_LIMITED:
            return 2
        return 3

    def _main_count(self, d: dict) -> int:
        return sum(c for _, c in d.values())

    def _extra_count(self, d: dict) -> int:
        return sum(c for _, c in d.values())

    def _try_add(self, card: Card, count: int, main_cards: dict, extra_cards: dict,
                 exclude_set: set, allow_forbidden: bool, main_limit: int = 60) -> bool:
        if card.name in exclude_set:
            return False
        mc = self._max_copies(card, allow_forbidden)
        if mc == 0:
            return False
        count = min(count, mc)
        if card.is_extra_deck:
            if card.name in extra_cards or self._extra_count(extra_cards) + count > 15:
                return False
            extra_cards[card.name] = (card, count)
        else:
            if card.name in main_cards or self._main_count(main_cards) + count > main_limit:
                return False
            main_cards[card.name] = (card, count)
        return True

    def _add_archetype_core(self, archetype, main_cards, extra_cards,
                            exclude_set, allow_forbidden, deck_style, main_deck_size):
        arch_cards = self.db.get_archetype_cards(archetype)
        if not arch_cards:
            return

        scored = []
        for card in arch_cards:
            if card.name in exclude_set or card.name in main_cards or card.name in extra_cards:
                continue
            if not allow_forbidden and card.ban_tcg == BanStatus.BANNED:
                continue
            score = self._score_archetype_card(card, archetype, deck_style)
            scored.append((card, score))
        scored.sort(key=lambda x: -x[1])

        target_arch = int(main_deck_size * 0.7)
        added = 0
        for card, score in scored:
            if added >= target_arch and card.is_main_deck:
                break
            copies = self._ideal_copies(card, archetype, deck_style, allow_forbidden, score)
            if self._try_add(card, copies, main_cards, extra_cards, exclude_set,
                           allow_forbidden, main_deck_size + 5):
                if card.is_main_deck:
                    added += copies

        # Non-archetype support mentioning this archetype
        support = self.synergy.find_archetype_support(archetype)
        sup_scored = []
        for card in support:
            if card.name in exclude_set or card.name in main_cards or card.name in extra_cards:
                continue
            if not allow_forbidden and card.ban_tcg == BanStatus.BANNED:
                continue
            s = self.synergy.score_card_for_deck(card, archetype,
                [c for c, _ in main_cards.values()], deck_style)
            sup_scored.append((card, s))
        sup_scored.sort(key=lambda x: -x[1])
        for card, score in sup_scored[:6]:
            if score < 15:
                break
            copies = self._ideal_copies(card, archetype, deck_style, allow_forbidden, score)
            self._try_add(card, copies, main_cards, extra_cards, exclude_set,
                         allow_forbidden, main_deck_size + 5)

    def _score_archetype_card(self, card, archetype, deck_style):
        score = 0.0
        roles = self.db.get_card_roles(card)
        desc_lower = card.desc.lower()
        arch_lower = archetype.lower()
        score += desc_lower.count(arch_lower) * 3.0
        role_bonuses = {
            CardRole.SEARCHER: 15, CardRole.STARTER: 12, CardRole.BOSS: 10,
            CardRole.NEGATE: 8, CardRole.EXTENDER: 7, CardRole.RECOVERY: 4,
        }
        for r in roles:
            score += role_bonuses.get(r, 0)
        if card.is_spell and card.race == "Field":
            score += 8.0
        if card.is_extra_deck:
            score += 5.0
            if CardRole.BOSS in roles or CardRole.NEGATE in roles:
                score += 5.0
        if "add" in desc_lower and "deck" in desc_lower and "hand" in desc_lower:
            score += 6.0
        return score

    def _ideal_copies(self, card, archetype, deck_style, allow_forbidden, score=0):
        mc = self._max_copies(card, allow_forbidden)
        if mc == 0:
            return 0
        if card.is_extra_deck:
            return 1
        roles = self.db.get_card_roles(card)
        # Archetype cards: prefer 3 copies for important ones
        if archetype and card.archetype == archetype:
            if score >= 15:
                return min(3, mc)
            if score >= 8:
                return min(2, mc)
            return min(1, mc)
        if CardRole.SEARCHER in roles or CardRole.STARTER in roles:
            return min(3, mc)
        if CardRole.HANDTRAP in roles:
            return min(3, mc)
        if CardRole.BOSS in roles:
            return min(1, mc)
        return min(2, mc)

    def _fill_staples(self, main_cards, extra_cards, exclude_set,
                      allow_forbidden, deck_style, main_deck_size, archetype):
        current_ht = sum(c for n, (card, c) in main_cards.items()
                        if card.name in KNOWN_HANDTRAPS or
                        CardRole.HANDTRAP in self.db.get_card_roles(card))
        ratios = get_deck_ratios(deck_style)
        ht_target = ratios["handtraps"][0]

        if current_ht < ht_target:
            self._add_from_list(HANDTRAPS, ht_target - current_ht,
                               main_cards, extra_cards, exclude_set, allow_forbidden, main_deck_size)

        if deck_style in ("COMBO", "AGGRO"):
            self._add_from_list(ANTI_HANDTRAPS, 2, main_cards, extra_cards,
                               exclude_set, allow_forbidden, main_deck_size)

        if deck_style in ("AGGRO", "MIDRANGE"):
            self._add_from_list(BOARD_BREAKERS, 3, main_cards, extra_cards,
                               exclude_set, allow_forbidden, main_deck_size)

        self._add_from_list(POT_SPELLS, 1, main_cards, extra_cards,
                           exclude_set, allow_forbidden, main_deck_size)

        if deck_style in ("CONTROL", "STUN"):
            self._add_from_list(GOING_FIRST_TRAPS, 4, main_cards, extra_cards,
                               exclude_set, allow_forbidden, main_deck_size)

        if deck_style == "STUN":
            self._add_from_list(FLOODGATES, 6, main_cards, extra_cards,
                               exclude_set, allow_forbidden, main_deck_size)

        # Final fill if still below target
        current = self._main_count(main_cards)
        if current < main_deck_size:
            self._add_from_list(HANDTRAPS, main_deck_size - current,
                               main_cards, extra_cards, exclude_set, allow_forbidden, main_deck_size)
        current = self._main_count(main_cards)
        if current < main_deck_size:
            self._add_from_list(BOARD_BREAKERS, main_deck_size - current,
                               main_cards, extra_cards, exclude_set, allow_forbidden, main_deck_size)

    def _add_from_list(self, staple_list, target_count, main_cards, extra_cards,
                       exclude_set, allow_forbidden, main_deck_size):
        added = 0
        for name, default_copies, _desc in staple_list:
            if added >= target_count:
                break
            card = self.db.get_card(name)
            if not card or card.name in main_cards or card.name in extra_cards:
                continue
            copies = min(default_copies, self._max_copies(card, allow_forbidden))
            copies = min(copies, target_count - added)
            if copies > 0 and self._try_add(card, copies, main_cards, extra_cards,
                                           exclude_set, allow_forbidden, main_deck_size):
                added += copies

    def _fill_extra_deck(self, main_cards, extra_cards, exclude_set,
                         allow_forbidden, archetype):
        if self._extra_count(extra_cards) >= 15:
            return
        main_list = [c for c, _ in main_cards.values()]
        compat = self.synergy.get_compatible_extra_deck(main_list, archetype)
        methods = compat["summoning_methods"]

        for method in ["link", "xyz", "synchro", "fusion"]:
            if not methods.get(method, False):
                continue
            for name, copies, _desc in EXTRA_DECK_STAPLES.get(method, []):
                if self._extra_count(extra_cards) >= 15:
                    break
                card = self.db.get_card(name)
                if card:
                    self._try_add(card, copies, main_cards, extra_cards,
                                 exclude_set, allow_forbidden)

    def _adjust_deck_size(self, main_cards, target, allow_forbidden):
        # Trim excess
        while self._main_count(main_cards) > target:
            lowest_name = min(main_cards, key=lambda n: self.db.get_card_score(main_cards[n][0]))
            card, count = main_cards[lowest_name]
            if count > 1:
                main_cards[lowest_name] = (card, count - 1)
            else:
                del main_cards[lowest_name]

        # Fill deficit with highest-scored available cards
        while self._main_count(main_cards) < target:
            best_card, best_score = None, -1
            for card in self.db.cards:
                if card.name in main_cards or card.is_extra_deck:
                    continue
                if not allow_forbidden and card.ban_tcg == BanStatus.BANNED:
                    continue
                roles = self.db.get_card_roles(card)
                if roles == [CardRole.GENERIC_SUPPORT]:
                    continue
                score = self.db.get_card_score(card)
                if score > best_score:
                    best_score = score
                    best_card = card
            if best_card:
                copies = min(self._max_copies(best_card, allow_forbidden), target - self._main_count(main_cards))
                main_cards[best_card.name] = (best_card, copies)
            else:
                break

    def build_deck_from_description(self, description: str,
                                    include_cards=None, exclude_cards=None,
                                    allow_forbidden: bool = False) -> DeckList:
        from .slang import detect_deck_style
        archetype = None
        deck_style = detect_deck_style(description)

        for arch in sorted(self.db._by_archetype.keys(), key=len, reverse=True):
            if arch.lower() in description.lower():
                archetype = arch
                break
        if not archetype:
            for word in description.split():
                resolved = self.db.resolve_archetype(word)
                if resolved:
                    archetype = resolved
                    break

        return self.build_deck(description=description, archetype=archetype,
                              include_cards=include_cards, exclude_cards=exclude_cards,
                              allow_forbidden=allow_forbidden, deck_style=deck_style)
