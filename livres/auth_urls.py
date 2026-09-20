from django.urls import path
from . import auth_views

urlpatterns = [
    path('connexion/', auth_views.connexion_view, name='connexion'),
    path('deconnexion/', auth_views.deconnexion_view, name='deconnexion'),
    path('inscription/', auth_views.inscription_view, name='inscription'),
]
