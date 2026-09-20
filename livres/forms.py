from django import forms
from .models import Livre, Commande


class LivreForm(forms.ModelForm):
    class Meta:
        model = Livre
        fields = ['titre', 'auteur', 'categorie', 'annee_publication',
                  'quantite_disponible', 'statut', 'date_retour_prevu', 'description', 'image']
        widgets = {
            'titre':               forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Titre du livre'}),
            'auteur':              forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Nom de l\'auteur'}),
            'categorie':           forms.Select(attrs={'class': 'form-input'}),
            'annee_publication':   forms.NumberInput(attrs={'class': 'form-input'}),
            'quantite_disponible': forms.NumberInput(attrs={'class': 'form-input', 'min': '0'}),
            'statut':              forms.Select(attrs={'class': 'form-input'}),
            'date_retour_prevu':   forms.DateInput(attrs={'class': 'form-input', 'type': 'date'}),
            'description':         forms.Textarea(attrs={'class': 'form-input', 'rows': 3}),
            'image':               forms.ClearableFileInput(attrs={'class': 'form-input'}),
        }
        labels = {
            'titre': 'Titre', 'auteur': 'Auteur', 'categorie': 'Catégorie',
            'annee_publication': 'Année', 'quantite_disponible': 'Quantité',
            'statut': 'Statut', 'date_retour_prevu': 'Date de retour prévue',
            'description': 'Description', 'image': 'Image de couverture',
        }


class CommandeClientForm(forms.ModelForm):
    class Meta:
        model = Commande
        fields = ['note_client']
        widgets = {
            'note_client': forms.Textarea(attrs={
                'class': 'form-input', 'rows': 3,
                'placeholder': 'Message pour le bibliothécaire (optionnel)…'
            }),
        }
        labels = {'note_client': 'Note pour le bibliothécaire'}


class CommandeAdminForm(forms.ModelForm):
    class Meta:
        model = Commande
        fields = ['statut', 'date_retour_prevu', 'note_admin']
        widgets = {
            'statut':            forms.Select(attrs={'class': 'form-input'}),
            'date_retour_prevu': forms.DateInput(attrs={'class': 'form-input', 'type': 'date'}),
            'note_admin':        forms.Textarea(attrs={'class': 'form-input', 'rows': 3,
                                                       'placeholder': 'Note interne…'}),
        }
        labels = {
            'statut': 'Statut de la commande',
            'date_retour_prevu': 'Date de retour prévue',
            'note_admin': 'Note interne',
        }
