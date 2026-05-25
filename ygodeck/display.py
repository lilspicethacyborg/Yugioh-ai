"""Display and export utilities for deck lists."""

from __future__ import annotations
import os
from .models import Card, DeckList, BanStatus, CardRole


class Colors:
    RESET = "\033[0m"
    BOLD = "\033[1m"
    DIM = "\033[2m"
    RED = "\033[91m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    BLUE = "\033[94m"
    MAGENTA = "\033[95m"
    CYAN = "\033[96m"
    WHITE = "\033[97m"
    ORANGE = "\033[38;5;208m"
    PURPLE = "\033[38;5;135m"


USE_COLOR = os.environ.get("TERM", "") != "dumb" and hasattr(os, "isatty") and os.isatty(1)


def c(text: str, color: str) -> str:
    return f"{color}{text}{Colors.RESET}" if USE_COLOR else text


def _card_color(card: Card) -> str:
    if card.is_extra_deck:
        return Colors.PURPLE
    if card.is_spell:
        return Colors.GREEN
    if card.is_trap:
        return Colors.MAGENTA
    return Colors.ORANGE


def _ban_str(card: Card) -> str:
    if card.ban_tcg == BanStatus.BANNED:
        return c(" [BANNED]", Colors.RED)
    if card.ban_tcg == BanStatus.LIMITED:
        return c(" [Limited]", Colors.YELLOW)
    if card.ban_tcg == BanStatus.SEMI_LIMITED:
        return c(" [Semi]", Colors.CYAN)
    return ""


def display_card_line(card: Card, count: int = 1, show_desc: bool = False, db=None) -> str:
    color = _card_color(card)
    count_str = f"{count}x " if count > 1 else "   "
    name = c(card.name, color)
    ban = _ban_str(card)
    parts = []
    if card.is_monster:
        if card.attribute:
            parts.append(card.attribute)
        if card.race:
            parts.append(card.race)
        if card.link_val:
            parts.append(f"Link-{card.link_val}")
        elif card.rank:
            parts.append(f"Rank {card.rank}")
        elif card.level:
            parts.append(f"Lv.{card.level}")
        if card.atk is not None:
            atk = str(card.atk)
            dfn = str(card.defense) if card.defense is not None else "?"
            parts.append(f"{atk}/{dfn}" if "Link" not in card.type else f"ATK {atk}")
    elif card.is_spell:
        parts.append(f"{card.race} Spell")
    elif card.is_trap:
        parts.append(f"{card.race} Trap")
    type_short = c(f" [{' / '.join(parts)}]", Colors.DIM) if parts else ""
    roles_str = ""
    if db:
        roles = db.get_card_roles(card)
        if roles:
            roles_str = c(f" ({', '.join(r.value for r in roles[:3])})", Colors.DIM)
    line = f"  {count_str}{name}{type_short}{ban}{roles_str}"
    if show_desc and card.desc:
        desc = card.desc[:200] + ("..." if len(card.desc) > 200 else "")
        line += f"\n        {c(desc, Colors.DIM)}"
    return line


def display_deck(deck: DeckList, db=None, verbose: bool = False):
    print()
    print(c("=" * 70, Colors.BLUE))
    print(c(f"  DECK: {deck.name}", Colors.BOLD + Colors.CYAN))
    if deck.description:
        print(c(f"  {deck.description}", Colors.DIM))
    if deck.archetype:
        print(c(f"  Archetype: {deck.archetype}", Colors.DIM))
    print(c("=" * 70, Colors.BLUE))

    monsters = [(cd, cnt) for cd, cnt in deck.main_deck if cd.is_monster]
    spells = [(cd, cnt) for cd, cnt in deck.main_deck if cd.is_spell]
    traps = [(cd, cnt) for cd, cnt in deck.main_deck if cd.is_trap]
    mc = sum(n for _, n in monsters)
    sc = sum(n for _, n in spells)
    tc = sum(n for _, n in traps)

    print()
    print(c(f"  MAIN DECK ({deck.main_count} cards)", Colors.BOLD))
    print(c(f"  Monsters: {mc} | Spells: {sc} | Traps: {tc}", Colors.DIM))
    print(c("  " + "-" * 40, Colors.DIM))

    if monsters:
        print(c(f"\n  Monsters ({mc}):", Colors.BOLD + Colors.ORANGE))
        for cd, cnt in monsters:
            print(display_card_line(cd, cnt, show_desc=verbose, db=db))
    if spells:
        print(c(f"\n  Spells ({sc}):", Colors.BOLD + Colors.GREEN))
        for cd, cnt in spells:
            print(display_card_line(cd, cnt, show_desc=verbose, db=db))
    if traps:
        print(c(f"\n  Traps ({tc}):", Colors.BOLD + Colors.MAGENTA))
        for cd, cnt in traps:
            print(display_card_line(cd, cnt, show_desc=verbose, db=db))

    if deck.extra_deck:
        print()
        print(c(f"  EXTRA DECK ({deck.extra_count} cards)", Colors.BOLD + Colors.PURPLE))
        print(c("  " + "-" * 40, Colors.DIM))
        for cd, cnt in deck.extra_deck:
            print(display_card_line(cd, cnt, show_desc=verbose, db=db))

    print()
    valid, errors = deck.is_valid()
    if valid:
        print(c("  Deck is VALID", Colors.GREEN + Colors.BOLD))
    else:
        print(c("  Deck has issues:", Colors.RED + Colors.BOLD))
        for err in errors:
            print(c(f"    - {err}", Colors.RED))
    print(c("=" * 70, Colors.BLUE))
    print()


def export_ydk(deck: DeckList, filepath: str):
    with open(filepath, "w") as f:
        f.write(deck.to_ydk())
    print(c(f"  Deck exported to: {filepath}", Colors.GREEN))


def display_card_detail(card: Card, db=None):
    print()
    print(c(f"  {card.name}", Colors.BOLD + _card_color(card)))
    print(c("  " + "-" * 50, Colors.DIM))
    print(f"  Type: {card.type}")
    if card.is_monster:
        for label, val in [("Attribute", card.attribute), ("Race", card.race),
                           ("Level", card.level), ("Rank", card.rank),
                           ("Link", card.link_val), ("Scale", card.scale)]:
            if val is not None:
                print(f"  {label}: {val}")
        if card.atk is not None:
            print(f"  ATK: {card.atk}")
        if card.defense is not None:
            print(f"  DEF: {card.defense}")
    if card.archetype:
        print(f"  Archetype: {card.archetype}")
    print(f"  Ban Status (TCG): {card.ban_tcg.value}")
    print()
    if card.desc:
        words = card.desc.split()
        line = "  "
        for word in words:
            if len(line) + len(word) > 75:
                print(line)
                line = "  " + word
            else:
                line += (" " + word) if line.strip() else ("  " + word)
        if line.strip():
            print(line)
    if db:
        roles = db.get_card_roles(card)
        if roles:
            print()
            print(c(f"  Roles: {', '.join(r.value for r in roles)}", Colors.CYAN))
            print(c(f"  Score: {db.get_card_score(card):.1f}", Colors.DIM))
    print()


def display_ban_list(cards: list[Card], category: str = "Banned"):
    print()
    print(c(f"  {category} Cards ({len(cards)})", Colors.BOLD + Colors.RED))
    print(c("  " + "-" * 50, Colors.DIM))
    for card in sorted(cards, key=lambda x: x.name):
        print(f"  {c(card.name, _card_color(card))} - {c(card.type, Colors.DIM)}")
    print()
