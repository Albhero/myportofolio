from django.shortcuts import render

from main.models import Experience
from main.models import Skills

from django.contrib import messages
from django.core import serializers
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render

from main.forms import SkillsForm, ExperienceForm
from main.models import Experience, Skills

def show_main(request):
    context = {
        "name": "Albhero",
        "cap_name": "ALBHERO",
        "full_name":"Khalifah Gigan Albhero",
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
        "full_name":"Khalifah Gigan Albhero",
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
        "full_name":"Khalifah Gigan Albhero",
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
        "full_name":"Khalifah Gigan Albhero",
        "form": form,
    }
    return render(request, "skills_form.html", context)

def create_experience(request):
    form = ExperienceForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Experience have been added successfully!")
        return redirect("main:show_experience")

    context = {
        "name": "Khalifah Gigan Albhero",
        "full_name":"Khalifah Gigan Albhero",
        "form": form,
    }
    return render(request, "experience_form.html", context)

def delete_experience(request, experience_id):
    experience = get_object_or_404(Experience, pk=experience_id)

    if request.method == "POST":
        experience.delete()
        messages.success(request, "Experience has been successfully deleted!")
        return redirect("main:show_experience")

    return redirect("main:show_experience")

def edit_experience(request, experience_id):
    experience = get_object_or_404(Experience, pk=experience_id)
    form = ExperienceForm(request.POST or None, instance=experience)

    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Experience updated successfully!")
        return redirect("main:show_experience")

    context = {
        "name": "Khalifah Gigan Albhero",
        "full_name": "Khalifah Gigan Albhero",
        "form": form,
        "experience": experience,
    }
    return render(request, "edit_experience.html", context)

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

def edit_skill(request, skill_id):
    skill = get_object_or_404(Skills, id=skill_id)
    if request.method == "POST":
        skill.title = request.POST.get("title")
        skill.description = request.POST.get("description")
        skill.category = request.POST.get("category")
        skill.save()
        messages.success(request, "Skill updated successfully!")
        return redirect("main:show_skills")
    
    return render(request, "edit_skill.html", {"skill": skill})