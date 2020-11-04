from flask import render_template, request, url_for, redirect, flash, session, jsonify
import random
import script_poker
from app import app

TAILLE_JEU = 5
def premier_tirage(deck):
    random.shuffle(deck)
    tirage=deck[0:5]
    deck=deck[5:]
    return tirage,deck


def shuffle_cards(deck,jeu=[]):
    _tirage,new_deck = script_poker.tirage(deck,jeu)
    return {"new_deck": new_deck, "cartes": _tirage}

def mapCardsToImg(cards: list):
    dico_card_map = []
    for card in cards:
        dico_card_map.append({ 'carte': card, 'img': url_for('static',filename=f"img/{card}.svg") })
    return dico_card_map

@app.route("/video-poker/start",methods=['POST'])  
def start_video_poker():
    initial_deck = ['2-h','3-h','4-h','5-h','6-h','7-h','8-h','9-h','10-h','J-h','Q-h','K-h','A-h','2-d','3-d','4-d','5-d','6-d','7-d','8-d','9-d','10-d','J-d','Q-d','K-d','A-d','2-c','3-c','4-c','5-c','6-c','7-c','8-c','9-c','10-c','J-c','Q-c','K-c','A-c','2-s','3-s','4-s','5-s','6-s','7-s','8-s','9-s','10-s','J-s','Q-s','K-s','A-s']
  
    bank,mise = (request.form["bank"] if ("bankroll" not in session or session["bankroll"] == 0) else session["bankroll"]), request.form["mise"]
    if (int(bank) - int(mise) < 0):
        flash('Mise trop élevée : veuillez réessayer', 'error')
        return redirect('/')
    else:
        shuffle_result = shuffle_cards(initial_deck)
        session["bankroll"] = int(bank) - int(mise)
        session["mise"] = int(mise)
        session["deck"] = shuffle_result["new_deck"]
        return render_template('board.html',deck=session["deck"],cartes=mapCardsToImg(shuffle_result["cartes"])), 201

@app.route("/video-poker/second",methods=['POST'])
def second_shuffle():
    choix_joueur: list = request.form.getlist("carte[]")
    #pour récupérer le deck précédemment modifié
    shuffle_result = shuffle_cards(session["deck"],choix_joueur)
    deck: list = shuffle_result["new_deck"]
    decomposition_cartes = [ dict({ "couleur": ensemble[1], "valeur": ensemble[0] }) for ensemble in [carte.split("-") for carte in shuffle_result["cartes"] ]]
    session["bankroll"],resultat = script_poker.partie(session["mise"],session["bankroll"],decomposition_cartes)
    
    return render_template('board.html',deck=session["deck"],cartes=mapCardsToImg(shuffle_result["cartes"]),resultat=resultat),201