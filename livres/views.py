from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.db.models import Q
from .models import Livre, Commande
from .forms import LivreForm, CommandeClientForm, CommandeAdminForm


def is_admin(user):
    return user.is_staff or user.is_superuser


# ══════════════════════════════════════
#  ADMIN — LIVRES
# ══════════════════════════════════════

@login_required
@user_passes_test(is_admin)
def liste_livres(request):
    query = request.GET.get('q', '')
    categorie = request.GET.get('categorie', '')
    statut = request.GET.get('statut', '')
    livres = Livre.objects.all()
    if query:
        livres = livres.filter(Q(titre__icontains=query) | Q(auteur__icontains=query) | Q(id__icontains=query))
    if categorie:
        livres = livres.filter(categorie=categorie)
    if statut:
        livres = livres.filter(statut=statut)
    stats = {
        'total':       Livre.objects.count(),
        'disponibles': Livre.objects.filter(statut='disponible').count(),
        'empruntes':   Livre.objects.filter(statut='emprunte').count(),
        'commandes':   Commande.objects.filter(statut='en_attente').count(),
    }
    return render(request, 'livres/admin/liste.html', {
        'livres': livres, 'query': query, 'categorie_filtre': categorie,
        'statut_filtre': statut, 'categories': Livre.CATEGORIE_CHOICES, 'stats': stats,
    })


@login_required
@user_passes_test(is_admin)
def detail_livre(request, pk):
    livre = get_object_or_404(Livre, pk=pk)
    rows = [
        ('ID', f'#{livre.id}'), ('Catégorie', livre.categorie),
        ('Année', livre.annee_publication), ('Quantité', livre.quantite_disponible),
        ('Statut', livre.get_statut_display_fr()),
        ('Retour prévu', livre.date_retour_prevu.strftime('%d/%m/%Y') if livre.date_retour_prevu else '—'),
    ]
    return render(request, 'livres/admin/detail.html', {'livre': livre, 'rows': rows})


@login_required
@user_passes_test(is_admin)
def ajouter_livre(request):
    if request.method == 'POST':
        form = LivreForm(request.POST, request.FILES)
        if form.is_valid():
            livre = form.save()
            messages.success(request, f'"{livre.titre}" a été ajouté.')
            return redirect('liste_livres')
    else:
        form = LivreForm()
    return render(request, 'livres/admin/formulaire.html', {
        'form': form, 'titre_page': 'Enregistrer un volume', 'action': 'Enregistrer'
    })


@login_required
@user_passes_test(is_admin)
def modifier_livre(request, pk):
    livre = get_object_or_404(Livre, pk=pk)
    if request.method == 'POST':
        form = LivreForm(request.POST, request.FILES, instance=livre)
        if form.is_valid():
            form.save()
            messages.success(request, f'"{livre.titre}" a été modifié.')
            return redirect('liste_livres')
    else:
        form = LivreForm(instance=livre)
    return render(request, 'livres/admin/formulaire.html', {
        'form': form, 'titre_page': f'Modifier "{livre.titre}"', 'action': 'Modifier', 'livre': livre
    })


@login_required
@user_passes_test(is_admin)
def supprimer_livre(request, pk):
    livre = get_object_or_404(Livre, pk=pk)
    if request.method == 'POST':
        titre = livre.titre
        livre.delete()
        messages.success(request, f'"{titre}" a été retiré.')
        return redirect('liste_livres')
    return render(request, 'livres/admin/confirmer_suppression.html', {'livre': livre})


# ══════════════════════════════════════
#  ADMIN — COMMANDES
# ══════════════════════════════════════

@login_required
@user_passes_test(is_admin)
def admin_commandes(request):
    statut_filtre = request.GET.get('statut', '')
    commandes = Commande.objects.select_related('client', 'livre').all()
    if statut_filtre:
        commandes = commandes.filter(statut=statut_filtre)
    stats = {s: Commande.objects.filter(statut=s).count() for s, _ in Commande.STATUT_CHOICES}
    return render(request, 'livres/admin/commandes.html', {
        'commandes': commandes, 'statut_filtre': statut_filtre,
        'statuts': Commande.STATUT_CHOICES, 'stats': stats,
    })


