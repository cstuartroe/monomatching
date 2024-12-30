import json
import os
import random

from matplotlib import pyplot as plt
from PIL import Image, ImageFont, ImageDraw
from tqdm import tqdm

from toki_pona_constants import *


Deck = list[set[int]]
OrderedDeck = list[list[int]]


def save_ordered_deck(deck: OrderedDeck, filename: str):
    with open(filename, "w") as fh:
        json.dump(deck, fh, indent=2)


def load_ordered_deck(filename: str) -> OrderedDeck:
    with open("filename", "r") as fh:
        return json.load(fh)


def construct_deck(symbols_per_card: int) -> Deck:
    """This method only generates valid decks when symbols_per_card is p + 1
       for some prime p, that is, it can generate decks based on finite projective planes
       of prime order p. Prime powers are proven to also be valid orders for finite
       projective planes, though I don't know whether any algorithm exists for finding them
       in the general case. Whether other composite numbers can be the order of a
       finite projective plane is an open question in mathematics.

       To summarize, here are the deck sizes which this function can generate:

       p   symbols_per_card (p + 1)  deck size p*(p + 1) + 1
        1               2                    3
        2               3                    7
        3               4                   13
        5               6                   31
        7               8                   57
       11              12                  133
       13              14                  183
       17              18                  307
       19              20                  381
       etc.
    """
    grid_cards: list[list[set[int]]] = []
    projective_cards: list[set[int]] = []
    symbol_index = 0

    for _ in range(symbols_per_card - 1):
        grid_cards.append([])
        for _ in range(symbols_per_card - 1):
            grid_cards[-1].append(set())

    for over in range(len(grid_cards)):
        projective_card = set()
        for col in range(len(grid_cards)):
            for row in range(len(grid_cards)):
                card = grid_cards[row][(col + (row * over)) % (symbols_per_card - 1)]
                card.add(symbol_index)
            projective_card.add(symbol_index)
            symbol_index += 1

            # for row in grid_cards:
            #     print(row)
            # print()
        projective_cards.append(projective_card)
        # print(projective_cards)
        # print()

    projective_card = set()
    for row in range(len(grid_cards)):
        for col in range(len(grid_cards)):
            card = grid_cards[row][col]
            card.add(symbol_index)
        projective_card.add(symbol_index)
        symbol_index += 1

        # for row in grid_cards:
        #     print(row)
        # print()
    projective_cards.append(projective_card)
    # print(projective_cards)
    # print()

    for card in projective_cards:
        card.add(symbol_index)

    deck = []
    for row in grid_cards:
        deck += row
    deck += projective_cards

    return deck


def verify_monomatching(deck: Deck):
    for i, c1 in enumerate(deck):
        for c2 in deck[i + 1:]:
            if len(c1 & c2) != 1:
                raise ValueError(f"Non-monomatching cards: {c1} {c2}")


def symbol_counts(deck: Deck):
    occurrences: dict[int, int] = {}
    for card in deck:
        for symbol in card:
            occurrences[symbol] = occurrences.get(symbol, 0) + 1
    return occurrences


def remove_rarest_symbol(deck: Deck):
    occurrences = symbol_counts(deck)

    rarest_symbol = sorted(list(occurrences.items()), key=lambda x: x[1])[0][0]
    # print(f"Removing {rarest_symbol} (occurs {occurrences[rarest_symbol]} times)")

    return [card for card in deck if rarest_symbol not in card]


def get_gap(deck: Deck, symbols: list[int]):
    occurrences = symbol_counts(deck)
    new_counts = [occurrences.get(symbol, 0) for symbol in symbols]
    return max(new_counts) - min(new_counts)


def remove_least_gapping_symbol(deck: Deck):
    all_symbols: list[int] = list(symbol_counts(deck).keys())

    lowest_gap = 100000000
    best_new_deck = None
    for symbol in all_symbols:
        new_deck = [c for c in deck if symbol not in c]
        gap = get_gap(new_deck, all_symbols)
        if gap < lowest_gap:
            lowest_gap = gap
            best_new_deck = new_deck

    return best_new_deck


def remove_most_common_card(deck: Deck):
    occurrences = symbol_counts(deck)
    most_common_card = sorted(deck, key=lambda c: sum(occurrences[symbol] for symbol in c))[-1]

    return [card for card in deck if card != most_common_card]


def remove_least_gapping_card(deck: Deck):
    all_symbols: list[int] = list(symbol_counts(deck).keys())

    lowest_gap = 100000000
    best_new_deck = None
    for card in deck:
        new_deck = [c for c in deck if c != card]
        gap = get_gap(new_deck, all_symbols)
        if gap < lowest_gap:
            lowest_gap = gap
            best_new_deck = new_deck

    return best_new_deck


def num_symbols(deck: Deck):
    symbols = set()
    for card in deck:
        symbols |= card
    return len(symbols)


def remap_symbols(deck: Deck):
    occurrences = symbol_counts(deck)

    sorted_symbols = sorted(list(occurrences.keys()), key=lambda k: -occurrences[k])
    symbol_map = {
        k: v
        for k, v in zip(sorted_symbols, range(len(sorted_symbols)))
    }

    return [
        {
            symbol_map[symbol]
            for symbol in card
        }
        for card in deck
    ]


def construct_reduced_deck(symbols: int) -> Deck:
    symbols_per_card = 1

    while True:
        deck = construct_deck(symbols_per_card)
        try:
            verify_monomatching(deck)
        except ValueError:
            symbols_per_card += 1
            continue

        if num_symbols(deck) < symbols:
            symbols_per_card += 1
            continue

        # print(f"Starting with {num_symbols(deck)} symbols")
        while num_symbols(deck) > symbols:
            deck = remove_rarest_symbol(deck)

        return remap_symbols(deck)


