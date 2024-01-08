from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse

from contact.forms import ContactForm
from contact.models import Contact


def create(request):
    form_action = reverse('contact:create')
    
    if request.method == 'POST':
        form = ContactForm(data=request.POST)

        context = {
            'form': form,
            'form_action': form_action,
        }

        if form.is_valid():
            contact = form.save(commit=False)
            contact.save()
            return redirect('contact:update', contact_id=contact.id)

        context = {
            'form': ContactForm(),
            'form_action': form_action,
        }

    context = {
        'form': ContactForm(data=request.POST or None),
    }

    return render(
        request,
        'contact/create.html',
        context
    )


def update(request, contact_id):
    contact = get_object_or_404(Contact, id=contact_id, show=True)

    form_action = reverse('contact:update', args={contact_id})  # type: ignore

    if request.method == 'POST':
        form = ContactForm(data=request.POST, instance=contact)

        context = {
            'form': form,
            'form_action': form_action,
            'contact': contact,
        }

        if form.is_valid():
            contact = form.save(commit=False)
            contact.save()
            return redirect('contact:update', contact_id=contact.id)
        
        return render(
            request,
            'contact/update.html',
            context
        )

    context = {
        'form': ContactForm(instance=contact),
        'form_action': form_action,
        'contact': contact,
    }

    return render(
        request,
        'contact/update.html',
        context
    )
