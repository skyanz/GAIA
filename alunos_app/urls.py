from django.urls import path
from .views import alunos_view
app_name = 'alunos_app'
# O Django procurará por 'urlpatterns' neste arquivo.
urlpatterns = [
    # A URL '' (raiz do app) será associada à view 'alunos_view'.
    # O nome 'alunos' pode ser usado para referenciar esta URL nos templates.
    path('', alunos_view, name='alunos'),
]
