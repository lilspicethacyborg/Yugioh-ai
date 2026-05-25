"""Card role classification via text analysis."""

import re
from .models import Card, CardRole

ROLE_PATTERNS: list[tuple[CardRole, list[re.Pattern]]] = [
    (CardRole.SEARCHER, [
        re.compile(r"add \d* ?\w* cards? from (?:your |the )?(?:Deck|GY|Graveyard) to (?:your |the )?hand", re.I),
        re.compile(r"add (?:it|them|that card|1 card|1 monster|1 Spell|1 Trap) .* from (?:your |the )?Deck to (?:your |the )?hand", re.I),
        re.compile(r"search (?:your |the )?Deck", re.I),
    ]),
    (CardRole.STARTER, [
        re.compile(r"if (?:this card is |you )(?:Normal |Special )?Summon", re.I),
        re.compile(r"when (?:this card is )?(?:Normal |Special )?Summoned", re.I),
    ]),
    (CardRole.EXTENDER, [
        re.compile(r"Special Summon (?:this card|itself) from (?:your |the )?hand", re.I),
        re.compile(r"you can Special Summon this card", re.I),
        re.compile(r"Special Summon \d+ .* from (?:your |the )?(?:hand|Deck|GY)", re.I),
    ]),
    (CardRole.HANDTRAP, [
        re.compile(r"(?:When|If) your opponent.+you can (?:discard|send|reveal) this card", re.I),
        re.compile(r"(?:discard|send) this card.+(?:negate|destroy|banish)", re.I),
        re.compile(r"\(Quick Effect\).+(?:from your hand|discard this card)", re.I),
    ]),
    (CardRole.BOARD_BREAKER, [
        re.compile(r"destroy all (?:Spell|Trap|monsters?|cards?).+(?:your opponent|on the field)", re.I),
        re.compile(r"return all .* to the hand", re.I),
        re.compile(r"banish all", re.I),
    ]),
    (CardRole.NEGATE, [
        re.compile(r"negate (?:the activation|that effect|its effects?|the effect)", re.I),
        re.compile(r"negate (?:the Summon|a Summon|the Special Summon)", re.I),
        re.compile(r"your opponent cannot activate", re.I),
    ]),
    (CardRole.REMOVAL, [
        re.compile(r"destroy (?:1|that|the targeted) .* (?:card|monster|Spell|Trap)", re.I),
        re.compile(r"banish (?:1|that) .* (?:card|monster)", re.I),
        re.compile(r"target 1 .* (?:card|monster).+destroy (?:it|that)", re.I),
    ]),
    (CardRole.DRAW, [
        re.compile(r"draw \d+ cards?", re.I),
        re.compile(r"draw cards? equal", re.I),
        re.compile(r"excavate the top", re.I),
    ]),
    (CardRole.FLOODGATE, [
        re.compile(r"(?:your opponent |neither player )cannot (?:Special Summon|activate|Normal Summon)", re.I),
        re.compile(r"each player can only", re.I),
        re.compile(r"neither player can", re.I),
        re.compile(r"negate (?:all|the effects of all)", re.I),
    ]),
    (CardRole.PROTECTION, [
        re.compile(r"cannot be (?:destroyed|targeted|banished)", re.I),
        re.compile(r"unaffected by (?:other|your opponent|activated effects)", re.I),
    ]),
    (CardRole.RECOVERY, [
        re.compile(r"Special Summon .* from (?:your |the )?(?:GY|Graveyard)", re.I),
        re.compile(r"add .* from (?:your |the )?GY to (?:your |the )?hand", re.I),
    ]),
    (CardRole.BOSS, [
        re.compile(r"unaffected by (?:other )?card effects", re.I),
        re.compile(r"(?:Quick Effect).+negate .+ destroy", re.I),
    ]),
]

KNOWN_HANDTRAPS = {
    "Ash Blossom & Joyous Spring", "Ghost Ogre & Snow Rabbit",
    "Ghost Belle & Haunted Mansion", "Ghost Mourner & Moonlit Chill",
    "Effect Veiler", "Maxx \"C\"", "Nibiru, the Primal Being",
    "D.D. Crow", "Droll & Lock Bird", "Artifact Lancea",
    "PSY-Framegear Gamma", "Dimension Shifter", "Skull Meister",
    "Token Collector", "Contact \"C\"", "Fantastical Dragon Phantazmay",
    "Mulcharmy Fuwalos", "Mulcharmy Purulia", "Mulcharmy Nyalus",
}

KNOWN_FLOODGATES = {
    "Skill Drain", "Imperial Order", "Rivalry of Warlords",
    "Gozen Match", "There Can Be Only One", "Anti-Spell Fragrance",
    "Vanity's Emptiness", "Macro Cosmos", "Dimensional Fissure",
    "Summon Limit", "Necrovalley", "Secret Village of the Spellcasters",
    "Inspector Boarder", "Amano-Iwato", "Denko Sekka",
    "Majesty's Fiend", "Vanity's Fiend",
}


def classify_card(card: Card) -> list[CardRole]:
    roles = []
    if card.name in KNOWN_HANDTRAPS:
        roles.append(CardRole.HANDTRAP)
    if card.name in KNOWN_FLOODGATES:
        roles.append(CardRole.FLOODGATE)

    desc = card.desc
    for role, patterns in ROLE_PATTERNS:
        if role in roles:
            continue
        for pattern in patterns:
            if pattern.search(desc):
                roles.append(role)
                break

    if card.is_extra_deck and card.monster_level and card.monster_level >= 7:
        if CardRole.NEGATE in roles and CardRole.BOSS not in roles:
            roles.append(CardRole.BOSS)

    if not roles:
        roles.append(CardRole.ARCHETYPE_CORE if card.archetype else CardRole.GENERIC_SUPPORT)

    return roles


def role_priority_score(card: Card, roles: list[CardRole]) -> float:
    role_scores = {
        CardRole.SEARCHER: 10.0, CardRole.STARTER: 9.0,
        CardRole.BOSS: 8.5, CardRole.NEGATE: 8.0,
        CardRole.EXTENDER: 7.5, CardRole.HANDTRAP: 7.0,
        CardRole.DRAW: 6.5, CardRole.BOARD_BREAKER: 6.0,
        CardRole.FLOODGATE: 5.5, CardRole.REMOVAL: 5.0,
        CardRole.RECOVERY: 4.5, CardRole.PROTECTION: 4.0,
        CardRole.ARCHETYPE_CORE: 3.0, CardRole.TECH: 2.0,
        CardRole.GENERIC_SUPPORT: 1.0,
    }
    score = sum(role_scores.get(r, 1.0) for r in roles)
    if len(roles) > 1:
        score += len(roles) * 1.5
    return score
