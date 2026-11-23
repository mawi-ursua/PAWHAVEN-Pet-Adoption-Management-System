from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm

from public.models import Pet, ShelterSettings

User = get_user_model()


class StaffAuthenticationForm(AuthenticationForm):
    """Only staff accounts may sign in to the admin portal."""

    def confirm_login_allowed(self, user):
        super().confirm_login_allowed(user)
        if not user.is_staff:
            raise forms.ValidationError(
                "This account does not have admin access.", code="not_staff"
            )


class PetForm(forms.ModelForm):
    class Meta:
        model = Pet
        fields = [
            "name",
            "species",
            "status",
            "age_months",
            "gender",
            "breed",
            "photo",
            "description",
        ]
        widgets = {
            "photo": forms.ClearableFileInput(attrs={"accept": "image/*"}),
            "description": forms.Textarea(attrs={"rows": 3}),
        }


class ShelterSettingsForm(forms.ModelForm):
    class Meta:
        model = ShelterSettings
        fields = ["name", "address", "contact_number", "email", "description"]
        widgets = {"description": forms.Textarea(attrs={"rows": 3})}


class AdminProfileForm(forms.Form):
    full_name = forms.CharField(max_length=150)
    email = forms.EmailField()

    def __init__(self, *args, user, **kwargs):
        self.user = user
        super().__init__(*args, **kwargs)
        if not self.is_bound:
            self.initial = {
                "full_name": user.get_full_name() or user.get_username(),
                "email": user.email,
            }

    def save(self):
        first, _, last = self.cleaned_data["full_name"].strip().partition(" ")
        self.user.first_name = first
        self.user.last_name = last.strip()
        self.user.email = self.cleaned_data["email"]
        self.user.save(update_fields=["first_name", "last_name", "email"])
        return self.user