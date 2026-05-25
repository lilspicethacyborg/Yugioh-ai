"""Local caching for card data to avoid repeated API calls."""

import json
import os
import time
from pathlib import Path

from .models import Card, BanStatus

CACHE_DIR = Path.home() / ".ygodeck_cache"
CARDS_CACHE = CACHE_DIR / "cards.json"
ARCHETYPES_CACHE = CACHE_DIR / "archetypes.json"
META_CACHE = CACHE_DIR / "meta.json"
CACHE_MAX_AGE = 7 * 24 * 3600


class CacheManager:
    def __init__(self):
        CACHE_DIR.mkdir(parents=True, exist_ok=True)

    def _is_fresh(self, cache_file: Path) -> bool:
        if not cache_file.exists():
            return False
        meta = self._load_meta()
        ts = meta.get(str(cache_file), 0)
        return (time.time() - ts) < CACHE_MAX_AGE

    def _load_meta(self) -> dict:
        if META_CACHE.exists():
            with open(META_CACHE) as f:
                return json.load(f)
        return {}

    def _save_meta(self, key: str):
        meta = self._load_meta()
        meta[key] = time.time()
        with open(META_CACHE, "w") as f:
            json.dump(meta, f)

    def load_cards(self) -> list[Card]:
        if self._is_fresh(CARDS_CACHE):
            return self._load_cards_from_file()
        # Try API download
        try:
            return self._download_and_cache_cards()
        except Exception as e:
            print(f"  Could not download cards: {e}")
            # Try stale cache
            if CARDS_CACHE.exists():
                print("  Using stale cached data.")
                return self._load_cards_from_file()
            # Fall back to bundled data
            print("  Using bundled card database (200+ popular cards).")
            return self._load_bundled()

    def _load_cards_from_file(self) -> list[Card]:
        print("  Loading cards from cache...")
        with open(CARDS_CACHE) as f:
            raw = json.load(f)
        cards = self._parse_card_list(raw)
        print(f"  Loaded {len(cards)} cards from cache.")
        return cards

    def _parse_card_list(self, raw: list[dict]) -> list[Card]:
        ban_map = {
            "Banned": BanStatus.BANNED, "Limited": BanStatus.LIMITED,
            "Semi-Limited": BanStatus.SEMI_LIMITED, "Unlimited": BanStatus.UNLIMITED,
        }
        cards = []
        for d in raw:
            try:
                ban_info = d.get("banlist_info", {})
                ban_tcg_str = ban_info.get("ban_tcg", d.get("ban_tcg", "Unlimited"))
                ban_ocg_str = ban_info.get("ban_ocg", d.get("ban_ocg", "Unlimited"))
                card = Card(
                    id=d["id"], name=d["name"], type=d["type"],
                    desc=d.get("desc", ""), race=d.get("race", ""),
                    archetype=d.get("archetype"),
                    atk=d.get("atk"), defense=d.get("def"),
                    level=d.get("level"), rank=d.get("rank"),
                    link_val=d.get("linkval"), scale=d.get("scale"),
                    attribute=d.get("attribute"),
                    ban_tcg=ban_map.get(ban_tcg_str, BanStatus.UNLIMITED),
                    ban_ocg=ban_map.get(ban_ocg_str, BanStatus.UNLIMITED),
                )
                cards.append(card)
            except (KeyError, TypeError):
                continue
        return cards

    def _download_and_cache_cards(self) -> list[Card]:
        from .api import fetch_all_cards
        raw_cards = fetch_all_cards()
        cards = []
        cache_data = []
        for d in raw_cards:
            try:
                card = Card.from_api(d)
                cards.append(card)
                cache_data.append(card.to_dict())
            except (KeyError, TypeError):
                continue
        with open(CARDS_CACHE, "w") as f:
            json.dump(cache_data, f)
        self._save_meta(str(CARDS_CACHE))
        print(f"  Cached {len(cards)} cards.")
        return cards

    def _load_bundled(self) -> list[Card]:
        from .bundled_cards import BUNDLED_CARDS
        return self._parse_card_list(BUNDLED_CARDS)

    def load_archetypes(self) -> list[str]:
        if self._is_fresh(ARCHETYPES_CACHE):
            with open(ARCHETYPES_CACHE) as f:
                archetypes = json.load(f)
            return archetypes
        try:
            from .api import fetch_archetypes
            archetypes = fetch_archetypes()
            with open(ARCHETYPES_CACHE, "w") as f:
                json.dump(archetypes, f)
            self._save_meta(str(ARCHETYPES_CACHE))
            return archetypes
        except Exception:
            return []

    def refresh(self):
        print("  Refreshing card database...")
        self._download_and_cache_cards()
        self.load_archetypes()
        print("  Cache refreshed!")

    def cache_age_str(self) -> str:
        meta = self._load_meta()
        ts = meta.get(str(CARDS_CACHE), 0)
        if ts == 0:
            return "never"
        age = time.time() - ts
        if age < 3600:
            return f"{int(age/60)} minutes ago"
        elif age < 86400:
            return f"{int(age/3600)} hours ago"
        return f"{int(age/86400)} days ago"
