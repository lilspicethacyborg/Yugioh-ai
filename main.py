#!/usr/bin/env python3
"""Yu-Gi-Oh! AI Deck Builder - Interactive CLI Application.

Builds intelligent, competitive Yu-Gi-Oh! decks using the full card database
from YGOPRODeck (free API). Supports archetype-based building, card synergy
analysis, slang resolution, and ban list compliance.

Usage:
    python3 main.py
"""

import sys
import os

from ygodeck.cache import CacheManager
from ygodeck.carddb import CardDatabase
from ygodeck.builder import DeckBuilder
from ygodeck.display import (
    display_deck, display_card_detail, display_ban_list,
    export_ydk, c, Colors,
)
from ygodeck.models import BanStatus


def print_banner():
    banner = r"""
    ╔══════════════════════════════════════════════════════════════╗
    ║            YU-GI-OH! AI DECK BUILDER  v1.0                 ║
    ║            Powered by YGOPRODeck Card Database              ║
    ╚══════════════════════════════════════════════════════════════╝
    """
    print(c(banner, Colors.CYAN))


def print_menu():
    print(c("  MAIN MENU", Colors.BOLD + Colors.CYAN))
    print(c("  " + "=" * 40, Colors.DIM))
    print(f"  {c('1', Colors.YELLOW)} - Build a Deck")
    print(f"  {c('2', Colors.YELLOW)} - Search Cards")
    print(f"  {c('3', Colors.YELLOW)} - View Card Details")
    print(f"  {c('4', Colors.YELLOW)} - View Ban List")
    print(f"  {c('5', Colors.YELLOW)} - List Archetypes")
    print(f"  {c('6', Colors.YELLOW)} - Refresh Card Database")
    print(f"  {c('7', Colors.YELLOW)} - Help & Tips")
    print(f"  {c('0', Colors.RED)} - Exit")
    print()


def inp(prompt: str) -> str:
    try:
        return input(c(f"  {prompt}", Colors.WHITE)).strip()
    except (EOFError, KeyboardInterrupt):
        print()
        return ""


def card_list_input(prompt: str) -> list[str]:
    raw = inp(prompt)
    return [n.strip() for n in raw.split(",") if n.strip()] if raw else []


def build_deck_interactive(builder: DeckBuilder, db: CardDatabase):
    print()
    print(c("  === DECK BUILDER ===", Colors.BOLD + Colors.CYAN))
    print()
    print(c("  Describe your deck. You can use:", Colors.DIM))
    print(c("    - Archetype names: 'Blue-Eyes', 'Branded', 'salad'", Colors.DIM))
    print(c("    - Deck styles:     'combo', 'control', 'stun', 'aggro'", Colors.DIM))
    print(c("    - Slang/nicknames: 'bewd', 'cydra', 'pk', 'ba', 'tear'", Colors.DIM))
    print()

    description = inp("Deck description or archetype: ")
    if not description:
        print(c("  No description provided.", Colors.RED))
        return

    archetype = None
    for word in description.replace(",", " ").split():
        resolved = db.resolve_archetype(word)
        if resolved:
            archetype = resolved
            break
    if not archetype:
        resolved = db.resolve_archetype(description)
        if resolved:
            archetype = resolved

    if archetype:
        print(c(f"  Detected archetype: {archetype}", Colors.GREEN))
    else:
        print(c("  No specific archetype detected - building custom deck.", Colors.YELLOW))

    print()
    print(c("  Deck style options: combo, control, midrange, aggro, stun", Colors.DIM))
    style_input = inp("Deck style (blank for auto): ")
    deck_style = style_input.upper() if style_input else None
    if deck_style and deck_style not in ("COMBO", "CONTROL", "MIDRANGE", "AGGRO", "STUN"):
        print(c(f"  Unknown style '{style_input}', using auto.", Colors.YELLOW))
        deck_style = None

    print()
    print(c("  Cards to INCLUDE (comma-separated, supports nicknames):", Colors.DIM))
    print(c("  Example: ash, imperm, called by, nibiru", Colors.DIM))
    include_cards = card_list_input("Include cards: ")
    if include_cards:
        for name in include_cards:
            card = db.resolve_card_name(name)
            if card:
                print(c(f"    '{name}' -> {card.name}", Colors.GREEN))
            else:
                print(c(f"    '{name}' -> NOT FOUND (skipping)", Colors.RED))

    print()
    print(c("  Cards to EXCLUDE (comma-separated, supports nicknames):", Colors.DIM))
    exclude_cards = card_list_input("Exclude cards: ")
    if exclude_cards:
        for name in exclude_cards:
            card = db.resolve_card_name(name)
            if card:
                print(c(f"    '{name}' -> {card.name} (excluded)", Colors.YELLOW))

    print()
    allow_forbidden = inp("Allow forbidden/banned cards? (y/N): ").lower() in ("y", "yes")

    size_input = inp("Main deck size (40-60, default 40): ")
    try:
        main_deck_size = max(40, min(60, int(size_input)))
    except (ValueError, TypeError):
        main_deck_size = 40

    print()
    print(c("  Building deck...", Colors.CYAN + Colors.BOLD))
    print()

    try:
        deck = builder.build_deck(
            description=description, archetype=archetype,
            include_cards=include_cards, exclude_cards=exclude_cards,
            allow_forbidden=allow_forbidden, deck_style=deck_style,
            main_deck_size=main_deck_size,
        )
        display_deck(deck, db=db)

        while True:
            print(c("  Options:", Colors.DIM))
            print(f"  {c('v', Colors.YELLOW)} - View detailed (with descriptions)")
            print(f"  {c('e', Colors.YELLOW)} - Export to .ydk file")
            print(f"  {c('r', Colors.YELLOW)} - Rebuild with different settings")
            print(f"  {c('b', Colors.YELLOW)} - Back to menu")
            print()
            choice = inp("Choice: ")
            if choice == "v":
                display_deck(deck, db=db, verbose=True)
            elif choice == "e":
                filename = inp("Filename (without extension): ") or "deck"
                export_ydk(deck, f"{filename}.ydk")
            elif choice == "r":
                build_deck_interactive(builder, db)
                return
            elif choice == "b" or not choice:
                return
    except Exception as e:
        print(c(f"  Error building deck: {e}", Colors.RED))
        import traceback
        traceback.print_exc()


