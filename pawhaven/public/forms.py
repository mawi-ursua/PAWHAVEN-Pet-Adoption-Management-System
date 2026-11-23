from django import forms

from .models import AdoptionApplication, ContactMessage, RescueReport


class RescueReportForm(forms.ModelForm):
    urgency = forms.ChoiceField(
        choices=RescueReport.Urgency.choices,
        widget=forms.RadioSelect,
        initial=RescueReport.Urgency.LOW,
    )

    class Meta:
        model = RescueReport
        fields = ["location", "image", "urgency", "description"]
        widgets = {
            "location": forms.TextInput(attrs={"placeholder": "Enter Location"}),
            "image": forms.ClearableFileInput(attrs={"accept": "image/*"}),
            "description": forms.Textarea(
                attrs={"placeholder": "Description...", "rows": 4}
            ),
        }


class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactMessage
        fields = ["name", "email", "message"]
        widgets = {"message": forms.Textarea(attrs={"rows": 5})}


class AdoptionApplicationForm(forms.ModelForm):
    class Meta:
        model = AdoptionApplication
        fields = ["applicant_name", "email", "phone", "home_experience"]
        widgets = {"home_experience": forms.Textarea(attrs={"rows": 5})}