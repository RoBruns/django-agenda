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
        cleaned_data = self.cleaned_data
        first_name = cleaned_data.get('first_name')
        last_name = cleaned_data.get('last_name')

        if first_name == last_name:
            msg = ValidationError(
                'Primeiro nome não pode ser igual ao segundo',
                code='invalid'
            )
            self.add_error('first_name', msg)
            self.add_error('last_name', msg)

        return super().clean()

    def clean_first_name(self) -> str:
        first_name = self.cleaned_data.get('first_name')

        if len(first_name) < 3:
            raise ValidationError(
                'Primeiro nome deve ter mais de 3 caracteres',
                code='invalid'
            )

        return first_name