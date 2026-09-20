from django import template
from livres.models import Commande

register = template.Library()

@register.simple_tag
def commandes_en_attente():
    return Commande.objects.filter(statut='en_attente').count()
