#!/usr/bin/env python
"""
Script pour peupler la bibliothèque avec des données d'exemple.
Exécuter avec : python seed_data.py
(depuis le répertoire du projet, après les migrations)
"""
import os
import sys
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bibliotheque.settings')
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
django.setup()

from livres.models import Livre
from datetime import date

livres_exemple = [
    {
        'titre': 'Le Petit Prince',
        'auteur': 'Antoine de Saint-Exupéry',
        'categorie': 'Roman',
        'annee_publication': 1943,
        'quantite_disponible': 3,
        'statut': 'disponible',
        'description': 'Un conte poétique et philosophique sur un petit prince voyageur.'
    },
    {
        'titre': 'Les Misérables',
        'auteur': 'Victor Hugo',
        'categorie': 'Roman',
        'annee_publication': 1862,
        'quantite_disponible': 0,
        'statut': 'emprunte',
        'date_retour_prevu': date(2026, 6, 15),
        'description': 'L\'histoire de Jean Valjean dans la France du XIXe siècle.'
    },
    {
        'titre': 'Notre-Dame de Paris',
        'auteur': 'Victor Hugo',
        'categorie': 'Roman',
        'annee_publication': 1831,
        'quantite_disponible': 2,
        'statut': 'disponible',
        'description': 'Le drame de Quasimodo et Esméralda.'
    },
    {
        'titre': 'Les Contemplations',
        'auteur': 'Victor Hugo',
        'categorie': 'Poésie',
        'annee_publication': 1856,
        'quantite_disponible': 1,
        'statut': 'disponible',
    },
    {
        'titre': 'Orgueil et Préjugés',
        'auteur': 'Jane Austen',
        'categorie': 'Roman',
        'annee_publication': 1813,
        'quantite_disponible': 2,
        'statut': 'disponible',
        'description': 'Les aventures amoureuses d\'Elizabeth Bennet.'
    },
    {
        'titre': 'Python pour les nuls',
        'auteur': 'John Paul Mueller',
        'categorie': 'Informatique',
        'annee_publication': 2020,
        'quantite_disponible': 4,
        'statut': 'disponible',
        'description': 'Introduction complète à Python pour les débutants.'
    },
    {
        'titre': 'Deep Learning',
        'auteur': 'Ian Goodfellow',
        'categorie': 'Informatique',
        'annee_publication': 2016,
        'quantite_disponible': 1,
        'statut': 'reserve',
        'description': 'La référence du deep learning.'
    },
    {
        'titre': 'Sapiens',
        'auteur': 'Yuval Noah Harari',
        'categorie': 'Histoire',
        'annee_publication': 2015,
        'quantite_disponible': 2,
        'statut': 'disponible',
        'description': 'Une brève histoire de l\'humanité.'
    },
    {
        'titre': 'L\'Étranger',
        'auteur': 'Albert Camus',
        'categorie': 'Roman',
        'annee_publication': 1942,
        'quantite_disponible': 0,
        'statut': 'emprunte',
        'date_retour_prevu': date(2026, 6, 20),
        'description': 'Meursault face à l\'absurde de l\'existence.'
    },
    {
        'titre': 'Une brève histoire du temps',
        'auteur': 'Stephen Hawking',
        'categorie': 'Science',
        'annee_publication': 1988,
        'quantite_disponible': 2,
        'statut': 'disponible',
        'description': 'Les mystères de l\'univers expliqués au grand public.'
    },
]

Livre.objects.all().delete()
for data in livres_exemple:
    Livre.objects.create(**data)

print(f"✅ {Livre.objects.count()} livres ajoutés avec succès !")
