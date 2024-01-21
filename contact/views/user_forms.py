from django.shortcuts import render

from contact.forms import ResgisterForm


def register(request):
    form = ResgisterForm()

    if request.method == 'POST':
        form = ResgisterForm(request.POST)

        if form.is_valid():
            form.save()
    return render(
        request,
        'contact/register.html',
        {
            'form': form,
        }

        )
