from django.shortcuts import render, redirect
from .forms import UserForm
from .models import User
from django.contrib import messages, auth
from .utils import detectUser
from django.contrib.auth.decorators import login_required, user_passes_test

from django.core.exceptions import PermissionDenied

# Create your views here.

# Interdiction aux vendors d'accéder aux pages des customers
def check_role_vendor(user):
    if user.role == 1:
        return True
    else:
        raise PermissionDenied

# Interdiction aux customers d'accéder aux pages des vendors
def check_role_custpmer(user):
    if user.role == 2:
        return True
    else:
        raise PermissionDenied

def registerUser(request):
    # Si le user ouvre une autre fenetre pour s'enregistrer alors qu'il est déja connecté, on le redirife vers le dashboard
    if request.user.is_authenticated:
        messages.warning(request, "You are already logged in !")
        return redirect("accounts:myAccount")

    elif request.method == "POST":
        print(request.POST)
        # on recupère les données saisies dans le formulaire
        form = UserForm(request.POST)

        # si les données saisies dans le formulaire sont valides
        if form.is_valid():
            """ Create an user using the form
            # on recupère le password saisi dans le form qu'on va hasher avant de save en BD
            password = form.cleaned_data['password']

            user = form.save(commit=False) # On use ceci quand on veut modifier la valeur de certains champs en back-end avant de save les data en BD.
            user.set_password(password) # hashage du password
            user.role = User.CUSTOMER
            user.save() # on use ceci parce qu'on a modifié certains champs avant de save les data du form en BD sinon on use form.save()
            # form.save(): on use ceci si l'on a aucun champ à modifier avant de save les data du formulaire sinon on user user.save()
            """

            # Create an user using create_user method defined in the UserManager class in models.py
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']

            user = User.objects.create_user(
                first_name=first_name,
                last_name=last_name,
                username=username,
                email=email,
                password=password
            )
            user.role = User.CUSTOMER
            user.save()

            # Message flash à afficher si creation ducompte avec succes. Par defaut les messages sont accessibles dans toutes les pages web
            messages.success(request, "Votre compte a été créé avec succès !!!")
            return redirect('registerUser')
    else:
        form = UserForm()
    context = {'form':form}
    return render(request, "accounts/registerUser.html", context)

def registerVendor(request):
    return render(request, 'accounts/registerVendor.html')

def login(request):
    # Si le user ouvre une autre fenetre pour se logger alors qu'il est déj connecté, on le redirife vers le dashboard
    if request.user.is_authenticated:
        messages.warning(request, "You are already logged in !")
        return redirect("accounts:myAccount")

    # Authentification des users: on recupère l'email et le password saisis dans le formulaire de login
    elif request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        user = auth.authenticate(email=email, password=password)

        # on teste s'il existe un usr avec ces paramètres de connexion
        if user is not None:
            auth.login(request, user)
            messages.success(request, "Welcome ! Your are now logged in")
            return redirect('accounts:myAccount')
        else:
            messages.error(request, "Invalid login credentials !!!")
            return redirect('accounts:login')
    return render(request, 'accounts/login.html')

def logout(request):
    auth.logout(request)
    messages.info(request, "You are logged out !!!")
    return redirect('accounts:login')

@login_required(login_url='login')  # pour accéder à l'url myAccount il faudra etre connecté
def myAccount(request):
    user = request.user # request.user nous renvoie le user conecté
    redirectUrl = detectUser(user)
    return redirect(f'accounts:{redirectUrl}')

@login_required(login_url='login')  # pour accéder à l'url vendorDashboard il faudra etre connecté
@user_passes_test(check_role_vendor)
def vendorDashboard(request):
    return render(request, "accounts/vendorDashboard.html")

@login_required(login_url='login')  # pour accéder à l'url custDashboard il faudra etre connecté
@user_passes_test(check_role_custpmer)
def custDashboard(request):
    return render(request, "accounts/custDashboard.html")

