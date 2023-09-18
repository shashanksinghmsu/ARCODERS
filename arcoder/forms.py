from django import forms
from django.apps import apps
from .models import user_detail

class privacy_form(forms.ModelForm):
    class Meta:
        model = user_detail
        fields = ['privacy']


