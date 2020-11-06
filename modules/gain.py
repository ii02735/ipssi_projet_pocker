from modules import util


def paire_simple(valeurs: list):
    """
        Fonction détectant une paire dans le jeu du joueur

        Paramètres
        ----------

            valeurs (list) : une liste contenant la valeur de chaque carte

        Sortie
        ------
            bool : un booléen confirmant s'il y a paire ou non
    """
    for valeur in valeurs:
        #
        # Rappelons-nous que la fonction occurrences permet
        # de détecter le nombre de doublons depuis une liste
        # d'entier (soit la liste des valeurs des cartes)
        #
        # On examine chaque chaque carte, et on regarde si ici
        # on a 2 occurrences
        #
        if util.occurrences(valeurs,valeur,2):
            return True
    return False

def brelan(valeurs: list):
    """
        Fonction détectant un brelan (trois cartes de même valeur) dans le jeu du joueur

        Paramètres
        ----------

            valeurs (list) : une liste contenant la valeur de chaque carte

        Sortie
        ------
            bool : un booléen confirmant s'il y a un brelan ou non
    """
    for valeur in valeurs:
        if util.occurrences(valeurs,valeur,3):
            return True
    return False

def paire_double(valeurs: list):
    """
        Fonction détectant une paire double dans le jeu du joueur

        Paramètres
        ----------

            valeurs (list) : une liste contenant la valeur de chaque carte

        Sortie
        ------
            bool : un booléen confirmant s'il y a un brelan ou non
    """

    # À partir d'une comprehension list, on regarde le nombre d'occurrences ayant des paires
    resultat = [ util.occurrences(valeurs,valeur,2) for valeur in valeurs ]
    # Puisque la fonction occurrences renvoie un booléen, si le tableau en contient deux
    # donc on a deux paires différentes
    return resultat == [True,True]

def quinte(valeurs: list):
    """
        Fonction détectant une quinte (suite de cartes consécutives selon 
        leur valeur)  dans le jeu du joueur

        Paramètres
        ----------

            valeurs (list) : une liste contenant la valeur de chaque carte

        Sortie
        ------
            bool : un booléen confirmant s'il y a une quinte ou non
    """

    # Si le jeu du joueur contient des valeurs non numériques (J,Q,K,A)
    # on doit les convertir en valeurs numériques
    valeurs = util.convert_cartes(valeurs)
    # si le tableau trié des valeurs, correspond à une suite de valeurs
    # (conversion d'une suite de chiffres en liste pour effectuer la comparaison)
    # alors on a affaire à une quinte
    return sorted(valeurs) == list(range(min(valeurs),max(valeurs)+1))

def flush(couleurs: list):
    """
        Fonction détectant un flush (cartes de même couleur / symbole) 
        dans le jeu du joueur

        Paramètres
        ----------

            couleur (list) : une liste contenant la couleur de chaque carte

        Sortie
        ------
            bool : un booléen confirmant s'il y a un flush ou non
    """

    #Si la première couleur du jeu de carte est contenu 5 fois
    #soit la taille du jeu du joueur, alors on a un flush
    return couleurs.count(couleurs[0]) == util.TAILLE_JEU

def full(valeurs: list):
    """
        Fonction détectant un full (paire + brelan) dans le jeu du joueur

        Paramètres
        ----------

            valeurs (list) : une liste contenant la valeur de chaque carte

        Sortie
        ------
            bool : un booléen confirmant s'il y a un full ou non
    """
    #on détecte en premier si on a un brelan
    check_brelan = brelan(valeurs)
    if check_brelan: 
        #si cela est vrai, le résultat de la fonction paire_simple déterminera
        #s'il y a bien un full
        return paire_simple(valeurs)
    else:
        return False

def carre(valeurs:list):
    """
        Fonction détectant un carré (4 cartes de même valeur) dans le jeu du joueur

        Paramètres
        ----------

            valeurs (list) : une liste contenant la valeur de chaque carte

        Sortie
        ------
            bool : un booléen confirmant s'il y a un brelan ou non
    """
    for valeur in valeurs:
        if util.occurrences(valeurs,valeur,4):
            return True
    return False

def quinte_flush(valeurs: list, couleurs: list):
    """
        Fonction détectant un quinte flush (quinte + flush) dans le jeu du joueur

        Paramètres
        ----------

            valeurs (list) : une liste contenant la valeur de chaque carte
            couleurs (list) : une liste contenant la couleur de chaque carte

        Sortie
        ------
            bool : un booléen confirmant s'il y a un quinte flush ou non
    """
    # on réutilise simplement la fonction quinte et flush pour retourner le booléen
    return quinte(valeurs) and flush(couleurs)

def quinte_flush_royale(valeurs: list, couleurs: list):
    """
        Fonction détectant un quinte flush royal 
        (quinte + flush + les cartes As (Ace), Roi (King), Reine (Queen), 10) 
        dans le jeu du joueur

        Paramètres
        ----------

            valeurs (list) : une liste contenant la valeur de chaque carte
            couleurs (list) : une liste contenant la couleur de chaque carte

        Sortie
        ------
            bool : un booléen confirmant s'il y a un brelan ou non
    """
    if flush(couleurs): #si on a un flush, il est possible d'avoir un qunite flush royal
        # Il faut que la liste triée des valeurs soit une suite numérique
        # c'est pour cela qu'on convertit les valeurs des cartes + cette suite doit comporter
        # des éléments précis
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