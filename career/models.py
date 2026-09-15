from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    education = models.CharField(max_length=255, blank=True)
    career_goal = models.CharField(max_length=255, blank=True)
    skills = models.TextField(blank=True)
    cv = models.FileField(upload_to="cvs/", blank=True, null=True)

    def __str__(self):
        return self.user.username


class CareerAnalysis(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    recommended_career = models.CharField(max_length=255, blank=True)
    strengths = models.TextField(blank=True)
    missing_skills = models.TextField(blank=True)
    analysis = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.recommended_career}"


class Roadmap(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    completed = models.BooleanField(default=False)

    def __str__(self):
        return self.title