from django.shortcuts import render, redirect
from .forms import LoginForm, UserCreateForm
from django.contrib.auth import logout, login, authenticate
# Create your views here.


def login_view(request):
    if request.POST:
        form = LoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('index')

    form = LoginForm()
    context = {
        'form': form,
    }
    return render(request, 'login.html', context)


def logout_view(request):
    if request.user.is_authenticated:
        logout(request)
    return redirect('index')


def register_view(request):
    if request.POST:
        form = UserCreateForm(data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')

    form = UserCreateForm()
    context = {
        'form': form
    }
    return render(request, 'register.html', context)
