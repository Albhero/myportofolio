from django.shortcuts import render

from main.models import Experience
from main.models import Skills

from django.contrib import messages
from django.core import serializers
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render

from main.forms import SkillsForm
from main.models import Experience, Skills

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
    json_response = get_skills_json(request)

    skills = serializers.deserialize(
        "json",
        json_response.content.decode("utf-8"),
    )
    skills = [skill.object for skill in skills]
    title_query = request.GET.get("title", "").strip()
    
    context = {
        "name": "Albhero",
        "skills_list": Skills.objects.all(),
    }
    return render(request, "skills.html", context)

def create_skills(request):
    form = SkillsForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Skills have been added successfully!")
        return redirect("main:show_skills")

    context = {
        "name": "Khalifah Gigan Albhero",
        "form": form,
    }
    return render(request, "skills_form.html", context)

def get_skills_json(request):
    title_query = request.GET.get("title", "").strip()
    skills = Skills.objects.all()

    if title_query:
        skills = skills.filter(title__icontains=title_query)

    skills_json = serializers.serialize("json", skills)
    return HttpResponse(skills_json, content_type="application/json")

def delete_skills(request, skills_id):
    skill = get_object_or_404(Skills, pk=skills_id)

    if request.method == "POST":
        skill.delete()
        messages.success(request, "Skill has been successfully deleted!")
        return redirect("main:show_skills")

    return redirect("main:show_skills")