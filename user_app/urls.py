# user_app/urls.py

from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

app_name = 'user_app'

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('registrar-professor/', views.register_professor, name='register_professor'),
    path('professores/', views.professor_list, name='professor_list'),
]