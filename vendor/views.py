from django.shortcuts import render, redirect
from .forms import VendorForm
from accounts.forms import UserForm
from accounts.models import User, UserProfile
from django.contrib import messages
from accounts.utils import send_verification_email

# Create your views here.
def registerVendor(request):
    # Si le user ouvre une autre fenetre pour s'enregistrer alors qu'il est déja connecté, on le redirife vers le dashboard
    if request.user.is_authenticated:
        messages.warning(request, "You are already logged in !")
        return redirect("accounts:dashboard")

    # Recuperer les data en provenance du formulaire pour les enregistrer en BD
    if request.method == 'POST':
        form = UserForm(request.POST)
        v_form = VendorForm(request.POST, request.FILES) # request.FILES parcequ'il y a un fichier transmis via le formulaire

        # Si le formulaire est valide, on save sinon on renvoie des erreurs
        if form.is_valid() and v_form.is_valid():
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
            user.role = User.VENDOR
            user.save()

            vendor = v_form.save(commit=False) # on use ceci parce qu'on a modifié certains champs avant de save les data du form en BD
            vendor.user = user
            user_profile = UserProfile.objects.get(user=user)
            vendor.user_profile = user_profile
            vendor.save()

            # send verification email
            email_subject = "Please active your account"
            email_template = "accounts/emails/account_verification_email.html "
            send_verification_email(request, user, email_subject, email_template)

            # Message flash à afficher si creation ducompte avec succes. Par defaut les messages sont accessibles dans toutes les pages web
            messages.success(request,
            "Votre compte a été créé avec succès !!! S'il vous plait veuillez attendre la confirmation.")
            return redirect('vendor:registerVendor')
    else:
        # Nous allons afficher les 2 formulaires dans la même page
        form = UserForm()
        v_form = VendorForm

    context = {
        'form': form,
        'v_form': VendorForm
    }
    return render(request, 'accounts/registerVendor.html', context)
