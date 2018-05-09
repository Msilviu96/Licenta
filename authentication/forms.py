from django import forms
from database import models


class LoginForm(forms.ModelForm):
    class Meta:
        model = models.Parent
        fields = ['username', 'password']