from typing import Any

from django import forms
from django.core.exceptions import ValidationError

from contact.models import Contact


class ContactForm(forms.ModelForm):
    first_name = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'placeholder': 'First name',
            }
        ),
        label='Primeiro nome',
        help_text='Informe o primeiro nome do contato.',
    )

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)

    class Meta:
        model = Contact
        fields = [
            'first_name',
            'last_name',
            'phone',
        ]

    def clean(self) -> dict[str, Any]:

        self.add_error(
            None,
            ValidationError('This is a test error.', code='test')
        )

        return super().clean()
