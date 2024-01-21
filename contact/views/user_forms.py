from django.contrib import messages
from django.shortcuts import redirect, render

from contact.forms import ResgisterForm


def register(request):
    form = ResgisterForm()

    if request.method == 'POST':
        form = ResgisterForm(request.POST)

        if form.is_valid():
            form.save()
            messages.success(request, 'Usuário cadastrado com sucesso!')
            return redirect('contact:index')

    return render(
        request,
        'contact/register.html',
        {
            'form': form,
        }

        )
