from django.shortcuts import redirect, render

from contact.forms import ContactForm


def create(request):
    if request.method == 'POST':
        form = ContactForm(data=request.POST)

        context = {
            'form': form,
        }

        if form.is_valid():
            contact = form.save(commit=False)
            contact.save()
            return redirect('contact:create')

        return render(
            request,
            'contact/create.html',
            context
        )

    context = {
        'form': ContactForm(data=request.POST or None),
    }

    return render(
        request,
        'contact/create.html',
        context
    )
