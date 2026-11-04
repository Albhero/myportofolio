from django import forms
from main.models import Skill

class SkillForm(forms.ModelForm):
    class Meta:
        model = Skill
        fields = ['name', 'proficiency', 'description', 'category', 'credential_url']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'w-full px-3 py-2 border rounded-lg', 'placeholder': 'Skill Name'}),
            'proficiency': forms.NumberInput(attrs={'class': 'w-full px-3 py-2 border rounded-lg', 'min': 1, 'max': 100}),
            'description': forms.Textarea(attrs={'class': 'w-full px-3 py-2 border rounded-lg', 'rows': 3}),
            'category': forms.TextInput(attrs={'class': 'w-full px-3 py-2 border rounded-lg', 'placeholder': 'e.g., Backend, Frontend, DevOps'}),
            'credential_url': forms.URLInput(attrs={'class': 'w-full px-3 py-2 border rounded-lg', 'placeholder': 'https://...'}),
        }
