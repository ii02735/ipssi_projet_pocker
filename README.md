## Projet vidéo poker en Python

Ce projet proposé par IPSSI, a été réalisé pour valider les acquis en Python.

Ce projet a consisté à rédiger un programme imitant le fonctionnement d'un vidéo-poker dans une première partie.

En seconde partie, une IHM Web a été construite à partir du micro-framwork *Flask*.

## Procédure

1. Mettre en place un environnement virtuelle de préférence
2. Installer la dépendance de *Flask* : `pip install Flask`

## Lancement

- Pour lancer le **script** du vidéo-poker, exécuter le fichier **script_poker.py**

- Pour lancer l'IHM web de Flask, exécuter le fichier **app.py**
    - Remarque : aucune configuration touchant la variables n'est nécessaire. Exécuter le fichier suffit.

    - Si des problèmes apparaissent, faire les manipulations suivantes :

      - Sur une machine **Unix** (Linux, Mac) : 
        ```sh
        export FLASK_APP=app.py
        export FLASK_ENV=development
        flask run #pour exécuter l'IHM
        ```
     
       - Sur une machine **Windows** :
         - CMD :
            ```bat
            set FLASK_APP=app.py
            set FLASK_ENV=development
            flask run
            ``` 
         - Powershell
            ```PS
            $env:FLASK_APP = "app.py"
            $env:FLASK_ENV = "development"
            flask run
            ```