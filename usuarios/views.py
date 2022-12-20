from django.shortcuts import render
from django.http import HttpResponse
from rolepermissions.decorators import has_permission_decorator
from .models import Users
from django.shortcuts import redirect
from django.urls import reverse
from django.contrib import auth

@has_permission_decorator('cadastrar_vendedor')
def cadastrar_vendedor(request):
    if request.method == "GET":
       return render(request, 'cadastrar_vendedor.html')
    if request.method == "POST":
        email = request.POST.get('email')
        senha = request.POST.get('senha')

        user = Users.objects.filter(email=email)
        if user.exists():
            # TODO: Utilizar mensagens do django
            return HttpResponse('E-mail ja existe')

        user = Users.objects.create_user(username=email, email=email, password=senha, cargo="V")

        #TODO: Redirecionar com uma mensagen
        return HttpResponse('Conta criada')


def login(request):
    if request.method == "GET":
       if request.user.is_authenticated:
           return redirect(reverse('plataforma'))
       return render (request, 'login.html')
    elif request.method == "POST":
        login = request.POST.get('email')
        senha = request.POST.get('senha')

        user = auth.authenticate(username=login, password=senha)

        if not user:
            #TODO:redirecionar com mensagem de erro
            return HttpResponse('Usuário invalido')

        auth.login(request,user)
        return HttpResponse('Usuário logado com sucesso')


def logout(request):
    request.session.flush()
    return redirect(reverse('login'))