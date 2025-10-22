# geral_app/models.py
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