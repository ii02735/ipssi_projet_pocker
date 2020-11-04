import random

TAILLE_JEU = 5
deck = ['2-h','3-h','4-h','5-h','6-h','7-h','8-h','9-h','10-h','J-h','Q-h','K-h','A-h','2-d','3-d','4-d','5-d','6-d','7-d','8-d','9-d','10-d','J-d','Q-d','K-d','A-d','2-c','3-c','4-c','5-c','6-c','7-c','8-c','9-c','10-c','J-c','Q-c','K-c','A-c','2-s','3-s','4-s','5-s','6-s','7-s','8-s','9-s','10-s','J-s','Q-s','K-s','A-s']

# def premier_tirage(deck):
#     random.shuffle(deck)
#     tirage=deck[0:5]
#     deck=deck[5:]
#     return tirage,deck

def tirage(deck,jeu=[]):
    random.shuffle(deck)
    if len(jeu) > 0:
        jeu.extend(deck[0:(TAILLE_JEU - len(jeu))])
        deck = deck[len(jeu):]
        tirage = jeu
    else:
        tirage=deck[0:5]
        deck=deck[5:]
    return tirage,deck


def choix_carte(tirage):
    jeu = []
    for carte_tiree in tirage:
        print(f"Conserver la carte {carte_tiree} ? (y/n)")
        reponse=input()
        while reponse.lower() not in ['y','n']: 
            print("Erreur dans la réponse : réessayez")
            print(f"Conserver la carte {carte_tiree} ? (y/n)")
            reponse=input()
        if reponse == 'y':
            jeu.append(carte_tiree)
    return jeu


def occurrences(valeurs: list,search,occurrences: int):
    """ 
        Vérifie le nombre de doublons

        Paramètres
        ----------
            valeurs: les valeurs des cartes
            search: la valeur à tester
            occurrences: le nombre d'occurrences à tester
        Retour
        ------
            Un booléen pour confirmer le nombre de doublons
    """
    return valeurs.count(search) == occurrences

def paire_simple(valeurs: list):
    for valeur in valeurs:
        if occurrences(valeurs,valeur,2):
            return True
    return False

def brelan(valeurs: list):
    for valeur in valeurs:
        if occurrences(valeurs,valeur,3):
            return True
    return False

def paire_double(valeurs: list):
    resultat = [ occurrences(valeurs,valeur,2) for valeur in valeurs ]
    return resultat == [True,True]

def convert_cartes(valeurs: list):
    dico: dict = { 'A': 1, 'J': 13, 'Q': 14, 'K': 15 }
    valeurs = [ dico.get(valeur) if valeur in dico else int(valeur) for valeur in valeurs ]
    return valeurs

def quinte(valeurs: list):
    valeurs = convert_cartes(valeurs)
    return sorted(valeurs) == list(range(min(valeurs),max(valeurs)+1))

def flush(couleurs: list):
    return couleurs.count(couleurs[0]) == TAILLE_JEU

def full(valeurs: list):
    check_brelan = brelan(valeurs)
    if check_brelan:
        return paire_simple(valeurs)
    else:
        return False

def carre(valeurs:list):
    for valeur in valeurs:
        if occurrences(valeurs,valeur,4):
            return True
    return False

def quinte_flush(valeurs: list, couleurs: list):
    return quinte(valeurs) and flush(couleurs)

def quinte_flush_royale(valeurs: list, couleurs: list):
    if flush(couleurs):
        return sorted(convert_cartes(['A','K','Q','J','10'])) == sorted(convert_cartes(valeurs))
    return False

def machine(deck):
    _tirage,deck = tirage(deck)
    print(f"Votre tirage est le suivant : {_tirage}")
    tirage_final = []
    choix = choix_carte(_tirage)
    if len(choix) != TAILLE_JEU:
        print("Deuxième tirage...")
        tirage_final,deck = tirage(deck,choix)
    else:
        tirage_final = choix
    print(f"Le tirage final est le suivant : {tirage_final}")
    return [ dict({ "couleur": ensemble[1], "valeur": ensemble[0] }) for ensemble in [carte.split("-") for carte in tirage_final ]]



def partie(mise: int, bankroll: int, ensemble_couleur_valeur: list ):
    """
        Effectue une partie de poker

        Paramètres
        ----------
            mise (int) : la mise du joueur
            bankroll (int) : le montant de la banque
            ensemble_couleur_valeur (list) : liste contenant les couleurs et les valeurs des cartes séparémment (list of dict)

        Retour
        ------
        list: Une liste contenant le nouveau montant de la banque et le résultat de la partie
    """
    tirage_final = ensemble_couleur_valeur
    couleurs = [ cartes["couleur"] for cartes in tirage_final ]
    valeurs = [ cartes["valeur"] for cartes in tirage_final ]
    resultat = "Vous avez perdu : retentez votre chance !"
    gain = 0
    #on test du cas le plus rare au plus régulier
    if quinte_flush_royale(valeurs,couleurs):
        gain = mise*250
        resultat = (f"Quinte flush royale ! Vous remportez {gain} €") 
    elif quinte_flush(valeurs,couleurs):
        gain = mise*50
        resultat = (f"Quinte flush ! Vous remportez {gain} €")
    elif carre(valeurs):
        gain = mise*25
        resultat = (f"Carré ! Vous remportez {gain} €")
    elif full(valeurs):
        gain = mise*9
        resultat = (f"Full ! Vous remportez {gain} €")
    elif flush(couleurs):
        gain = mise*6
        resultat = (f"Flush ! Vous remportez {gain} €")
    elif quinte(valeurs):
        gain = mise*4
        resultat = (f"Quinte ! Vous remportez {gain} €")
    elif brelan(valeurs):
        gain = mise*3
        resultat = (f"Brelan ! Vous remportez {gain} €")
    elif paire_double(valeurs):
        gain = mise*2
        resultat = (f"Double paire ! Vous remportez {gain} €")
    elif paire_simple(valeurs):
        gain = mise
        resultat =(f"Paire ! Vous remportez {mise} €")
    
    bankroll += gain    
    return bankroll, resultat   

def video_poker(bankroll: int, mise: int):
    try:
        while True:
            if bankroll - mise_joueur >= 0:
                bankroll, resultat = partie(mise_joueur,bankroll - mise, machine(deck))
                print(f"{resultat}\n")
                print(f"Montant de la banque : {bankroll} €")
            else:
                print('Erreur : mise trop élevée, recommencez la saisie')
            if bankroll == 0:
                break
        print("Partie terminée ! À bientôt !")
    except Exception as e:
        print(e)


if __name__ == "__main__":
    bankroll = int(input('Saisir montant de la banque : '))
    mise_joueur = int(input('Faites vos jeux : '))
    video_poker(bankroll,mise_joueur)