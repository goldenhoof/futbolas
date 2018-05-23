from django.urls import path
from . import views
from .forms import LoginForm
import django.contrib.auth.views as auth_views

urlpatterns = [
    path('', views.index, name='index'),
    path('tvarkarastis/', views.tvarkarastis, name='tvarkarastis'),
    path('sign_up/', views.sign_up, name='sign_up'),
    path('sign_in/', auth_views.LoginView.as_view(template_name='apas/sign_in.html', authentication_form=LoginForm), name='sign_in'),
    path('sign_out/', auth_views.LogoutView.as_view(next_page='/'), name='sign_out'),

    path('pasirinkimas/<id>/<pasirinkimas>', views.pasirinkimas, name='pasirinkimas'),

    path('zaidejas/<pk>', views.zaidejas, name='zaidejas'),

    path('account/home', views.account_home, name='account_home'),
]
