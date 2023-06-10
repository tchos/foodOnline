from django import forms
from .models import User

# classe formulaire pour la creation des users
class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    confirm_password = forms.CharField(widget=forms.PasswordInput())
    email = forms.EmailField(widget=forms.EmailInput(), required=True)
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'phone_number', 'password', 'confirm_password']


    def clean(self):
        cleaned_data = super(UserForm, self).clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')
        email = cleaned_data.get('email')

        if password != confirm_password:
            raise forms.ValidationError("Password does not match !!!")

        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Erreur: Cet email existe déjà. Veuillez utiliser une adresse email !!!")