# Yu-Gi-Oh! AI Deck Builder

An intelligent Yu-Gi-Oh! deck builder that constructs competitive decks using the complete YGOPRODeck card database (13,000+ cards). Free to use forever — no API keys, no accounts, no subscriptions.

## Quick Start

```bash
# Install dependencies
pip3 install -r requirements.txt

# Run the deck builder
python3 main.py
```

Or use the setup script:
```bash
chmod +x setup.sh && ./setup.sh
python3 main.py
```

## Features

- **Full Card Database**: Downloads and caches the entire Yu-Gi-Oh! card database from YGOPRODeck (free API). 200+ popular cards bundled for offline use.
- **Current Ban List**: Automatically uses the latest TCG ban list. Option to allow forbidden cards.
- **Intelligent Deck Design**: Card role classification (searcher, starter, extender, hand trap, boss, etc.), synergy analysis, and optimized deck ratios.
- **5 Deck Styles**: Combo, Control, Midrange, Aggro, and Stun — each with tailored card ratios and staple selection.
- **Archetype Awareness**: Knows archetype cores, support cards, and cross-archetype engines.
- **Yu-Gi-Oh! Slang**: Understands community nicknames — `ash`, `nib`, `imperm`, `cbtg`, `salad`, `ba`, `tear`, `cydra`, and 100+ more.
- **Fuzzy Card Search**: Find cards even with typos or partial names.
- **YDK Export**: Export decks to `.ydk` format for EDOPro, YGOPro, Dueling Book, and other simulators.
- **Include/Exclude Cards**: Force specific cards in or out of your deck.

## How It Works

1. **Specify your deck**: Enter an archetype name (or slang), pick a deck style, and optionally include/exclude specific cards.
2. **AI builds the deck**: The engine identifies archetype core cards, scores them by role/importance, fills with appropriate generic staples (hand traps, board breakers, draw spells), and builds a matching extra deck.
3. **Review and export**: View the full deck list with card types, roles, and ban status. Export to `.ydk` for use in simulators.

## Deck Styles

| Style | Description |
|-------|-------------|
| **Combo** | Maximize combo pieces, strong going first. 6-12 hand traps, minimal traps. |
| **Control** | Trap-heavy, grind game. 8-16 traps, strong negation. |
| **Midrange** | Balanced, flexible approach. Good going first or second. |
| **Aggro** | Going-second OTK strategy. Board breakers, aggressive monsters. |
| **Stun** | Floodgate-heavy. Restrict opponent's plays with continuous traps. |

## Slang Reference

| Slang | Card |
|-------|------|
| ash | Ash Blossom & Joyous Spring |
| nib | Nibiru, the Primal Being |
| imperm | Infinite Impermanence |
| veiler | Effect Veiler |
| cbtg / called by | Called by the Grave |
| hfd | Harpie's Feather Duster |
| droplet | Forbidden Droplet |
| baronne | Baronne de Fleur |
| zeus | Divine Arsenal AA-ZEUS - Sky Thunder |
| salad | Salamangreat |
| ba | Burning Abyss |
| pk | The Phantom Knights |
| tear | Tearlaments |
| lab | Labrynth |

...and 100+ more. See `ygodeck/slang.py` for the full dictionary.

## Data Source

Card data is provided by [YGOPRODeck](https://ygoprodeck.com/) via their free public API. Data is cached locally for 7 days and can be refreshed from the app menu.

## Requirements

- Python 3.9+
- `requests` (HTTP client)
- `rapidfuzz` (fuzzy string matching)

## License

MIT
