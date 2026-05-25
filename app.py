#!/usr/bin/env python3
"""Yu-Gi-Oh! AI Deck Builder - Web Application.

Mobile-friendly web interface for the deck builder.

Usage:
    python3 app.py

Then open http://localhost:5000 on your phone or computer.
For phone access on the same WiFi, use http://<your-ip>:5000
"""

import json
import io
from flask import Flask, render_template, request, jsonify, send_file

from ygodeck.cache import CacheManager
from ygodeck.carddb import CardDatabase
from ygodeck.builder import DeckBuilder
from ygodeck.models import BanStatus

app = Flask(__name__)

# Global state - initialized on startup
db = None
builder = None


def init_db():
    global db, builder
    print("Initializing card database...")
    cache = CacheManager()
    try:
        cards = cache.load_cards()
        archetypes = cache.load_archetypes()
    except Exception:
        print("Using bundled card database.")
        cards = cache._load_bundled()
        archetypes = []
    db = CardDatabase(cards, archetypes)
    builder = DeckBuilder(db)
    print(f"Ready! {len(cards)} cards, {len(db._by_archetype)} archetypes loaded.")


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/api/build", methods=["POST"])
def api_build():
    data = request.json or {}
    description = data.get("description", "")
    archetype_input = data.get("archetype", "")
    style = data.get("style", "")
    include_raw = data.get("include_cards", "")
    exclude_raw = data.get("exclude_cards", "")
    allow_forbidden = data.get("allow_forbidden", False)
    deck_size = data.get("deck_size", 40)

    try:
        deck_size = max(40, min(60, int(deck_size)))
    except (ValueError, TypeError):
        deck_size = 40

    include_cards = [c.strip() for c in include_raw.split(",") if c.strip()] if include_raw else []
    exclude_cards = [c.strip() for c in exclude_raw.split(",") if c.strip()] if exclude_raw else []

    archetype = None
    query = archetype_input or description
    if query:
        for word in query.replace(",", " ").split():
            resolved = db.resolve_archetype(word)
            if resolved:
                archetype = resolved
                break
        if not archetype:
            resolved = db.resolve_archetype(query)
            if resolved:
                archetype = resolved

    deck_style = style.upper() if style else None
    if deck_style and deck_style not in ("COMBO", "CONTROL", "MIDRANGE", "AGGRO", "STUN"):
        deck_style = None

    # Resolve include/exclude for preview
    resolved_includes = []
    for name in include_cards:
        card = db.resolve_card_name(name)
        resolved_includes.append({"input": name, "resolved": card.name if card else None})

    resolved_excludes = []
    for name in exclude_cards:
        card = db.resolve_card_name(name)
        resolved_excludes.append({"input": name, "resolved": card.name if card else None})

    try:
        deck = builder.build_deck(
            description=description, archetype=archetype,
            include_cards=include_cards, exclude_cards=exclude_cards,
            allow_forbidden=allow_forbidden, deck_style=deck_style,
            main_deck_size=deck_size,
        )
    except Exception as e:
        return jsonify({"error": str(e)}), 400

    valid, errors = deck.is_valid(allow_forbidden=allow_forbidden)

    def card_to_dict(card, count):
        roles = db.get_card_roles(card)
        return {
            "id": card.id, "name": card.name, "type": card.type,
            "race": card.race, "attribute": card.attribute or "",
            "atk": card.atk, "def": card.defense,
            "level": card.level, "rank": card.rank, "link": card.link_val,
            "archetype": card.archetype or "",
            "ban": card.ban_tcg.value,
            "roles": [r.value for r in roles],
            "count": count,
            "is_monster": card.is_monster, "is_spell": card.is_spell,
            "is_trap": card.is_trap, "is_extra": card.is_extra_deck,
            "desc": card.desc,
        }

    return jsonify({
        "name": deck.name,
        "archetype": archetype or "",
        "style": deck_style or "AUTO",
        "main_deck": [card_to_dict(c, n) for c, n in deck.main_deck],
        "extra_deck": [card_to_dict(c, n) for c, n in deck.extra_deck],
        "main_count": deck.main_count,
        "extra_count": deck.extra_count,
        "valid": valid,
        "errors": errors,
        "resolved_includes": resolved_includes,
        "resolved_excludes": resolved_excludes,
    })


@app.route("/api/export", methods=["POST"])
def api_export():
    data = request.json or {}
    # Rebuild the deck from the same params
    # Actually we'll construct YDK from the card IDs sent
    main_ids = data.get("main_ids", [])
    extra_ids = data.get("extra_ids", [])

    lines = ["#created by YuGiOh AI Deck Builder", "#main"]
    lines.extend(str(cid) for cid in main_ids)
    lines.append("#extra")
    lines.extend(str(cid) for cid in extra_ids)
    lines.append("!side")

    ydk_content = "\n".join(lines)
    buf = io.BytesIO(ydk_content.encode("utf-8"))
    buf.seek(0)
    return send_file(buf, mimetype="text/plain", as_attachment=True,
                     download_name="deck.ydk")


@app.route("/api/search", methods=["GET"])
def api_search():
    query = request.args.get("q", "")
    if not query or len(query) < 2:
        return jsonify({"results": []})

    card = db.resolve_card_name(query)
    results = db.search_cards(query, limit=20)

    def card_brief(c):
        return {
            "name": c.name, "type": c.type, "archetype": c.archetype or "",
            "ban": c.ban_tcg.value, "attribute": c.attribute or "",
            "race": c.race, "atk": c.atk, "def": c.defense,
            "level": c.level, "rank": c.rank, "link": c.link_val,
            "desc": c.desc, "roles": [r.value for r in db.get_card_roles(c)],
        }

    best = card_brief(card) if card else None
    return jsonify({
        "best_match": best,
        "results": [card_brief(c) for c in results],
    })


@app.route("/api/archetypes", methods=["GET"])
def api_archetypes():
    query = request.args.get("q", "").lower()
    archetypes = sorted(db._by_archetype.keys())
    if query:
        archetypes = [a for a in archetypes if query in a.lower()]
    return jsonify({
        "archetypes": [{"name": a, "count": len(db._by_archetype[a])} for a in archetypes]
    })


@app.route("/api/banlist", methods=["GET"])
def api_banlist():
    category = request.args.get("category", "all")
    result = {}
    if category in ("banned", "all"):
        result["banned"] = [{"name": c.name, "type": c.type} for c in sorted(db.get_banned_cards(), key=lambda x: x.name)]
    if category in ("limited", "all"):
        result["limited"] = [{"name": c.name, "type": c.type} for c in sorted(db.get_limited_cards(), key=lambda x: x.name)]
    if category in ("semi", "all"):
        result["semi_limited"] = [{"name": c.name, "type": c.type} for c in sorted(db.get_semi_limited_cards(), key=lambda x: x.name)]
    return jsonify(result)


@app.route("/api/stats", methods=["GET"])
def api_stats():
    return jsonify({
        "total_cards": len(db.cards),
        "archetypes": len(db._by_archetype),
        "banned": len(db.get_banned_cards()),
        "limited": len(db.get_limited_cards()),
    })


if __name__ == "__main__":
    init_db()
    import socket
    hostname = socket.gethostname()
    try:
        local_ip = socket.gethostbyname(hostname)
    except Exception:
        local_ip = "localhost"
    print(f"\n  Open in browser:")
    print(f"    Local:  http://localhost:5000")
    print(f"    Phone:  http://{local_ip}:5000")
    print(f"  (phone must be on the same WiFi network)\n")
    app.run(host="0.0.0.0", port=5000, debug=False)
