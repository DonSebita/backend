from django import forms
from api.models import programmer


class ProgrammerForm(forms.ModelForm):
    class Meta:
        model = programmer
        fields = [
            "fullname",
            "nickname",
            "language",
            "age",
            "is_active",
        ]