from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm


class UserAuthenticationForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={
        "class": "form-control",
        "placeholder": "Введите ваш username"
    }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        "class": "form-control",
        "placeholder": "Введите ваш пароль"
    }))

    class Meta:
        model = User


class UserRegistrationForm(UserCreationForm):
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={
        "class": "form-control",
        "placeholder": "Введите ваш пароль"
    }))

    password2 = forms.CharField(widget=forms.PasswordInput(attrs={
        "class": "form-control",
        "placeholder": "Введите ваш пароль"
    }))
    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]
        widgets = {
            "username": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Введите ваш username"
            }),
            "email": forms.EmailInput(attrs={
                "class": "form-control",
                "placeholder": "Введите ваш email"
            })
            # "password1": forms.PasswordInput(attrs={
            #     "class": "form-control",
            #     "placeholder": "Введите ваш пароль"
            # }),
            # "password2": forms.PasswordInput(attrs={
            #     "class": "form-control",
            #     "placeholder": "Подтвердите ваш пароль"
            # })
        }

