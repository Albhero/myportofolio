from django.forms import ModelForm, TextInput, Textarea
from main.models import Skills, Experience

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
        
class ExperienceForm(ModelForm):
    class Meta:
        model = Experience
        fields = [
            "title",
            "description",
            "category",
        ]

        labels = {
            "title": "Experience Title",
            "description": "Experience Description",
            "category": "Type",
            "started_at": "Start Year",
            "ended_at": "End Year",
        }

        widgets = {
            "title": TextInput(
                attrs={
                    "placeholder": "Experience title",
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
            "started_at": TextInput(
                attrs={
                    "placeholder": "2006",
                }
            ),
            "ended_at": TextInput(
                attrs={
                    "placeholder": "2026",
                }
            ),
        }