def search_cards_interactive(db: CardDatabase):
    print()
    print(c("  === CARD SEARCH ===", Colors.BOLD + Colors.CYAN))
    print(c("  Supports nicknames and fuzzy matching", Colors.DIM))
    print()
    query = inp("Search query: ")
    if not query:
        return
    card = db.resolve_card_name(query)
    if card:
        print(c(f"\n  Best match: {card.name}", Colors.GREEN))
        display_card_detail(card, db=db)
    results = db.search_cards(query, limit=15)
    if results:
        print(c(f"  All matches ({len(results)}):", Colors.BOLD))
        for card in results:
            color = Colors.GREEN if card.is_spell else (
                Colors.MAGENTA if card.is_trap else (
                    Colors.PURPLE if card.is_extra_deck else Colors.ORANGE))
            ban = ""
            if card.ban_tcg == BanStatus.BANNED:
                ban = c(" [BANNED]", Colors.RED)
            elif card.ban_tcg == BanStatus.LIMITED:
                ban = c(" [Limited]", Colors.YELLOW)
            arch = f" ({card.archetype})" if card.archetype else ""
            print(f"    {c(card.name, color)}{c(arch, Colors.DIM)}{ban}")
        print()
        detail = inp("Enter card name for details (or blank): ")
        if detail:
            card = db.resolve_card_name(detail)
            if card:
                display_card_detail(card, db=db)
    else:
        print(c("  No results found.", Colors.RED))


def view_card_detail_interactive(db: CardDatabase):
    print()
    query = inp("Card name (supports nicknames): ")
    if not query:
        return
    card = db.resolve_card_name(query)
    if card:
        display_card_detail(card, db=db)
        related = db.find_related_cards(card, limit=10)
        if related:
            print(c("  Related Cards:", Colors.BOLD))
            for rc in related:
                arch = f" ({rc.archetype})" if rc.archetype else ""
                print(f"    {c(rc.name, _card_color(rc))}{c(arch, Colors.DIM)}")
            print()
    else:
        print(c(f"  Card '{query}' not found.", Colors.RED))


def _card_color(card):
    if card.is_extra_deck:
        return Colors.PURPLE
    if card.is_spell:
        return Colors.GREEN
    if card.is_trap:
        return Colors.MAGENTA
    return Colors.ORANGE


def view_ban_list(db: CardDatabase):
    print()
    print(c("  === TCG BAN LIST ===", Colors.BOLD + Colors.RED))
    print()
    banned = db.get_banned_cards()
    limited = db.get_limited_cards()
    semi = db.get_semi_limited_cards()
    print(f"  {c('1', Colors.YELLOW)} - Banned ({len(banned)} cards)")
    print(f"  {c('2', Colors.YELLOW)} - Limited ({len(limited)} cards)")
    print(f"  {c('3', Colors.YELLOW)} - Semi-Limited ({len(semi)} cards)")
    print(f"  {c('4', Colors.YELLOW)} - All")
    print()
    choice = inp("View: ")
    if choice == "1":
        display_ban_list(banned, "Banned")
    elif choice == "2":
        display_ban_list(limited, "Limited")
    elif choice == "3":
        display_ban_list(semi, "Semi-Limited")
    elif choice == "4":
        display_ban_list(banned, "Banned")
        display_ban_list(limited, "Limited")
        display_ban_list(semi, "Semi-Limited")


