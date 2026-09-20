from django.urls import path
from . import views

urlpatterns = [
    # ── ADMIN ──
    path('', views.liste_livres, name='liste_livres'),
    path('<int:pk>/', views.detail_livre, name='detail_livre'),
    path('ajouter/', views.ajouter_livre, name='ajouter_livre'),
    path('<int:pk>/modifier/', views.modifier_livre, name='modifier_livre'),
    path('<int:pk>/supprimer/', views.supprimer_livre, name='supprimer_livre'),
    path('commandes/', views.admin_commandes, name='admin_commandes'),
    path('commandes/<int:pk>/statut/', views.admin_statut_commande, name='admin_statut_commande'),

    # ── CLIENT ──
    path('catalogue/', views.accueil_client, name='accueil_client'),
    path('catalogue/<int:pk>/', views.detail_client, name='detail_client'),
    path('catalogue/<int:pk>/commander/', views.commander_livre, name='commander_livre'),
    path('mes-commandes/', views.mes_commandes, name='mes_commandes'),
    path('mes-commandes/<int:pk>/annuler/', views.annuler_commande, name='annuler_commande'),
]
