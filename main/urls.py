from django.urls import path
from main.views import show_skills, get_skills_json, create_skill_ajax

app_name = 'main'

urlpatterns = [
    path('skills/', show_skills, name='show_skills'),
    path('api/skills/', get_skills_json, name='get_skills_json'),
    path('skills/add-ajax/', create_skill_ajax, name='create_skill_ajax'),
]
