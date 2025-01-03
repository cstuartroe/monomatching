import random

from flask import Flask, render_template, send_from_directory

from toki_pona_constants import WORDS_IN_DECK, SITELEN_VARIANTS, load_ordered_deck, TOKI_PONA_DECK_JSON

app = Flask(__name__)


@app.route("/")
def render_html():
    return render_template("display.html")


@app.route("/pair")
def get_pair():
    cards = load_ordered_deck(TOKI_PONA_DECK_JSON)

    left_index, right_index = random.sample(list(range(len(cards))), 2)
    answer = WORDS_IN_DECK[list(set(cards[left_index]) & set(cards[right_index]))[0]]
    answer_glyph = SITELEN_VARIANTS.get(answer, answer)

    return {
        "left": left_index,
        "right": right_index,
        "answer": answer,
        "answer_glyph": answer_glyph,
    }


@app.route('/static/img/<path:path>')
def image(path):
    # Using request args for path will expose you to directory traversal attacks
    return send_from_directory('decks/toki_pona', path)