def print_occurrences(deck: Deck, names = None):
    occurrences: dict[int, int] = {}
    for card in deck:
        for symbol in card:
            occurrences[symbol] = occurrences.get(symbol, 0) + 1

    for symbol, count in sorted(list(occurrences.items()), key=lambda x: x[1]):
        if names:
            print(names[symbol], count)
        else:
            print(symbol, count)


def print_matches(deck: Deck):
    matches: dict[int, int] = {}
    for i, c1 in enumerate(deck):
        for c2 in deck[i + 1:]:
            assert len(c1 & c2) == 1
            match = list(c1 & c2)[0]
            matches[match] = matches.get(match, 0) + 1

    for k, v in sorted(list(matches.items()), key=lambda x: x[1]):
        print(k, v)


def plot_reduced_deck_sizes():
    data = []
    for symbols in range(1, 500):
        # print(symbols)
        deck = construct_reduced_deck(symbols)
        # print(f"{len(deck)} cards, {num_symbols(deck)} symbols")
        if num_symbols(deck) == symbols:
            data.append((symbols, len(deck)))
        else:
            data.append((symbols, 0))

    plt.plot(*zip(*data))
    plt.show()


def shuffle_deck(deck: Deck) -> OrderedDeck:
    deck = [
        list(card)
        for card in deck
    ]
    for card in deck:
        random.shuffle(card)
    random.shuffle(deck)

    total_matches = 0
    same_position_matches = 0
    for i, c1 in enumerate(deck):
        for c2 in deck[i+1:]:
            total_matches += 1
            shared_symbol = list(set(c1) & set(c2))[0]
            if c1.index(shared_symbol) == c2.index(shared_symbol):
                same_position_matches += 1
    print(f"{same_position_matches}/{total_matches} have match in the same position")

    return deck


def paste_img_center(background: Image.Image, sprite: Image.Image, x, y):
    background.paste(
        sprite,
        (x - sprite.width // 2, y - sprite.height // 2),
        sprite,
    )

TOKI_PONA_FONT = ImageFont.truetype(TOKI_PONA_FONT_LOCATION, 400)
TOKI_PONA_FONT_LARGE = ImageFont.truetype(TOKI_PONA_FONT_LOCATION, 800)


def toki_pona_rescale(img: Image.Image):
    new_width = round(TOKI_PONA_ROW_SIZE*.75)
    new_height = round(new_width*img.height/img.width)
    return img.resize((new_width, new_height))


def make_toki_pona_cards():
    random.seed(50)

    deck = construct_reduced_deck(133)
    verify_monomatching(deck)
    while len(deck) > 90:
        deck = remove_least_gapping_card(deck)
    deck = remap_symbols(deck)

    shuffled_deck = shuffle_deck(deck)
    save_ordered_deck(shuffled_deck, TOKI_PONA_DECK_JSON)

    print_occurrences(deck, WORDS_IN_DECK)
    # print()
    # print(num_symbols(deck))
    # print(len(deck))

    os.makedirs(TOKI_PONA_DECK_DIR, exist_ok=True)
    for filename in os.listdir(TOKI_PONA_DECK_DIR):
        os.unlink(f"{TOKI_PONA_DECK_DIR}/{filename}")

    for i, card in enumerate(tqdm(shuffled_deck)):
        card_image = Image.new("RGBA", TOKI_PONA_CARD_SIZE, (255, 255, 255))
        draw = ImageDraw.Draw(card_image)
        for row in range(4):
            for col in range(3):
                x = round(TOKI_PONA_ROW_SIZE*(col + .5)) + TOKI_PONA_MARGIN_SIZE
                y = round(TOKI_PONA_ROW_SIZE*(row + .5)) + TOKI_PONA_MARGIN_SIZE
                word = WORDS_IN_DECK[card[row*3 + col]]
                draw.text(
                    (x, y),
                    SITELEN_VARIANTS.get(word, word),
                    (0, 0, 0),
                    font=TOKI_PONA_FONT,
                    anchor="mm",
                    features=["liga"],
                ),
        card_image.save(f"{TOKI_PONA_DECK_DIR}/{i}.png")

    card_back = Image.new("RGBA", TOKI_PONA_CARD_SIZE, (255, 255, 255))
    draw = ImageDraw.Draw(card_back)
    title = ["o", "alasa", "e", "sama"]
    for row in range(2):
        for col in range(2):
            x = TOKI_PONA_CARD_SIZE[0]//2 + round(TOKI_PONA_TITLE_ROW_SIZE*(-.5 + col))
            y = TOKI_PONA_CARD_SIZE[1]//2 + round(TOKI_PONA_TITLE_ROW_SIZE*(-.5 + row))
            draw.text(
                (x, y),
                title[row*2 + col],
                (0, 0, 0),
                font=TOKI_PONA_FONT_LARGE,
                anchor="mm",
                features=["liga"],
            ),
    card_back.save(f"{TOKI_PONA_DECK_DIR}/back.png")


def make_favicon():
    img = Image.new("RGBA", (800, 800), (255, 255, 255))
    draw = ImageDraw.Draw(img)
    draw.text(
        (400, 400),
        "alasa",
        (0, 0, 0),
        font=TOKI_PONA_FONT_LARGE,
        anchor="mm",
        features=["liga"],
    )
    img.save("static/favicon.ico")


if __name__ == "__main__":
    make_toki_pona_cards()
    make_favicon()
