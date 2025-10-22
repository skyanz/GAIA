from django.db import models

class Turma(models.Model):
    nome = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.nome

class Categoria(models.Model):
    nome = models.CharField(max_length=100, unique=True)
   
    class Meta:
        verbose_name_plural = "Categorias" # Para o admin

    def __str__(self):
        return self.nome

# gerador_app/models.py
from django.db import models
from django.contrib.auth.models import User
from geral_app.models import Categoria, Turma # Importe os models que acabamos de criar

class Questao(models.Model):
    DIFICULDADE_CHOICES = [
        ('F', 'Fácil'),
        ('M', 'Média'),
        ('D', 'Difícil'),
    ]
   
    categoria = models.ForeignKey(Categoria, on_delete=models.PROTECT, related_name='questoes')
    dificuldade = models.CharField(max_length=1, choices=DIFICULDADE_CHOICES)
    enunciado = models.TextField()
   
    # JSONField é perfeito para seu HTML dinâmico
    # Ex: {"A": "Texto da A", "B": "Texto da B", ...}
    alternativas = models.JSONField(default=dict)
   
    resposta_correta = models.CharField(max_length=5) # "A", "B", "C" ou "D" etc.
   
    criado_por = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.enunciado[:50] + '...'

class Avaliacao(models.Model):
    titulo = models.CharField(max_length=200, verbose_name="Título")
    turma = models.ForeignKey(Turma, on_delete=models.CASCADE, related_name='avaliacoes')
    questoes = models.ManyToManyField(Questao, related_name='avaliacoes')
    professor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='avaliacoes_criadas')

    def __str__(self):
        return f"{self.titulo} - {self.turma.nome}"

class RespostaAluno(models.Model):
    avaliacao = models.ForeignKey(Avaliacao, on_delete=models.CASCADE, related_name='respostas')
    questao = models.ForeignKey(Questao, on_delete=models.CASCADE)
   
    # Campo chave para seu dashboard
    # Sugestão: adicione um campo "Nome" no seu quiz HTML
    aluno_id_externo = models.CharField(max_length=255, db_index=True)
   
    resposta_aluno = models.CharField(max_length=5) # A resposta que o aluno marcou
    esta_correta = models.BooleanField()

    def save(self, *args, **kwargs):
        # Lógica automática que facilita o dashboard
        self.esta_correta = (self.resposta_aluno == self.questao.resposta_correta)
        super().save(*args, **kwargs)

    def __str__(self):
        return f'Resposta de {self.aluno_id_externo} para {self.questao_id}'
   
    class Meta:
        unique_together = ('avaliacao', 'questao', 'aluno_id_externo')
