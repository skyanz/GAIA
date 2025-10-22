# USER_APP/FORMS.PY
from django import forms
from django.contrib.auth.forms import AuthenticationForm
# Importe os models corretos!
from django.contrib.auth.models import User
from .models import Professor
from geral_app.models import Turma

class ProfessorRegistrationForm(forms.ModelForm):
    # Campos do 'User'
    username = forms.CharField(
        label='Nome de Usuário',
        max_length=100,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nome de Usuário'})
    )
    first_name = forms.CharField(
        label='Nome',
        max_length=100,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nome'})
    )
    last_name = forms.CharField(
        label='Sobrenome',
        max_length=100,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Sobrenome'})
    )
    email = forms.EmailField(
        label='E-mail',
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'E-mail'})
    )
    password = forms.CharField(
        label='Senha',
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Senha'})
    )
    password2 = forms.CharField(
        label='Confirmar Senha',
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirmar Senha'})
    )

    # Campos do 'Professor'
    turmas = forms.ModelMultipleChoiceField(
        label='Turmas',
        queryset=Turma.objects.all(),
        widget=forms.SelectMultiple(attrs={'class': 'form-select'}),
        required=False
    )
    telefone = forms.CharField(
        label='Telefone',
        max_length=15,
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Telefone (Opcional)'})
    )

    class Meta:
        model = User  # O formulário principal é do User
        fields = ['username', 'first_name', 'last_name', 'email', 'turmas', 'telefone']

    def clean_password2(self):
        # Validação de senha
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('As senhas não são iguais.')
        return cd['password2']

    def clean_email(self):
        # Validação de email
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('Um usuário com este e-mail já existe.')
        return email

    def save(self, commit=True):
        # Lógica para salvar os dois models (User e Professor)
        user = User.objects.create_user(
            username=self.cleaned_data['username'],
            email=self.cleaned_data['email'],
            password=self.cleaned_data['password'],
            first_name=self.cleaned_data['first_name'],
            last_name=self.cleaned_data['last_name']
        )

        # Cria o perfil de Professor
        professor = Professor.objects.create(
            user=user,
            telefone=self.cleaned_data.get('telefone'),
            # materia=... (você pode adicionar um campo 'materia' no form se quiser)
        )

        # Adiciona as turmas (relação ManyToMany)
        professor.turmas.set(self.cleaned_data['turmas'])

        return user


# Este é o seu formulário de login, ele não afeta o cadastro, mas está correto.
class ProfessorLoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Nome de Usuário'
        })
        self.fields['password'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Senha'
        })