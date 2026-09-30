from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.core import serializers
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render

from main.forms import SkillsForm, ExperienceForm
from main.models import Experience, Skills

import datetime
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied

def show_main(request):
    last_login = request.COOKIES.get('last_login', 'No active login session / Cookie not found')
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
        ),
        "last_login": last_login,
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
        "title_query": title_query,
    }
    return render(request, "skills.html", context)

@login_required(login_url="/login/")
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

@login_required(login_url="/login/")
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

@login_required(login_url="/login/")
def delete_experience(request, experience_id):
    experience = get_object_or_404(Experience, pk=experience_id)

    if request.method == "POST":
        experience.delete()
        messages.success(request, "Experience has been successfully deleted!")
        return redirect("main:show_experience")

    return redirect("main:show_experience")

@login_required(login_url="/login/")
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

    skills_json = serializers.serialize("json", skills, use_natural_foreign_keys=True)
    return HttpResponse(skills_json, content_type="application/json")

@login_required(login_url="/login/")
def delete_skills(request, skills_id):
    skill = get_object_or_404(Skills, pk=skills_id)

    if request.method == "POST":
        skill.delete()
        messages.success(request, "Skill has been successfully deleted!")
        return redirect("main:show_skills")

    return redirect("main:show_skills")

@login_required(login_url="/login/")
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

def register(request):
    form = UserCreationForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Account created successfully. Please log in.")
        return redirect("main:login")

    context = {
        "name": "Albhero",
        "form": form,
    }
    return render(request, "register.html", context)

def login_user(request):
    form = AuthenticationForm(request, data=request.POST or None)

    if request.method == "POST" and form.is_valid():
        user = form.get_user()
        login(request, user)
        response = redirect("main:show_main")
        response.set_cookie('last_login', datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        return response

    context = {
        "name": "Albhero",
        "form": form,
    }
    return render(request, "login.html", context)

def logout_user(request):
    logout(request)
    response = redirect("main:show_main")
    response.delete_cookie('last_login')
    return response

@login_required(login_url="/login/")
def toggle_star(request, skills_id):
    skill = get_object_or_404(Skills, pk=skills_id)

    if request.method == "POST":
        if request.user in skill.starred_by.all():
            skill.starred_by.remove(request.user)
        else:
            skill.starred_by.add(request.user)

    return redirect("main:show_skills")