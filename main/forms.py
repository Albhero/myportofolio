from django.forms import ModelForm, TextInput, Textarea
from main.models import Skills

class SkillsForm(ModelForm):
    class Meta:
        model = Skills
        fields = [
            "title",
            "description",
            "category",
        ]

        labels = {
            "title": "Skill Name",
            "description": "Skill Description",
            "category": "Skill Level",
        }

        widgets = {
            "title": TextInput(
                attrs={
                    "placeholder": "Skill Name",
                    "maxlength": 255,
                }
            ),
            "description": Textarea(
                attrs={
                    "placeholder": "Describe this skill and its uses...",
                    "rows": 3,
                }
            ),
            "category": TextInput(
                attrs={
                    "placeholder": "Beginner",
                }
            ),
        }