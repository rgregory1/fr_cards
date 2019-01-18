from flask import Flask, session, render_template, url_for, redirect, request
import random
from flask_debugtoolbar import DebugToolbarExtension
from pprint import pprint

app = Flask(__name__)

# the toolbar is only enabled in debug mode:
app.debug = True

# set a 'SECRET_KEY' to enable the Flask session cookies
app.config["SECRET_KEY"] = "<replace with a secret key>"

toolbar = DebugToolbarExtension(app)
# DEBUG_TB_INTERCEPT_REDIRECTS = False
app.config["DEBUG_TB_INTERCEPT_REDIRECTS"] = False


# Set the secret key to some random bytes. Keep this really secret!
app.secret_key = "my_secret"

sprinter_cards_begin = [
    [2, "S", ""],
    [2, "S", ""],
    [2, "S", ""],
    [3, "S", ""],
    [3, "S", ""],
    [3, "S", ""],
    [4, "S", ""],
    [4, "S", ""],
    [4, "S", ""],
    [5, "S", ""],
    [5, "S", ""],
    [5, "S", ""],
    [9, "S", ""],
    [9, "S", ""],
    [9, "S", ""],
]
# sprinter_cards_begin = [2, 2, 2, 3, 3, 3, 4, 4, 4, 5, 5, 5, 9, 9, 9]


@app.route("/")
def home():
    # clear all cookies to setup new player
    session.clear()
    return render_template("home.html")


@app.route("/setup", methods=["POST", "GET"])
def setup():
    # collect form info
    session["player_name"] = request.form["player_name"]
    session["team_color"] = request.form["team_color"]
    session["round"] = 1
    session["choosen_cards"] = []
    session["current_hand"] = []
    for card in sprinter_cards_begin:
        card[2] = session["team_color"]
    session["sprint_deck"] = sprinter_cards_begin
    session["sprinter_discards"] = []
    session["sprinter_recycle"] = []
    return redirect(url_for("view_hand"))


@app.route("/view_hand", methods=["POST", "GET"])
def view_hand():
    random.shuffle(session["sprint_deck"])
    for x in range(3):
        current_card = session["sprint_deck"].pop()
        print(current_card)
        session["current_hand"].append(current_card)
    print("line72")
    print(session["current_hand"])
    return render_template("card_picker.html")


@app.route("/first_choice", methods=["POST", "GET"])
def first_choice():
    # pull card choice from form and turn it into an integer
    result_number = request.form["card_choice"]
    result_number = int(result_number)
    print(result_number)
    print(session["current_hand"])
    # get the chosen card from the hand
    result = session["current_hand"].pop(result_number)
    session["choosen_cards"].append(result)
    # add the 'unchosen' cards to the recyle pile
    session["sprinter_recycle"].extend(session["current_hand"])
    # add chosen card to the discard pile
    choosen_cards = session["choosen_cards"]
    session["sprinter_discards"].extend(result)
    # session["current_hand"] = []
    return render_template("first_choice.html", choosen_cards=choosen_cards)


@app.route("/delete-value/")
def delete_visits():
    session.pop("trial1", None)  # delete visits
    result = "deleted trial value"
    return render_template("blank.html", result=result)


if __name__ == "__main__":
    app.run(debug=True)
    # app.run(host="0.0.0.0")
