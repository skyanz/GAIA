# gaia_project/urls.py

from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('geral_app.urls')),
    path('gerador/', include('gerador_app.urls')),
    path('', include('user_app.urls')),
    path('alunos/', include('alunos_app.urls')),
]