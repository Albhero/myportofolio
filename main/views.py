from django.shortcuts import render

from main.models import Experience

from main.models import Skills

def show_main(request):
    context = {
        "name": "Albhero",
        "npm": "2506555224",
        "study_program": "S1 Ilmu Komputer KKI",
        "bio": (
            "CS student at Universitas Indonesia enrolled in an international "
            "program. Planning to move to University of Queensland in the "
            "future. Professional random guy."
        ),
        "experience": (
            "A list of all experiences and roles that have previously been taken. Each roles "
            "are authentic and are a marking stone for the future. Extra informations such as "
            "dates, status, and categories have also been added."
        ),
        "skills": (
            "A list of all skills that have been earned through everyday life. Each skills "
            "are authentic and are categorized based on proficiency, which ranges from beginner, "
            "intermediate, advanced, and expert."
        )
    }
    return render(request, "index.html", context)


def show_experience(request):
    context = {
        "name": "Albhero",
        "experience_list": Experience.objects.all(),
    }
    return render(request, "experience.html", context)

def show_skills(request):
    context = {
        "name": "Albhero",
        "skills_list": Skills.objects.all(),
    }
    return render(request, "skills.html", context)