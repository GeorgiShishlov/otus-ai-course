from django.db import models


class SurveyAnswer(models.Model):
    answers = models.JSONField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
