from django.shortcuts import redirect, render
from django.contrib.auth import login, authenticate, logout
from . import forms
from .forms import RegisterForm
from django.contrib.auth.decorators import login_required

'''
Disconnection of the user.

Parameters:
    request: 

Returns:
    Redirect the user to the login page.

'''
def logout_user(request):
    logout(request)
    return redirect('login')

'''
Connection of the user.

Parameters:
    request: objet contenant toutes les informations de la requête.

Returns:
    tupple contenant : toutes les informations de la requête, le template de la page html,un dictionnaire de la liste des
     dictionnaires des informations du formulaire pour créer un nouvel utilisateur et du message d'erreur.

'''
def login_page(request):
    form = forms.LoginForm()
    message = ''
    if request.method == 'POST':
        form = forms.LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password'],
            )
            if user is not None:
                login(request, user)
                return redirect('home')
        message = 'Identifiants invalides.'
    return render(request, 'authentication/login.html', context={'form': form, 'message': message})

'''
Registration of the user.

Parameters:
    request: objet contenant toutes les informations de la requête.

Returns:
    tupple contenant : toutes les informations de la requête, le template de la page html,un dictionnaire de la liste des
     dictionnaires des informations du formulaire pour connecter un utilisateur existant.

'''
def sign_up(request):
    form = RegisterForm()
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request, user)
            return redirect('home')
    return render(request,
                  'authentication/register.html',
                  context={'form': form})





