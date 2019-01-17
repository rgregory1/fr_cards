from flask import Flask, session, render_template, url_for, redirect, request
import random
from flask_debugtoolbar import DebugToolbarExtension

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

sprinter_cards_begin = [2, 2, 2, 3, 3, 3, 4, 4, 4, 5, 5, 5, 9, 9, 9]


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
    return redirect(url_for("view_hand"))


@app.route("/view_hand", methods=["POST", "GET"])
def view_hand():
    # session["team_color"] = "green-card"
    #     print(5 * "\n")
    #     print("checking for session cards in cookie")
    if session.get("sprint_deck"):
        #         print("\n")
        print("found sprint dec in cookies")
    #         print("sprint deck from cookies is: ")
    #         print(session["sprint_deck"])
    #         print(bool(session["sprint_deck"]))
    #         if session["sprint_deck"] == False:
    #             print("assigning session deck to variable")
    #             sprinter_cards = session["sprint_deck"]
    #             print(sprinter_cards)
    #         else:
    #             print("into the else statement meaning it is True")
    #             session["sprint_deck"] = sprinter_cards_begin
    #             session.modified = True
    #             print("just reset sprint_deck")
    #
    #             sprinter_cards = session["sprint_deck"]
    else:
        print("no sprint deck in cookies, setting it now")
        session["sprint_deck"] = sprinter_cards_begin
    #         print(session["sprint_deck"])
    #         sprinter_cards = session["sprint_deck"]
    #     print("out of loop now")
    #     session["trial"] = "it works"
    session["current_hand"] = []
    random.shuffle(session["sprint_deck"])

    #     print(sprinter_cards)
    for x in range(3):
        current_card = session["sprint_deck"].pop()
        print(current_card)
        session["current_hand"].append(current_card)
    current_hand = session["current_hand"]
    #     print(current_hand)
    #     print(sprinter_cards)
    card_type = "sprinter"
    team_color = session["team_color"]
    return render_template(
        "card_picker.html",
        current_hand=current_hand,
        card_type=card_type,
        team_color=team_color,
    )


@app.route("/new_hand")
def new_hand():
    sprinter_cards = [2, 2, 2, 3, 3, 3, 4, 4, 4, 5, 5, 5, 9, 9, 9]
    return redirect(url_for("view_hand"))


@app.route("/result", methods=["POST", "GET"])
def result():
    result = request.form["card_choice"]
    return "your result is: " + result


#
# @app.route("/")
# def session_test():
#     if session.get("trial1"):
#         result = "We have trial: and it is a list"
#         print("\n")
#         print(bool(session["trial1"]))
#         if len(session["trial1"]) > 1:
#             random.shuffle(session["trial1"])
#             session["current_card"] = session["trial1"].pop()
#             print("inside the greater than 1 loop")
#             trial1 = session["trial1"]
#         else:
#             session["current_card"] = session["trial1"].pop()
#             trial1 = session["trial1"]
#             session.pop("trial1", None)
#             result = "no more list"
#
#         return render_template("blank.html", result=result, trial1=trial1)
#
# else:
#     result = "There is no trial viriable"
#     session["trial1"] = [1, 2, 3]
#     result = "There is no trial viriable"
#     trial1 = session["trial1"]
#     return render_template("blank.html", result=result, trial1=trial1)


@app.route("/set_color/<color>")
def set_color(color):
    session["team_color"] = color
    return "team color is now {}".format(color)


@app.route("/delete-value/")
def delete_visits():
    session.pop("trial1", None)  # delete visits
    result = "deleted trial value"
    return render_template("blank.html", result=result)


if __name__ == "__main__":
    app.run(debug=True)
    # app.run(host="0.0.0.0")
