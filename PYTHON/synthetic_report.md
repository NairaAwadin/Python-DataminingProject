# SYNTHETIC REPORT : BANK PROCESSING, DNA PROCESSING, SCRAPPING

Contributeurs : Léo, Yane, Paul, Mika et Naira
Date : 19/10/2025
Langage : Python
Bibliothèques utilisées : tkinter, requests
Norme de commits : [ADD], [MODIF], [SUPP]

-------------------------------------------------------------

## BANk PROCESSING

### OBJECTIF DU PROJET

Le projet Bank Processing vise à automatiser la génération et la vérification d'IBANs à partir d'un fichier texte mais également une saisie manuelle.
Il permet :
    - Extraire les informations d'un RIB à partir d'un fichier .txt
    - Générer un IBAN français valide
    - Et le vérifier grâce à l'API OpenIBAN

### MÉTHODOLOGIE

#### Architecture du code

Lecture et extraction du fichier

-> open_file(file_name) : ouvre le fichier .txt et vérifie s'il est vide ou inexistant

-> extract_iban(file_content) : parcourt le contenu pour extraire les champs de l'IBAN :
    - Code Banque, Code agence, Numero de compte banquaire, Chiffre d'indicatif national
    - Ignore les lignes dont le dernier mot est un mot clé pcq ca voudrait dire qu'il n y a pas de valeur à extraire

-> charger_fichier() : charge un fichier .txt, extrait les champs IBAN, remplit l’interface et affiche un message d’erreur si nécessaire

Génération de l’IBAN

-> lettre_to_chiffre(c) : convertit les lettres en nombres(ex: A=10, etc)

-> calculer_cle(banque, agence, compte, cle_rib) : calcule la clé IBAN selon l'algorithme mod 97

-> genrer_iban() : assemble les informations de l'IBAN sous le format :
    FR{clé}{banque}{agence}{compte}{cle_rib} et affiche l'iban dans l'interface GUI

Vérification de l'IBAN

-> verifier_api() : envoie une requête à l'API OpenIban pour verifier si iban valide
    retourne :
        - Retourne le message “✔️ IBAN valide” ou “❌ IBAN invalide”

Interface graphique (GUI)

-> Interface constuite avec Tkinter
-> Permet de charger un fichiern afficher les valeurs extraites et générer puis vérifier un IBAN
-> On a utilisé des labels, boutons, champs de saisie et messages d'erreurs colorés

### RESULTATS

#### Interface principale

Pemet de :
    - Charger un fichier .txt
    - Génerer un IBAN automatiquement avec le choix entre une clé iban fixe et une clé dynamique
    - Vérifier un IBAN via une API externe

![Interface generateur iban](Bank_Processing/images/interface_iban.jpg)

#### Tests IBAN valides / non valides

Test 1 : Iban généré à partir du fichier bankaccount.txt avec une clé calculé dynamiquement

Code banque	20041
Code agence	01005
Numero de compte bancaire	0500013M026
Chiffre d'indicatif national	E1

-> Résultat : la clé est calculé dynamiquement, elle est égale à 82 et on a le message "IBAN valide" qui s'affiche, lorsqu'on vérfie l'iban

![Test 1](Bank_Processing/images/test_1.jpg)

Test 2 : Iban généré à partir du meme fichier .txt, cette fois ci avec une clé static

-> Résultat : la clé qui s'affiche au debut de l'iban est une clé fixe = à 14, et lorsqu'on vérifie l'IBAN, le message "IBAN invalide" s'affiche en rouge.

![Test 2](Bank_Processing/images/test_2.jpg)

#### Tests de gestion d'erreurs

Test 3 : Fichier vide
-> Résultat : On a le message "Le fichier est vide !" qui s'affiche lorsqu"on essaye de télécharger un fichier vide

![Test 3](Bank_Processing/images/test_3.jpg)

Test 4 : champs manquants - On enlève la ligne "Chiffre d'indicatif national	E1" du fichier
-> Résultat : On a le message "Informations manquantes dnas le fichier" qui s'affiche en rouge

![Test 4](Bank_Processingimages/test_4.jpg)

Test 5 : si je supprime une valeur manuellement (ex : le numéro de compte)
-> Résultat : Le message "Champs manquants" s'affiche en rouge

![Test 5](Bank_Processing/images/test_5.jpg)

Test 6 : Si je supprime manuellement la case IBAN généré
-> Résultat : Le message "Aucun IBAN généré à vérifier s'affiche en rouge"

![Test 6](Bank_Processing/images/test_6.jpg)

Test 7 : seulement la valeur à extraire manque - Exemple de fichier .txt

Code banque	20041
Code agence	01005
Numero de compte bancaire
Chiffre d'indicatif national	E1

-> Résultat : On remarque qu'il manque la valeur à extraire qui corresond au "Numero de compte banquaire" - Le message "Informations manquantes dnas le fichier" s'affiche dans l'interface en rouge

Test 8 : si l'orthographe des mots clés à extraire est incorrecte (ex: chifre au lieu de chiffre)

-> Résultat : L'information n'est pas récupérée, car le programme recherche les mots exactes définis dans extract_iban() - Le message "Informations manquantes dnas le fichier" s'affiche dans l'interface en rouge

![Test 7 et 8](Bank_Processing/images/test_7et8.jpg)

Test 9 : Si on change l'ordre des informations à extraire

Numero de compte bancaire	0500013M026
Chiffre d'indicatif national	E1
Code banque	20041
Code agence	01005

-> Résultat : Le programme recupère quand même les informations de l'IBAN correctement

![Test 9](Bank_Processing/images/test_9.jpg)

### ANALYSE ET COMMENTAIRES

-> Le programme est plutôt robuste : il gère les erreurs courantes sans planter
-> L'interface Tkinter est simple et intuitive
-> Le test API garantit une validation externe et fiable

#### Limites

-> Le script est limité au format IBAN français(FR...)

#### Améliorations futures possibles

-> Génération d'IBANs multi-pays
-> Interface plus ergonomique

### CONCLUSION

Le générateur IBAN est un outil combiant :
-> Traitement de fichier texte
-> Calcul algorithmique
-> Interface graphique(Tkinter)
-> Connexion à une API externe

-------------------------------------------------------------

## DNA PROCESSING

...

-------------------------------------------------------------

## SCRAPPING

...