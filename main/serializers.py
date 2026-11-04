from rest_framework import serializers
from django.utils.html import strip_tags
from main.models import Skill

class SkillSerializer(serializers.ModelSerializer):
    star_count = serializers.SerializerMethodField()
    is_starred = serializers.SerializerMethodField()
    starred_by_names = serializers.SerializerMethodField()

    class Meta:
        model = Skill
        fields = [
            'id', 'name', 'proficiency', 'description', 
            'category', 'credential_url', 'star_count', 
            'is_starred', 'starred_by_names'
        ]
        read_only_fields = ['id', 'star_count', 'is_starred', 'starred_by_names']

    def get_star_count(self, obj):
        return obj.starred_by.count()

    def get_is_starred(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return request.user in obj.starred_by.all()
        return False

    def get_starred_by_names(self, obj):
        return ", ".join([u.username for u in obj.starred_by.all()])

    def validate_name(self, value):
        clean_value = strip_tags(value).strip()
        if not clean_value:
            raise serializers.ValidationError("Skill name cannot be empty or consist only of HTML tags.")
        return clean_value
