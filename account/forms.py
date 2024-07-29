from typing import Any

from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.forms.widgets import PasswordInput, TextInput

User = get_user_model()


class UserCreateForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
        widgets = {
            'username': TextInput(attrs={'class': 'form-control'}),
            'email': TextInput(attrs={'class': 'form-control'}),
            'password1': PasswordInput(attrs={'class': 'form-control'}),
            'password2': PasswordInput(attrs={'class': 'form-control'}),
        }

        def __init__(self, *args, **kwargs):
            super(UserCreateForm, self).__init__(*args, **kwargs)

            self.fields['email'].label = 'Your Email Address'
            self.fields['email'].required = True
            self.fields['username'].help_text = ''
            self.fields['password1'].help_text = ''

        def clean_email(self):
            email = self.cleaned_data.get['email'].lower()
            if User.objects.filter(email=email).exists():
                raise forms.ValidationError('This email address is already registered.')
            return email


class LoginForm(AuthenticationForm):
    username = forms.CharField(widget=TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(widget=PasswordInput(attrs={'class': 'form-control'}))


class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField(required=True)

    def __init__(self, *args, **kwargs):
        super(UserUpdateForm, self).__init__(*args, **kwargs)

        self.fields['email'].label = 'Your Email Address'
        self.fields['email'].required = True

    class Meta:
        model = User
        fields = ['username', 'email']
