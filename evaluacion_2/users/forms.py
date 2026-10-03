from django import forms
from django.contrib.auth import get_user_model

User = get_user_model()


class UsuarioForm(forms.ModelForm):

    password = forms.CharField(
        label="Contraseña",
        widget=forms.PasswordInput,
        required=False,
        help_text="Deja vacío para mantener la contraseña actual al editar."
    )

    class Meta:
        model = User

        fields = [
            'username',
            'first_name',
            'last_name',
            'email',
            'role',
            'is_active',
            'password',
        ]

        labels = {
            'username': 'Nombre de usuario',
            'first_name': 'Nombre',
            'last_name': 'Apellido',
            'email': 'Correo electrónico',
            'role': 'Rol',
            'is_active': 'Usuario activo',
        }

        widgets = {
            'role': forms.Select(),
            'is_active': forms.CheckboxInput(),
        }

    def save(self, commit=True):

        user = super().save(commit=False)

        password = self.cleaned_data.get('password')

        if password:
            user.set_password(password)

        if commit:
            user.save()

        return user