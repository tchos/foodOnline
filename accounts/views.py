from django.shortcuts import render, redirect
from .forms import UserForm
from .models import User
from django.contrib import messages

# Create your views here.
def registerUser(request):
    if request.method == "POST":
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
