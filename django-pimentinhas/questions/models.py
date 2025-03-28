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

class GlobalStats(models.Model):
    """Armazena estatísticas globais, como o total de perguntas servidas."""
    # Usamos um ID fixo para garantir que haja apenas uma linha nesta tabela (Singleton)
    singleton_instance_id = models.PositiveIntegerField(default=1, unique=True, editable=False, primary_key=True)
    total_questions_served = models.PositiveIntegerField(default=0, help_text="Contador total de perguntas oficiais servidas pela API.")

    class Meta:
        verbose_name = "Estatística Global"
        verbose_name_plural = "Estatísticas Globais"

    def __str__(self):
        return f"Total de Perguntas Servidas: {self.total_questions_served}"

    @classmethod
    def get_instance(cls):
        """Obtém ou cria a única instância de GlobalStats."""
        instance, created = cls.objects.get_or_create(singleton_instance_id=1)
        return instance

    def increment_questions_served(self):
        """Incrementa o contador de forma atômica."""
        # Usar F() previne race conditions em ambientes concorrentes
        self.total_questions_served = models.F('total_questions_served') + 1
        self.save(update_fields=['total_questions_served'])
        # Opcional: recarregar do DB se precisar do valor atualizado imediatamente
        # self.refresh_from_db()