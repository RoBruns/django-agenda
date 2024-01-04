from django.shortcuts import get_object_or_404, render

from contact.models import Contact


def index(request):
    contacts = Contact.objects \
        .filter(show=True)\
        .order_by('-id')[:10]

    context = {
        'contacts': contacts,
    }

    return render(
        request,
        'contact/index.html',
        context
    )


def contact(request, contact_id):   
    sigle_contact = get_object_or_404(Contact, pk=contact_id, show=True)

    context = {
        'contact': sigle_contact,
    }

    return render(
        request,
        'contact/contact.html',
        context
    )
