from django.contrib import auth, messages
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import redirect, render

from contact.forms import RegisterUpdateForm, ResgisterForm


def register(request):
    form = ResgisterForm()

    if request.method == 'POST':
        form = ResgisterForm(request.POST)

        if form.is_valid():

            form.save()
            messages.success(request, 'Usuário cadastrado com sucesso!')
            return redirect('contact:login')

    return render(
        request,
        'contact/register.html',
        {
            'form': form,
        }

        )


def login_view(request):
    form = AuthenticationForm(request)

    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)

        if form.is_valid():
            user = form.get_user()
            messages.success(request, 'Bem vindo, {}!'.format(user.username))
            auth.login(request, user)
            return redirect('contact:index')
        
        messages.error(request, 'Usuário ou senha inválidos!')

    return render(
        request,
        'contact/login.html',
        {
            'form': form,
        }
    )


def logout_view(request):
    auth.logout(request)
    messages.success(request, 'Logout realizado com sucesso!')
    return redirect('contact:login')


def update_user(request):
    form = RegisterUpdateForm(instance=request.user)

    if request.method != 'POST':
        return render(
            request,
            'contact/register.html',
            {
                'form': form,
            }
        )
    
    form = RegisterUpdateForm(request.POST, instance=request.user)

    if not form.is_valid():
        return render(
            request,
            'contact/register.html',
            {
                'form': form,
            }
        )
    
    form.save()