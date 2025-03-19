from django.shortcuts import render
import json
import random
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import PendingQuestion, OfficialQuestion

@csrf_exempt
def add_question(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        level = data.get('level')
        question = data.get('question')

        if not level or not question:
            return JsonResponse({"error": "Level and question are required"}, status=400)

        PendingQuestion.objects.create(level=level, question=question)
        return JsonResponse({"message": "Pergunta adicionada com sucesso!"})
    else:
        return JsonResponse({"error": "Method not allowed"}, status=405)


@csrf_exempt
def approve_question(request, question_id):
    if request.method == 'POST':
        try:
            pend_q = PendingQuestion.objects.get(id=question_id)
        except PendingQuestion.DoesNotExist:
            return JsonResponse({"error": "Pergunta não encontrada"}, status=404)

        # Criar na Official
        OfficialQuestion.objects.create(level=pend_q.level, question=pend_q.question)
        # Deletar do Pending
        pend_q.delete()

        return JsonResponse({"message": "Pergunta aprovada e movida para oficial!"})
    else:
        return JsonResponse({"error": "Method not allowed"}, status=405)


def get_question(request):
    if request.method == 'GET':
        level = request.GET.get('level')
        if not level:
            return JsonResponse({"error": "Param 'level' é obrigatório"}, status=400)

        qs = OfficialQuestion.objects.filter(level=level)
        if not qs.exists():
            return JsonResponse({"error": "Nenhuma pergunta encontrada"}, status=404)

        chosen = random.choice(qs)
        return JsonResponse({"question": chosen.question})
    else:
        return JsonResponse({"error": "Method not allowed"}, status=405)


# Create your views here.
