from django import forms
from django.apps import apps
from .models import form

class add_program_code(forms.ModelForm):
    class Meta:
        model = form
        fields = ['title', 'code']
       