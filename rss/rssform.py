from django import forms

from rss.models import FeedRss

class RssForm(forms.ModelForm):
    
    class Meta:
        model = FeedRss
        
        fields = [
            'titulo',
            'enlace',
            'descripcion'
        ]
        labels = {       # definicion de diccionario
            'titulo': 'title',
            'enlace': 'link',
            'descripcion': 'description',
        }
        widgets = {
            'titulo': forms.TextInput(attrs={'class':'form-control'}),
            'enlace': forms.TextInput(attrs={'class':'form-control'}),
            'descripcion': forms.TextInput(attrs={'class':'form-control'})
        }