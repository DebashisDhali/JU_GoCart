from django import forms
from gocart.models import GoCart

class GoCartForm(forms.ModelForm):
    class Meta:
        model = GoCart
        fields = ['number_plate', 'driver', 'route', 'capacity']
