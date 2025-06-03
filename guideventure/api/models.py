from django.contrib.auth.models import User
from django.db import models


class Adventure(models.Model):
    """
    Represents an adventure in the Guideventure application.
    """
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    owner = models.ForeignKey(User, related_name='adventures', on_delete=models.CASCADE)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.title} - {self.owner.username}"


class Step(models.Model):
    """
    Represents a step in an adventure.
    """
    adventure = models.ForeignKey(Adventure, related_name='steps', on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    order = models.PositiveIntegerField()
    longitude = models.FloatField()
    latitude = models.FloatField()

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"{self.adventure.title} - {self.title}"


class QuizStep(Step):
    """
    Represents a quiz step in an adventure.
    """

    def __str__(self):
        return f"{self.adventure.title} - Quiz: {self.title}"


class Question(models.Model):
    """
    Represents a question in a quiz step.
    """
    quiz_step = models.ForeignKey(QuizStep, related_name='questions', on_delete=models.CASCADE)
    text = models.CharField(max_length=255)
    correct_answer = models.CharField(max_length=255)
    wrong_answers = models.JSONField(default=list, blank=True)

    def __str__(self):
        return f"{self.quiz_step.title} - Question: {self.text}"
