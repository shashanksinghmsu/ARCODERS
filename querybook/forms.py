from django import forms
from django.apps import apps
from .models import query_form, solution_form

class add_query(forms.ModelForm):
    class Meta:
        model = query_form
        fields = ['query', 'description']
        


class add_solution(forms.ModelForm):
    class Meta:
        model = solution_form
        fields = ['solution']
