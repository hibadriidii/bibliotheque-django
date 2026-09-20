from django.db import models
from django.contrib.auth.models import User


class Livre(models.Model):
    STATUT_CHOICES = [
        ('disponible', 'Disponible'),
        ('emprunte', 'Emprunté'),
        ('reserve', 'Réservé'),
    ]
    CATEGORIE_CHOICES = [
        ('Roman', 'Roman'),
        ('Science', 'Science'),
        ('Histoire', 'Histoire'),
        ('Informatique', 'Informatique'),
        ('Philosophie', 'Philosophie'),
        ('Poésie', 'Poésie'),
        ('Biographie', 'Biographie'),
        ('Autre', 'Autre'),
    ]

    titre               = models.CharField(max_length=300)
    auteur              = models.CharField(max_length=200)
    categorie           = models.CharField(max_length=50, choices=CATEGORIE_CHOICES, default='Autre')
    annee_publication   = models.IntegerField()
    quantite_disponible = models.IntegerField(default=1)
    statut              = models.CharField(max_length=20, choices=STATUT_CHOICES, default='disponible')
    date_retour_prevu   = models.DateField(null=True, blank=True)
    description         = models.TextField(blank=True, default='')
    image               = models.ImageField(upload_to='livres/', null=True, blank=True)

    class Meta:
        verbose_name = 'Livre'
        verbose_name_plural = 'Livres'
        ordering = ['titre']

    def __str__(self):
        return f"{self.titre} — {self.auteur}"

    def get_statut_display_fr(self):
        return {'disponible': 'Disponible', 'emprunte': 'Emprunté', 'reserve': 'Réservé'}.get(self.statut, self.statut)

    def get_emoji(self):
        return {
            'Informatique': '💻', 'Science': '🔬', 'Histoire': '⚔️',
            'Poésie': '🖋️', 'Philosophie': '🤔', 'Biographie': '👤',
            'Roman': '📖',
        }.get(self.categorie, '📚')


class Commande(models.Model):
    STATUT_CHOICES = [
        ('en_attente', 'En attente'),
        ('confirmee',  'Confirmée'),
        ('prete',      'Prête à retirer'),
        ('en_cours',   'En cours'),
        ('rendue',     'Rendue'),
        ('annulee',    'Annulée'),
    ]

    client            = models.ForeignKey(User, on_delete=models.CASCADE, related_name='commandes')
    livre             = models.ForeignKey(Livre, on_delete=models.CASCADE, related_name='commandes')
    statut            = models.CharField(max_length=20, choices=STATUT_CHOICES, default='en_attente')
    date_commande     = models.DateTimeField(auto_now_add=True)
    date_retour_prevu = models.DateField(null=True, blank=True)
    note_client       = models.TextField(blank=True, default='')
    note_admin        = models.TextField(blank=True, default='')

    class Meta:
        verbose_name = 'Commande'
        verbose_name_plural = 'Commandes'
        ordering = ['-date_commande']

    def __str__(self):
        return f"Commande #{self.id} — {self.client.username} — {self.livre.titre}"

    def get_statut_display_fr(self):
        return dict(self.STATUT_CHOICES).get(self.statut, self.statut)

    def peut_annuler(self):
        return self.statut in ('en_attente', 'confirmee', 'prete')

    def get_statut_couleur(self):
        return {
            'en_attente': 'or',
            'confirmee':  'bleu',
            'prete':      'vert',
            'en_cours':   'vert',
            'rendue':     'gris',
            'annulee':    'rouge',
        }.get(self.statut, 'gris')
