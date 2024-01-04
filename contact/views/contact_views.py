from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render

from contact.models import Contact


def index(request):
    contacts = Contact.objects \
        .filter(show=True)\
        .order_by('-id')[:10]

    context = {
        'contacts': contacts,
        'site_title': 'Contatos -'
    }

    return render(
        request,
        'contact/index.html',
        context
    )


def search(request):
    search_value = request.GET.get('q', "").strip()

    if not search_value:
        return redirect('contact:index')

    contacts = Contact.objects \
        .filter(show=True)\
        .filter(
            Q(first_name__icontains=search_value) |
            Q(last_name__icontains=search_value) |
            Q(email__icontains=search_value) |
            Q(phone__icontains=search_value) |
            Q(id__icontains=search_value)
        )\
        .order_by('-id')

    context = {
        'contacts': contacts,
        'site_title': f'Search: {search_value} -'
    }

    return render(
        request,
        'contact/index.html',
        context
    )


def contact(request, contact_id,):
    sigle_contact = get_object_or_404(Contact, pk=contact_id, show=True)

    context = {
        'contact': sigle_contact,
        'site_title': f'{sigle_contact.first_name} {sigle_contact.last_name} -'
    }

    return render(
        request,
        'contact/contact.html',
        context
    )
