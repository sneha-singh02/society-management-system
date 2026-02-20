from django import forms

class LoginForm(forms.Form):
    username_or_email = forms.CharField(label='Email or Username')
    password = forms.CharField(widget=forms.PasswordInput)
