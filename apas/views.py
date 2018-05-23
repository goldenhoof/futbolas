from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.views.generic import TemplateView
from django.contrib.auth import authenticate, login
from .forms import UserForm
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .models import Rungtynes, Zaidejas, Stavke
from django.utils import timezone


def update_rungtynes(rungtynes):
    for rungtyne in rungtynes:
        if rungtyne.prasidejo == False:
            if rungtyne.data < timezone.now():
                rungtyne.prasidejo = True
                rungtyne.save()

def update_taskai(zaidejas):
    laimetos = Stavke.objects.filter(zaidejas=zaidejas, laimeta=True)
    zaidejas.taskai = sum([stavke.laimejimas for stavke in laimetos])
    zaidejas.save()

def update_stavke(stavkes):
    for stavke in stavkes:
        baigtis = stavke.rungtynes.baigtis
        if baigtis == stavke.pasirinkimas:
            stavke.laimeta = True
            if baigtis == '1':
                stavke.laimejimas = stavke.rungtynes.kofas1
            elif baigtis == '2':
                stavke.laimejimas = stavke.rungtynes.kofas2
            else:
                stavke.laimejimas = stavke.rungtynes.kofasx
            stavke.save()

def index(request):
    stavkes = Stavke.objects.filter(laimeta=False)
    update_stavke(stavkes)
    zaidejai = Zaidejas.objects.order_by('taskai').reverse()
    for zaidejas in zaidejai:
        update_taskai(zaidejas)
    return render(request, 'apas/index.html', {'zaidejai': zaidejai})

def tvarkarastis(request):
    rungtynes = Rungtynes.objects.order_by('data')
    update_rungtynes(rungtynes)
    return render(request, 'apas/tvarkarastis.html', {'rungtynes': rungtynes})

def sign_up(request):
    user_form = UserForm()
    if request.method == 'POST':
        user_form = UserForm(request.POST)
        if user_form.is_valid():
            username = user_form.cleaned_data.get('username')
            raw_password = user_form.cleaned_data.get('password')
            email = user_form.cleaned_data.get('email')
            new_user = User.objects.create_user(username=username, password=raw_password, email=email)
            new_user.save()
            login(request, authenticate(
                username = username,
                password = raw_password
            ))
            return HttpResponseRedirect('/')
    return render(request, 'apas/sign_up.html', {'form': user_form})

def zaidejas(request, pk):
    zaidejas_id = User.objects.get(username=pk).id
    zaidejas = Zaidejas.objects.get(user_id=zaidejas_id)
    stavkes = Stavke.objects.filter(zaidejas_id=zaidejas_id).order_by('rungtynes_id')
    return render(request, 'apas/zaidejas.html', {'zaidejas': zaidejas, 'stavkes': stavkes})

@login_required(login_url='../sign_in/')
def account_home(request):
    sarasas = []
    rungtynes = Rungtynes.objects.order_by('data')
    update_rungtynes(rungtynes)
    zaidejas = Zaidejas.objects.get(user_id=request.user.id)
    stavkes = Stavke.objects.filter(zaidejas=zaidejas, laimeta=False)
    update_stavke(stavkes)
    for i in rungtynes:
        try:
            sarasas.append((i, Stavke.objects.get(zaidejas=zaidejas, rungtynes=i)))
        except:
            sarasas.append((i, Stavke()))

    return render(request, 'account/home.html', {'sarasas': sarasas})

@login_required(login_url='../sign_in/')
def pasirinkimas(request, id, pasirinkimas):
    rungtyne = Rungtynes.objects.get(pk=id)
    zaidejas = Zaidejas.objects.get(user_id=request.user.id)
    if rungtyne.data > timezone.now():
        try:
            stavke = Stavke.objects.get(zaidejas=zaidejas, rungtynes=rungtyne)
        except Stavke.DoesNotExist:
            stavke = Stavke()
            stavke.zaidejas = zaidejas
            stavke.rungtynes = rungtyne
        stavke.pasirinkimas = pasirinkimas
        stavke.save()

    return redirect('account_home')
