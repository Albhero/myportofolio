from django.urls import path
from main.api_views import skill_list_create_api, skill_detail_api, skill_star_api

app_name = 'main_api'

urlpatterns = [
    path('v1/skills/', skill_list_create_api, name='skill-list-create'),
    path('v1/skills/<uuid:pk>/', skill_detail_api, name='skill-detail'),
    path('v1/skills/<uuid:pk>/star/', skill_star_api, name='skill-star'),
]
