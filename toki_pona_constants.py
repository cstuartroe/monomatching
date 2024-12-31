import json

TOKI_PONA_DECK_DIR = "decks/toki_pona"
TOKI_PONA_DECK_JSON = "deck.json"
TOKI_PONA_ROW_SIZE = 600
TOKI_PONA_TITLE_ROW_SIZE = 900
TOKI_PONA_MARGIN_SIZE = 200
TOKI_PONA_CARD_SIZE = (TOKI_PONA_ROW_SIZE*3 + TOKI_PONA_MARGIN_SIZE*2, TOKI_PONA_ROW_SIZE*4 + TOKI_PONA_MARGIN_SIZE*2)
TOKI_PONA_FONT_LOCATION = "flaskr/static/sitelenselikiwenasuki.ttf"

# based on one small corpus, not really authoritative but doesn't need to be
TOKI_PONA_FREQUENCY_ORDER = [
    "li",
    "e",
    "jan",
    "tawa",
    "pi",
    "ona",
    "ni",
    "mi",
    "la",
    "lawa",
    "ma",
    "sina",
    "lon",
    "kama",
    "toki",
    "ala",
    "tan",
    "tenpo",
    "sewi",
    "ike",
    "o",
    "ale",
    "tomo",
    "mute",
    "pana",
    "pona",
    "pali",
    "pilin",
    "kulupu",
    "meli",
    "telo",
    "wile",
    "suli",
    "sama",
    "lili",
    "lukin",
    "awen",
    "wawa",
    "anpa",
    "en",
    "wan",
    "nasin",
    "pakala",
    "weka",
    "moli",
    "sona",
    "pini",
    "ante",
    "utala",
    "sinpin",
    "jo",
    "suno",
    "ken",
    "insa",
    "poka",
    "tu",
    "mama",
    "moku",
    "kute",
    "kepeken",
    "taso",
    "ijo",
    "kalama",
    "alasa",
    "musi",
    "nanpa",
    "sitelen",
    "kiwen",
    "lupa",
    "mije",
    "sike",
    "poki",
    "unpa",
    "len",
    "palisa",
    "noka",
    "kon",
    "mun",
    "anu",
    "uta",
    "seme",
    "olin",
    "seli",
    "linja",
    "pimeja",
    "nimi",
    "sin",
    "jaki",
    "mani",
    "sijelo",
    "soweli",
    "ilo",
    "luka",
    "ko",
    "nena",
    "open",
    "kasi",
    "nasa",
    "a",
    "mu",
    "kili",
    "supa",
    "lipu",
    "lape",
    "monsi",
    "pan",
    "jelo",
    "esun",
    "loje",
    "selo",
    "waso",
    "pipi",
    "laso",
    "pu",
    "kule",
    "lete",
    "akesi",
    "suwi",
    "kala",
    "walo",

    # Here and below is ku
    "oko",
    "lanpan",
    "kin",
    "kipisi",
    "monsuta",
    "namako",
    "leko",
    "tonsi",
    "misikeke",
    "ku",
    "kokosila",
    "kijetesantakalu",
    "jasima",
    "meso",
    "epiku",
    "soko",
    "n",
]

TOKI_PONA_SKIP = ["epiku", "oko", "n", "kokosila"]

WORDS_IN_DECK = [word for word in TOKI_PONA_FREQUENCY_ORDER if word not in TOKI_PONA_SKIP]

SITELEN_VARIANTS = {
    "soko": "soko2",
    "namako": "namako2",
}

Deck = list[set[int]]
OrderedDeck = list[list[int]]


def save_ordered_deck(deck: OrderedDeck, filename: str):
    with open(filename, "w") as fh:
        json.dump(deck, fh, indent=2)


def load_ordered_deck(filename: str) -> OrderedDeck:
    with open(filename, "r") as fh:
        return json.load(fh)