@login_required
@user_passes_test(is_admin)
def admin_statut_commande(request, pk):
    commande = get_object_or_404(Commande, pk=pk)
    if request.method == 'POST':
        form = CommandeAdminForm(request.POST, instance=commande)
        if form.is_valid():
            form.save()
            messages.success(request, f'Commande #{commande.id} mise à jour.')
            return redirect('admin_commandes')
    else:
        form = CommandeAdminForm(instance=commande)
    rows = [
        ('Client', commande.client.username),
        ('Date de commande', commande.date_commande.strftime('%d/%m/%Y %H:%M')),
        ('Statut actuel', commande.get_statut_display_fr()),
    ]
    return render(request, 'livres/admin/statut_commande.html', {'commande': commande, 'form': form, 'rows': rows})


# ══════════════════════════════════════
#  CLIENT
# ══════════════════════════════════════

@login_required
def accueil_client(request):
    query = request.GET.get('q', '')
    categorie = request.GET.get('categorie', '')
    livres = Livre.objects.all()
    if query:
        livres = livres.filter(Q(titre__icontains=query) | Q(auteur__icontains=query))
    if categorie:
        livres = livres.filter(categorie=categorie)
    return render(request, 'livres/client/catalogue.html', {
        'livres': livres, 'query': query, 'categorie_filtre': categorie,
        'categories': Livre.CATEGORIE_CHOICES,
        'total': Livre.objects.count(),
        'disponibles': Livre.objects.filter(statut='disponible').count(),
    })


@login_required
def detail_client(request, pk):
    livre = get_object_or_404(Livre, pk=pk)
    suggestions = Livre.objects.filter(categorie=livre.categorie).exclude(pk=pk)[:3]
    commande_active = Commande.objects.filter(
        client=request.user, livre=livre
    ).exclude(statut__in=['annulee', 'rendue']).first()
    rows = [
        ('Catégorie', livre.categorie), ('Année', livre.annee_publication),
        ('Quantité', livre.quantite_disponible),
    ]
    return render(request, 'livres/client/detail.html', {
        'livre': livre, 'suggestions': suggestions, 'commande_active': commande_active, 'rows': rows,
    })


@login_required
def commander_livre(request, pk):
    livre = get_object_or_404(Livre, pk=pk)
    # Vérifier si le client a déjà une commande active
    commande_active = Commande.objects.filter(
        client=request.user, livre=livre
    ).exclude(statut__in=['annulee', 'rendue']).first()
    if commande_active:
        messages.error(request, 'Vous avez déjà une commande active pour ce livre.')
        return redirect('detail_client', pk=pk)
    if livre.statut not in ('disponible',):
        messages.error(request, 'Ce livre n\'est pas disponible pour le moment.')
        return redirect('detail_client', pk=pk)
    if request.method == 'POST':
        form = CommandeClientForm(request.POST)
        if form.is_valid():
            commande = form.save(commit=False)
            commande.client = request.user
            commande.livre = livre
            commande.save()
            messages.success(request, f'Votre demande pour « {livre.titre} » a été enregistrée !')
            return redirect('mes_commandes')
    else:
        form = CommandeClientForm()
    return render(request, 'livres/client/commander.html', {'livre': livre, 'form': form})


@login_required
def mes_commandes(request):
    commandes = Commande.objects.filter(client=request.user).select_related('livre')
    return render(request, 'livres/client/mes_commandes.html', {'commandes': commandes})


@login_required
def annuler_commande(request, pk):
    commande = get_object_or_404(Commande, pk=pk, client=request.user)
    if not commande.peut_annuler():
        messages.error(request, 'Cette commande ne peut plus être annulée.')
        return redirect('mes_commandes')
    if request.method == 'POST':
        commande.statut = 'annulee'
        commande.save()
        messages.success(request, f'Votre commande pour « {commande.livre.titre} » a été annulée.')
        return redirect('mes_commandes')
    return render(request, 'livres/client/confirmer_annulation.html', {'commande': commande})

# Patch: add rows to admin_statut_commande - already inline in template
