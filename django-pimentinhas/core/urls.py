from django.contrib import admin
from django.urls import path
from questions.views import add_question, approve_question, get_question

urlpatterns = [
    path('admin/', admin.site.urls),

    path('api/add_question', add_question, name='add_question'),
    path('api/approve_question/<int:question_id>', approve_question, name='approve_question'),
    path('api/perguntas', get_question, name='get_question'),
]
