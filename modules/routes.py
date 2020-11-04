from flask import render_template, request, url_for, redirect, flash, session
import random
from script_poker import tirage
from modules.gain import partie
from modules.util import mapCardsToImg
from app import app

@app.route("/",methods=["GET"])
def homepage():
    """
        Fonction affichant la page d'accueil de l'interface Web

        Son état change selon le montant de la banque
    """
    if "bankroll" in session and session["bankroll"] == 0:
        flash('Banque épuisée : partie terminée !','error')
        del session["bankroll"]
    return render_template("homepage.html")


@app.route("/restart",methods=["GET"])
def restart():
    """
        Réinitialise le vidéo-poker : la banque sera donc supprimée
    """
    del session["bankroll"]
    return redirect('/')

@app.route("/video-poker/start",methods=['POST'])
def start_video_poker():
    """
        Fonction prenant en compte le montant de la banque,
        puis de la mise afin de tirer des cartes à l'utilisateur

    """
    initial_deck = ['2-h','3-h','4-h','5-h','6-h','7-h','8-h','9-h','10-h','J-h','Q-h','K-h','A-h','2-d','3-d','4-d','5-d','6-d','7-d','8-d','9-d','10-d','J-d','Q-d','K-d','A-d','2-c','3-c','4-c','5-c','6-c','7-c','8-c','9-c','10-c','J-c','Q-c','K-c','A-c','2-s','3-s','4-s','5-s','6-s','7-s','8-s','9-s','10-s','J-s','Q-s','K-s','A-s']
    
    #on récupère le montant de la banque et la mise depuis le formulaire
    #si le montant de la banque existe déjà en session, on le récupère
    bank,mise = (request.form["bank"] if ("bankroll" not in session) else session["bankroll"]), request.form["mise"]
    
    if bank == 0:
        return redirect('/')
    if int(bank) - int(mise) < 0:
        flash('Mise trop élevée : veuillez réessayer', 'error')
        return redirect('/')
    else:
        #on mélange les cartes
        cartes_tirees,new_deck = tirage(initial_deck)
        session["bankroll"] = int(bank) - int(mise)
        session["mise"] = int(mise)
        #on sauve le deck mélangé en session pour le prochain tirage
        session["deck"] = new_deck
        #on renvoie le template qui propose les cartes à garder (on associe chaque carte à son image correspondante pour l'affichage -> mapCardsToImg)
        return render_template('board.html',deck=session["deck"],cartes=mapCardsToImg(cartes_tirees)), 201


@app.route("/video-poker/second",methods=['POST'])
def second_shuffle():
    """
        Fonction permettant de faire un second tirage
        mais cette fois-ci pour tester les différentes combinaisons gagnates

        Le montant de la banque, capturée en session sera modifié ou non selon le résultat (oui si gagnant)
    """
    #récupération des cartes que le joueur souhaite garder
    choix_joueur: list = request.form.getlist("carte[]")
    #pour récupérer le deck précédemment modifié
    cartes_tirees,new_deck = tirage(session["deck"],choix_joueur)
    #on décompose chaque carte en un dictionnaire contenant la couleur et la valeur
    decomposition_cartes = [ dict({ "couleur": ensemble[1], "valeur": ensemble[0] }) for ensemble in [carte.split("-") for carte in cartes_tirees    ]]
    session["bankroll"],resultat = partie(session["mise"],session["bankroll"],decomposition_cartes)
    
    return render_template('board.html',deck=new_deck,cartes=mapCardsToImg(cartes_tirees),resultat=resultat),201