from modules import util, gain

deck = ['2-h','3-h','4-h','5-h','6-h','7-h','8-h','9-h','10-h','J-h','Q-h','K-h','A-h','2-d','3-d','4-d','5-d','6-d','7-d','8-d','9-d','10-d','J-d','Q-d','K-d','A-d','2-c','3-c','4-c','5-c','6-c','7-c','8-c','9-c','10-c','J-c','Q-c','K-c','A-c','2-s','3-s','4-s','5-s','6-s','7-s','8-s','9-s','10-s','J-s','Q-s','K-s','A-s']


def choix_carte(tirage):
    """
        Fonction demandant au joueur s'il souhaite conserver
        chaque carte que la machine lui a tiré

        Paramètres
        ----------
            tirage (list) : liste de 5 cartes

        Sortie
        ------
            list : le jeu du joueur

    """
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


def machine(deck):
    """
        Fonction dédiée au fonctionnement de la 'machine' de cartes
        À partir du deck fourni, elle effectue un tirage de 5 cartes
        Puis elle les propose au joueur.

        Cette fonction n'est pas utilisée dans Flask

        Paramètres
        ----------
            deck (list) : le deck avec lequel la machine effectuera les tirages

        Sortie
        ------
            list of dict : une liste de dictionnaire contenant séparément la valeur et la couleur
            de chaque carte
    """
    cartes_tirees,deck = util.tirage(deck)
    print(f"Votre tirage est le suivant : {cartes_tirees}")
    tirage_final = []
    choix = choix_carte(cartes_tirees)
    #Si le joueur ne conserve pas toutes les cartes
    #on effectue le deuxième tirage...
    if len(choix) != util.TAILLE_JEU:
        print("Deuxième tirage...")
        tirage_final,deck = util.tirage(deck,choix)
        print(f"Le tirage final est le suivant : {tirage_final}")
    else: #sinon on conserve ses choix
        tirage_final = choix
    return [ dict({ "couleur": ensemble[1], "valeur": ensemble[0] }) for ensemble in [carte.split("-") for carte in tirage_final ]]
 

def video_poker(bankroll: int):
    """
        Fonction principale qui permet de démarrer un jeu de vidéo poker depuis le terminal

        Paramètres
        ----------
            bankroll (int) : le montant de la banque choisi
            mise (int) : la mise initiale choisie
    """
    try:
        mise  = int(input('Faites vos jeux : '))
        while True:
            if bankroll - mise >= 0:
                # on démarre une partie de poker, on soustrait la banque avec la mise
                bankroll, resultat = gain.partie(mise,bankroll - mise, machine(deck))
                print(f"{resultat}\n")
                print(f"Montant de la banque : {bankroll} €")
            else:
                print('Erreur : mise trop élevée, recommencez la saisie')
            if bankroll == 0:
                break
            reprendre = input('Faire une nouvelle partie ? (y / n) : ')
            while reprendre not in ['y','n']:
                reprendre = input('Saisie invalide : recommencez (y / n) :')
            if reprendre == 'y':    
                mise = int(input('Saisir une nouvelle mise : '))
            else:
                break
        print("Partie terminée ! À bientôt !")
    except Exception as e: #pour capturer l'exception si un caractère invalide a été passé
        print(e)


if __name__ == "__main__":
    #on saisit qu'une et une seule fois le montant de la banque
    bankroll = int(input('Saisir montant de la banque : '))
    video_poker(bankroll)