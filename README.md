# Projet 9 Développeur d'application Python : Développez une application Web en utilisant Django

## Informations générales

Ce projet constitue un examen dans le cadre du parcours Développeur d'application Python d'OpenClassrooms, il est codé
avec le langage Python.
Concrètement, il consiste à créer une application permettant de publier et de consulter des critiques de livres.

## Auteur

Fabien ROYER

## Contributions

Le projet est achevé depuis février 2024.

## Installation

Création de l'environnement :
python -m venv env

Lancement de l'environnement :
env\Scripts\activate

Utilisez le _package installer_ [pip](https://pypi.org/project/pip/) pour installer les packages inclus dans le fichier 
requirements.txt, pour cela utilisez dans le terminal la commande :

```bash
pip install -r requirements.txt
```

## Utilisation

Pour exécuter le code, il faut entrer la commande suivante dans le terminal :

```bash
python manage.py runserver
```

Une url sera affichée en retour dans le terminal, il faut entrer cette url dans un navigateur de recherche.
URL : http://127.0.0.1:8000/

Il est possible de se connecter avec les informations suivantes :
Utilisateur : admin
Mot de passe : admin

Il est possible de créer un nouvel utilisateur à l'url suivante :
http://127.0.0.1:8000/login/

Il est possible d'accéder au site d'administration avec l'url suivante :
http://127.0.0.1:8000/admin/

Ce programme permet de créer des critiques de livres, de demander des critiques de livres, de suivre des utilisateurs
pour consulter leurs critiques de livres ou leurs demandes de critiques. Il est également possible de modifier
ou supprimer ses propres critiques.
