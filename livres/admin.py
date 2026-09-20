from django.contrib import admin
from .models import Livre


@admin.register(Livre)
class LivreAdmin(admin.ModelAdmin):
    list_display = ['id', 'titre', 'auteur', 'categorie', 'annee_publication', 'statut', 'quantite_disponible']
    list_filter = ['categorie', 'statut']
    search_fields = ['titre', 'auteur']
    list_editable = ['statut', 'quantite_disponible']
