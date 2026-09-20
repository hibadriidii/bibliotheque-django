from .models import Commande

def commandes_count(request):
    if request.user.is_authenticated and (request.user.is_staff or request.user.is_superuser):
        return {'commandes_en_attente': Commande.objects.filter(statut='en_attente').count()}
    return {'commandes_en_attente': 0}
