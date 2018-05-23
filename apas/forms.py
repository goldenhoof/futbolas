from django import forms
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.contrib.auth.forms import AuthenticationForm


class UserForm(forms.ModelForm):
    username = forms.CharField(label='Vardas', max_length=100)
    email = forms.EmailField(label='El. paštas', max_length=100, required=False)
    password = forms.CharField(label='Slaptažodis', widget=forms.PasswordInput())
    confirm_password = forms.CharField(label='Pakartoti slaptažodį', widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('username', 'email', 'password')

    def clean(self):
        cleaned_data = super(UserForm, self).clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password != confirm_password:
            raise forms.ValidationError("Slaptažodžiai nesutampa")


class LoginForm(AuthenticationForm):
    username = forms.CharField(label='Vardas', max_length=100)
    password = forms.CharField(label='Slaptažodis', widget=forms.PasswordInput())
