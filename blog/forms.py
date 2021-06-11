from .models import Document
from django import forms

class DocumentForm(forms.ModelForm):
    class Meta:
        model = Document
        fields = ('document', 'name')