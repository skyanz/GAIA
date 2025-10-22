# user_app/views.py

from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib import messages
from .forms import ProfessorRegistrationForm, ProfessorLoginForm
# Precisamos importar o User para a listagem
from django.contrib.auth.models import User


def login_view(request):
    if request.method == 'POST':
        form = ProfessorLoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, 'Login realizado com sucesso!')
                return redirect('dashboard')
    else:
        form = ProfessorLoginForm()
    
    return render(request, './login.html', {'form': form})

@login_required
@permission_required('auth.add_user', raise_exception=True) # <-- Permissão mudou!
def register_professor(request):
    if request.method == 'POST':
        form = ProfessorRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Professor cadastrado com sucesso!')
            return redirect('dashboard')
    else:
        form = ProfessorRegistrationForm()
    
    return render(request, './register_professor.html', {'form': form})

@login_required
@permission_required('auth.view_user', raise_exception=True) # <-- Permissão mudou!
def professor_list(request):
    professores = User.objects.filter(profile__isnull=False)
    return render(request, 'user_app/professor_list.html', {'professores': professores})

@login_required
def dashboard(request):
    return render(request, 'user_app/dashboard.html')