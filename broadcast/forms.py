from django import forms
from .models import Broadcast


class BroadcastForm(forms.ModelForm):
    class Meta:
        model = Broadcast
        fields = ['title', 'categories', 'url']

        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'categories': forms.Select(attrs={'class': 'form-control'}),
            'url': forms.Textarea(attrs={'class': 'form-control'})
        }

