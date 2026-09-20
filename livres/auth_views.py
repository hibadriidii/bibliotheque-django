from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages


def connexion_view(request):
    if request.user.is_authenticated:
        return redirect('accueil_client') if not request.user.is_staff else redirect('liste_livres')
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            if user.is_staff or user.is_superuser:
                return redirect('liste_livres')
            return redirect('accueil_client')
        messages.error(request, 'Identifiants incorrects.')
    return render(request, 'auth/connexion.html')


def deconnexion_view(request):
    logout(request)
    return redirect('connexion')


def inscription_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        if password1 != password2:
            messages.error(request, 'Les mots de passe ne correspondent pas.')
        elif User.objects.filter(username=username).exists():
            messages.error(request, 'Ce nom d\'utilisateur est déjà pris.')
        else:
            user = User.objects.create_user(username=username, email=email, password=password1)
            login(request, user)
            messages.success(request, f'Bienvenue, {username} !')
            return redirect('accueil_client')
    return render(request, 'auth/inscription.html')
