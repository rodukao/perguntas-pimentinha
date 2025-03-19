from django.contrib import admin
from .models import PendingQuestion, OfficialQuestion

@admin.register(PendingQuestion)
class PendingQuestionAdmin(admin.ModelAdmin):
    list_display = ('id', 'level', 'question')

@admin.register(OfficialQuestion)
class OfficialQuestionAdmin(admin.ModelAdmin):
    list_display = ('id', 'level', 'question')