def list_archetypes(db: CardDatabase):
    print()
    query = inp("Filter archetypes (or blank for all): ")
    archetypes = sorted(db._by_archetype.keys())
    if query:
        archetypes = [a for a in archetypes if query.lower() in a.lower()]
    print()
    print(c(f"  Archetypes ({len(archetypes)}):", Colors.BOLD + Colors.CYAN))
    print(c("  " + "-" * 50, Colors.DIM))
    col_width = 30
    for i in range(0, len(archetypes), 2):
        row = archetypes[i:i + 2]
        line = "  " + "".join(f"{a} ({len(db._by_archetype.get(a, []))})".ljust(col_width) for a in row)
        print(line)
    print()


def show_help():
    print()
    print(c("  === HELP & TIPS ===", Colors.BOLD + Colors.CYAN))
    print()
    print(c("  BUILDING DECKS:", Colors.BOLD))
    print("  - Enter an archetype name or deck description when prompted")
    print("  - Slang works: 'salad' = Salamangreat, 'ba' = Burning Abyss")
    print("  - Card nicknames: 'ash' = Ash Blossom, 'nib' = Nibiru")
    print("  - Styles: combo, control, midrange, aggro, stun")
    print("  - Include/exclude cards using comma-separated names")
    print()
    print(c("  DECK STYLES:", Colors.BOLD))
    print("  - COMBO:    Maximize combo pieces, strong going first")
    print("  - CONTROL:  Trap-heavy, grind game")
    print("  - MIDRANGE: Balanced, flexible approach")
    print("  - AGGRO:    Going-second OTK, board breakers")
    print("  - STUN:     Floodgate-heavy, restrict opponent")
    print()
    print(c("  SLANG EXAMPLES:", Colors.BOLD))
    print("  Hand traps: ash, veiler, nib, imperm, maxx c, droll, ogre")
    print("  Spells: hfd, mst, called by, cbtg, rota, foolish, super poly")
    print("  Traps: strike, judgment, torrential, bottomless, evenly")
    print("  Extra: accesscode, baronne, savage, zeus, masquerena, ip")
    print("  Archetypes: salad, ba, pk, cydra, bewd, thundra, tear, lab")
    print()
    print(c("  EXPORT:", Colors.BOLD))
    print("  - .ydk files work with EDOPro, YGOPro, Dueling Book, etc.")
    print()
    print(c("  DATA:", Colors.BOLD))
    print("  - Card data from YGOPRODeck API (free, auto-cached)")
    print("  - 200+ popular cards bundled for offline use")
    print("  - Use option 6 to refresh card data")
    print()


def main():
    print_banner()
    print(c("  Initializing...", Colors.CYAN))

    cache = CacheManager()
    print(f"  Cache last updated: {cache.cache_age_str()}")

    try:
        cards = cache.load_cards()
        archetypes = cache.load_archetypes()
    except Exception as e:
        print(c(f"  Error: {e}", Colors.RED))
        print(c("  Trying fresh download...", Colors.YELLOW))
        try:
            cache.refresh()
            cards = cache.load_cards()
            archetypes = cache.load_archetypes()
        except Exception:
            print(c("  Using bundled card database.", Colors.YELLOW))
            cards = cache._load_bundled()
            archetypes = []

    db = CardDatabase(cards, archetypes)
    builder = DeckBuilder(db)
    print(c(f"  Ready! {len(cards)} cards, {len(db._by_archetype)} archetypes loaded.", Colors.GREEN))
    print()

    while True:
        print_menu()
        choice = inp("Select option: ")
        if choice == "1":
            build_deck_interactive(builder, db)
        elif choice == "2":
            search_cards_interactive(db)
        elif choice == "3":
            view_card_detail_interactive(db)
        elif choice == "4":
            view_ban_list(db)
        elif choice == "5":
            list_archetypes(db)
        elif choice == "6":
            print(c("  Refreshing...", Colors.CYAN))
            try:
                cache.refresh()
                cards = cache.load_cards()
                archetypes = cache.load_archetypes()
                db = CardDatabase(cards, archetypes)
                builder = DeckBuilder(db)
                print(c(f"  Done! {len(cards)} cards loaded.", Colors.GREEN))
            except Exception as e:
                print(c(f"  Error: {e}", Colors.RED))
        elif choice == "7":
            show_help()
        elif choice == "0":
            print(c("\n  Thanks for using Yu-Gi-Oh! AI Deck Builder!", Colors.CYAN))
            print(c("  It's time to d-d-d-duel!\n", Colors.BOLD + Colors.YELLOW))
            break
        elif choice:
            print(c(f"  Unknown option: {choice}", Colors.RED))


if __name__ == "__main__":
    main()
