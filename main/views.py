from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.http import require_POST
from main.models import Skill
from main.forms import SkillForm

def get_skills_json(request):
    title_query = request.GET.get("name", "").strip()
    skills = Skill.objects.prefetch_related('starred_by').all()
    if title_query:
        skills = skills.filter(name__icontains=title_query)

    data = []
    for skill in skills:
        starred_users = skill.starred_by.all()
        is_starred = request.user in starred_users if request.user.is_authenticated else False
        starred_by_names = ", ".join([u.username for u in starred_users])

        data.append({
            "pk": str(skill.id),
            "fields": {
                "name": skill.name,
                "proficiency": skill.proficiency,
                "description": skill.description,
                "category": skill.category,
                "credential_url": skill.credential_url,
                "star_count": starred_users.count(),
                "is_starred": is_starred,
                "starred_by_names": starred_by_names,
            }
        })
    return JsonResponse(data, safe=False)

def show_skills(request):
    title_query = request.GET.get("name", "").strip()
    context = {
        "name": "Portfolio Owner",
        "title_query": title_query,
        "form": SkillForm(),
    }
    return render(request, "skills.html", context)

@require_POST
def create_skill_ajax(request):
    if not request.user.is_superuser:
        return JsonResponse({"message": "Only the portfolio owner can add skills."}, status=403)

    form = SkillForm(request.POST)
    if form.is_valid():
        skill = form.save()
        return JsonResponse({"message": "Skill added successfully.", "pk": str(skill.id)}, status=201)
    return JsonResponse({"errors": form.errors.get_json_data()}, status=400)
