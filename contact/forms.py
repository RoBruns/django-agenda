from typing import Any

from django import forms
from django.contrib.auth import password_validation
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

from contact.models import Contact


class ContactForm(forms.ModelForm):
    picture = forms.ImageField(
        widget=forms.FileInput(
            attrs={
                'accept': 'image/*',
            }
        ),
    )

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
            'email',
            'description',
            'category',
            'picture'
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
                'Nome deve ter mais de 3 caracteres',
                code='invalid'
            )

        return first_name


class ResgisterForm(UserCreationForm):

    first_name = forms.CharField(
        required=True,
    )

    last_name = forms.CharField(
        required=True,
    )

    email = forms.EmailField(
        required=True,
    )

    class Meta:
        model = User
        fields = [
            'first_name',
            'last_name',
            'email',
            'username',
            'password1',
            'password2',
        ]

    def clean_email(self) -> str:
        email = self.cleaned_data.get('email')

        if User.objects.filter(email=email).exists():
            self.add_error(
                'email',
                ValidationError(
                    'Email já cadastrado',
                    code='invalid'
                )
            )

        return email


class RegisterUpdateForm(forms.ModelForm):
    first_name = forms.CharField(
        required=True,
        min_length=3,
        max_length=50,
        help_text='Required',
        error_messages={
            'required': 'Campo obrigatório',
            'min_length': 'Nome deve ter mais de 3 caracteres',
            'max_length': 'Nome deve ter menos de 50 caracteres',
        }
    )

    last_name = forms.CharField(
        required=True,
        min_length=3,
        max_length=50,
        help_text='Required',
        error_messages={
            'required': 'Campo obrigatório',
            'min_length': 'Sobrenome deve ter mais de 3 caracteres',
            'max_length': 'Sobrenome deve ter menos de 50 caracteres',
        }
    )

    email = forms.EmailField(
        required=True,
        help_text='Required',
        error_messages={
            'required': 'Campo obrigatório',
            'invalid': 'Email inválido',
        }
    )

    username = forms.CharField(
        required=True,
        min_length=3,
        max_length=50,
        help_text='Required',
        error_messages={
            'required': 'Campo obrigatório',
            'min_length': 'Usuário deve ter mais de 3 caracteres',
            'max_length': 'Usuário deve ter menos de 50 caracteres',
        }
    )

    password1 = forms.CharField(
        label='Password',
        strip=False,
        widget=forms.PasswordInput(
            attrs={
                'autocomplete': 'new-password',
            }
        ),
        help_text=password_validation.password_validators_help_text_html(),
        required=False,
    )

    password2 = forms.CharField(
        label='Password confirmation',
        widget=forms.PasswordInput(
            attrs={
                'autocomplete': 'new-password',
            }
        ),
        strip=False,
        help_text='Use a senha que você digitou anteriormente',
        required=False,
    )

    class Meta:
        model = User
        fields = (
            'first_name', 'last_name', 'email',
            'username',
        )

    def save(self, commit=True):
        cleaned_data = self.cleaned_data
        user = super().save(commit=False)
        password = cleaned_data.get('password1')

        if password:
            user.set_password(password)

        if commit:
            user.save()

        return user

    def clean(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')

        if password1 or password2:
            if password1 != password2:
                self.add_error(
                    'password2',
                    ValidationError('Senhas não batem')
                )

        return super().clean()

    def clean_email(self):
        email = self.cleaned_data.get('email')
        current_email = self.instance.email

        if current_email != email:
            if User.objects.filter(email=email).exists():
                self.add_error(
                    'email',
                    ValidationError('Já existe este e-mail', code='invalid')
                )

        return email

    def clean_password1(self):
        password1 = self.cleaned_data.get('password1')

        if password1:
            try:
                password_validation.validate_password(password1)
            except ValidationError as errors:
                self.add_error(
                    'password1',
                    ValidationError(errors)
                )

        return password1