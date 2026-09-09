from django.shortcuts import render

from main.models import Experience


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
    }
    return render(request, "index.html", context)


def show_experience(request):
    context = {
        "name": "Albhero",
        "experience_list": Experience.objects.all(),
    }
    return render(request, "experience.html", context)