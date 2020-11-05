import random
from flask import url_for

TAILLE_JEU = 5

# fonctions utilitaires et destinées à être réutilisées

def tirage(deck,jeu=[]):
    """
        Permet de mélanger le deck
        
        Puis retourne une liste de 5 cartes aléatoirement

        Paramètres
        ----------
            deck (list) : deck sur quoi le brassage devra se baser
            jeu (list) : tableau optionnel contenant le jeu du joueur et à remplir 
            à partir des cartes choisies aléatorement

        Sortie
        ------
            list : une liste de 5 cartes choisies aléatoirement
            deck : le deck mis à jour après mélange sans remise
    """
    random.shuffle(deck)
    if len(jeu) > 0:
        jeu.extend(deck[0:(TAILLE_JEU - len(jeu))])
        deck = deck[len(jeu):]
        tirage = jeu
    else:
        tirage=deck[0:5]
        deck=deck[5:]
    return tirage,deck

def occurrences(valeurs: list,search,occurrences: int):
    """ 
        Vérifie le nombre de doublons

        Paramètres
        ----------
            valeurs: les valeurs des cartes
            search: la valeur à tester
            occurrences: le nombre d'occurrences à tester
        Sortie
        ------
            Un booléen pour confirmer le nombre de doublons
    """
    return valeurs.count(search) == occurrences


def convert_cartes(valeurs: list):
    """
        Fonction permettant de traduire des cartes
        ayant des valeurs non numériques

        Paramètres
        ----------
            valeurs (list) : liste de cartes
        
        Sortie
        ------
            list : une liste contenant que des entiers
    """
    dico: dict = { 'A': 1, 'J': 13, 'Q': 14, 'K': 15 }
    valeurs = [ dico.get(valeur) if valeur in dico else int(valeur) for valeur in valeurs ]
    return valeurs

# côté Flask :

def mapCardsToImg(cards: list):
    """
        Fonction permettant de faire correspondre chaque carte au bon fichier image

        Paramètres
        ----------
            cards (list) : Liste de cartes, donc ici de str (exemple : ['1-d','A-c'...])
        
        Sortie
        ------
            list of dico : Une liste de dictionnaire contenant une carte avec son image en url
    """
    dico_card_map = []
    for card in cards:
        dico_card_map.append({ 'carte': card, 'img': url_for('static',filename=f"img/{card}.svg") })
    return dico_card_map