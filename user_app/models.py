# user_app/models.py
from django.db import models
from django.contrib.auth.models import User
from geral_app.models import Turma # Importe o model Turma

class Professor(models.Model):
    # Ligação 1-para-1 com o sistema de autenticação do Django
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
   
    # Seus campos de negócio
    # Note que agora é ManyToManyField, muito mais flexível
    turmas = models.ManyToManyField(Turma, related_name='professores', blank=True)
    materia = models.CharField(max_length=100, default="Matemática")
    telefone = models.CharField(max_length=15, blank=True, null=True)
    data_criacao = models.DateTimeField(auto_now_add=True)
   
    def __str__(self):
        # Busca o nome do User associado
        return self.user.get_full_name() or self.user.username
