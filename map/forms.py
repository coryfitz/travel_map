from django import forms

from .models import CountryInput

class CountriesForm(forms.ModelForm):
    class Meta:
        model = CountryInput
        fields = ['countries']
        labels = {'countries': ''}