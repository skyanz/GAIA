# user_app/admin.py
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from .models import Professor
from geral_app.models import Turma, Categoria
from gerador_app.models import Questao, Avaliacao, RespostaAluno

# Define um "inline" para o perfil do Professor
class ProfessorInline(admin.StackedInline):
    model = Professor
    can_delete = False
    verbose_name_plural = 'Perfil Professor'
    fk_name = 'user'
    # Filtro para o campo M2M de turmas
    filter_horizontal = ('turmas',) 

# Define um novo User admin
class UserAdmin(BaseUserAdmin):
    inlines = (ProfessorInline,)
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff')

    def get_inline_instances(self, request, obj=None):
        if not obj:
            return list()
        return super(UserAdmin, self).get_inline_instances(request, obj)

# Registra os outros models para aparecerem no admin
@admin.register(Questao)
class QuestaoAdmin(admin.ModelAdmin):
    list_display = ('enunciado', 'categoria', 'dificuldade')
    list_filter = ('categoria', 'dificuldade')

# Re-registra o User admin
admin.site.unregister(User)
admin.site.register(User, UserAdmin)

# Registra os models simples
admin.site.register(Turma)
admin.site.register(Categoria)
admin.site.register(Avaliacao)
admin.site.register(RespostaAluno)