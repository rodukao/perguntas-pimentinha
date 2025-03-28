from django.shortcuts import render
import json
import random
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.db.models import F
from .models import PendingQuestion, OfficialQuestion, GlobalStats

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
        level_str = request.GET.get('level') # Renomeado para evitar conflito com a variável 'level'
        if not level_str:
            return JsonResponse({"error": "Param 'level' é obrigatório"}, status=400)

        try:
            level = int(level_str) # Tenta converter para inteiro
        except ValueError:
            return JsonResponse({"error": "Param 'level' deve ser um número inteiro."}, status=400)

        qs = OfficialQuestion.objects.filter(level=level)
        if not qs.exists():
            # Considerar retornar uma pergunta genérica ou de nível 1? Ou manter o erro 404.
            return JsonResponse({"error": f"Nenhuma pergunta oficial encontrada para o nível {level}."}, status=404)

        try:
            chosen = random.choice(list(qs)) # Converte para lista para usar random.choice

            # --- INCREMENTAR CONTADOR GLOBAL ---
            try:
                stats = GlobalStats.get_instance()
                stats.increment_questions_served()
                # Não precisamos do valor atualizado aqui, apenas incrementar.
            except Exception as e:
                # É importante logar o erro, mas não impedir a pergunta de ser enviada.
                # Em produção, use o sistema de logging do Django.
                print(f"ALERTA: Falha ao incrementar o contador global de perguntas: {e}")
            # ------------------------------------

            return JsonResponse({"question": chosen.question})

        except IndexError:
             # Isso pode acontecer se a queryset estiver vazia após o filtro,
             # embora o .exists() acima deva prevenir isso. Mas por segurança:
             return JsonResponse({"error": f"Erro inesperado ao selecionar pergunta para o nível {level}."}, status=500)

    else:
        # Retornar 405 Method Not Allowed é mais apropriado
        return JsonResponse({"error": "Método não permitido. Use GET."}, status=405)
    
def get_global_stats(request):
    """Retorna as estatísticas globais (atualmente, apenas o contador de perguntas)."""
    if request.method == 'GET':
        try:
            stats = GlobalStats.get_instance()
            data = {
                'total_questions_served': stats.total_questions_served
                # Poderia adicionar outras estatísticas aqui no futuro
            }
            return JsonResponse(data)
        except Exception as e:
            print(f"Erro ao buscar estatísticas globais: {e}")
            return JsonResponse({"error": "Não foi possível buscar as estatísticas."}, status=500)
    else:
        return JsonResponse({"error": "Método não permitido. Use GET."}, status=405)
