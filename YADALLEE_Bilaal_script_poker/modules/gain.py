from modules import util

def paire_simple(valeurs: list):
    for valeur in valeurs:
        if util.occurrences(valeurs,valeur,2):
            return True
    return False

def brelan(valeurs: list):
    for valeur in valeurs:
        if util.occurrences(valeurs,valeur,3):
            return True
    return False

def paire_double(valeurs: list):
    resultat = [ util.occurrences(valeurs,valeur,2) for valeur in valeurs ]
    return resultat == [True,True]

def quinte(valeurs: list):
    valeurs = util.convert_cartes(valeurs)
    return sorted(valeurs) == list(range(min(valeurs),max(valeurs)+1))

def flush(couleurs: list):
    return couleurs.count(couleurs[0]) == util.TAILLE_JEU

def full(valeurs: list):
    check_brelan = brelan(valeurs)
    if check_brelan:
        return paire_simple(valeurs)
    else:
        return False

def carre(valeurs:list):
    for valeur in valeurs:
        if util.occurrences(valeurs,valeur,4):
            return True
    return False

def quinte_flush(valeurs: list, couleurs: list):
    return quinte(valeurs) and flush(couleurs)

def quinte_flush_royale(valeurs: list, couleurs: list):
    if flush(couleurs):
        return sorted(util.convert_cartes(['A','K','Q','J','10'])) == sorted(util.convert_cartes(valeurs))
    return False


def partie(mise: int, bankroll: int, ensemble_couleur_valeur: list ):
    """
        Effectue une partie de poker

        Paramètres
        ----------
            mise (int) : la mise du joueur (nécessaire pour calculer les gains)
            bankroll (int) : le montant de la banque
            ensemble_couleur_valeur (list) : liste contenant les couleurs et les valeurs des cartes séparémment (list of dict)

        Sortie
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