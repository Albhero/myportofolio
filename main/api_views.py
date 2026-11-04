from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import BasePermission, SAFE_METHODS, IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from main.models import Skill
from main.serializers import SkillSerializer

class IsPortfolioOwnerOrEditorOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        if request.user.is_superuser:
            return True
        if request.user.groups.filter(name='Editor').exists() and request.method in ['PUT', 'PATCH']:
            return True
        return False

@api_view(['GET', 'POST'])
@permission_classes([IsPortfolioOwnerOrEditorOrReadOnly])
def skill_list_create_api(request):
    if request.method == 'GET':
        name_query = request.GET.get('name', '').strip()
        skills = Skill.objects.all()
        if name_query:
            skills = skills.filter(name__icontains=name_query)
        serializer = SkillSerializer(skills, many=True, context={'request': request})
        return Response(serializer.data)
    
    elif request.method == 'POST':
        serializer = SkillSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'PATCH', 'DELETE'])
@permission_classes([IsPortfolioOwnerOrEditorOrReadOnly])
def skill_detail_api(request, pk):
    skill = get_object_or_404(Skill, pk=pk)
    
    if request.method == 'GET':
        serializer = SkillSerializer(skill, context={'request': request})
        return Response(serializer.data)
    
    elif request.method in ['PUT', 'PATCH']:
        partial = request.method == 'PATCH'
        serializer = SkillSerializer(skill, data=request.data, partial=partial, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    elif request.method == 'DELETE':
        if not request.user.is_superuser:
            return Response({"detail": "Only the portfolio owner can delete skills."}, status=status.HTTP_403_FORBIDDEN)
        skill.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def skill_star_api(request, pk):
    skill = get_object_or_404(Skill, pk=pk)
    user = request.user
    if user in skill.starred_by.all():
        skill.starred_by.remove(user)
        starred = False
    else:
        skill.starred_by.add(user)
        starred = True
    return Response({"is_starred": starred, "star_count": skill.starred_by.count()}, status=status.HTTP_200_OK)
