import uuid
from django.db import models
from django.contrib.auth.models import User

class Skill(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    proficiency = models.IntegerField(default=1) # 1 to 100 or 1 to 5 scale
    description = models.TextField()
    category = models.CharField(max_length=100, default='General')
    credential_url = models.URLField(blank=True, null=True)
    starred_by = models.ManyToManyField(User, related_name='starred_skills', blank=True)

    def __str__(self):
        return self.name
