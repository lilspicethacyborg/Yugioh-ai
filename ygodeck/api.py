"""YGOPRODeck API client - free card database API."""

import requests
import time
from typing import Optional

BASE_URL = "https://db.ygoprodeck.com/api/v7"
_last_request_time = 0.0


def _rate_limit():
    global _last_request_time
    now = time.time()
    elapsed = now - _last_request_time
    if elapsed < 0.05:
        time.sleep(0.05 - elapsed)
    _last_request_time = time.time()


def _get(endpoint: str, params: Optional[dict] = None, retries: int = 3) -> dict:
    url = f"{BASE_URL}/{endpoint}"
    for attempt in range(retries):
        try:
            _rate_limit()
            resp = requests.get(url, params=params, timeout=60)
            resp.raise_for_status()
            return resp.json()
        except (requests.RequestException, ValueError) as e:
            if attempt < retries - 1:
                wait = 2 ** (attempt + 1)
                print(f"  API request failed ({e}), retrying in {wait}s...")
                time.sleep(wait)
            else:
                raise RuntimeError(f"Failed to fetch from API after {retries} attempts: {e}")


def fetch_all_cards() -> list[dict]:
    print("  Downloading card database from YGOPRODeck...")
    data = _get("cardinfo.php", params={"misc": "yes"})
    cards = data.get("data", [])
    print(f"  Downloaded {len(cards)} cards.")
    return cards


def fetch_archetypes() -> list[str]:
    print("  Downloading archetype list...")
    data = _get("archetypes.php")
    archetypes = [item["archetype_name"] for item in data]
    print(f"  Found {len(archetypes)} archetypes.")
    return archetypes
