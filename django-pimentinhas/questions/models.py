from django.db import models

class PendingQuestion(models.Model):
    level = models.IntegerField()
    question = models.TextField()

    def __str__(self):
        return f"[PENDENTE] L{self.level}: {self.question[:30]}"

class OfficialQuestion(models.Model):
    level = models.IntegerField()
    question = models.TextField()

    def __str__(self):
        return f"[OFICIAL] L{self.level}: {self.question[:30]}"
