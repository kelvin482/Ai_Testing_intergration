from django import forms

from .models import Cow


class CowRegistrationForm(forms.ModelForm):
    class Meta:
        model = Cow
        fields = [
            "cow_number",
            "name",
            "breed",
            "date_of_birth",
            "is_pregnant",
            "expected_calving_date",
            "is_lactating",
            "photo",
            "notes",
        ]
        widgets = {
            "cow_number": forms.TextInput(
                attrs={"placeholder": "e.g. COW-001", "class": "form-input"}
            ),
            "name": forms.TextInput(
                attrs={"placeholder": "e.g. Daisy, Bella, Rosie", "class": "form-input"}
            ),
            "breed": forms.Select(attrs={"class": "form-input"}),
            "date_of_birth": forms.DateInput(
                attrs={"type": "date", "class": "form-input"}
            ),
            "expected_calving_date": forms.DateInput(
                attrs={"type": "date", "class": "form-input"}
            ),
            "notes": forms.Textarea(
                attrs={
                    "rows": 4,
                    "placeholder": "Any notes about this cow...",
                    "class": "form-input",
                }
            ),
            "photo": forms.ClearableFileInput(
                attrs={"accept": "image/*", "class": "sr-only", "id": "id_photo"}
            ),
        }
        labels = {
            "cow_number": "Cow Number",
            "date_of_birth": "Date of Birth",
            "expected_calving_date": "Expected Calving Date",
            "is_pregnant": "Currently Pregnant?",
            "is_lactating": "Currently Lactating?",
            "photo": "Cow Image",
        }

    def clean(self):
        cleaned_data = super().clean()
        is_pregnant = cleaned_data.get("is_pregnant")
        expected_calving_date = cleaned_data.get("expected_calving_date")

        if expected_calving_date and not is_pregnant:
            self.add_error(
                "expected_calving_date",
                "Set the cow as pregnant before adding an expected calving date.",
            )
        return cleaned_data

    def clean_photo(self):
        photo = self.cleaned_data.get("photo")
        if not photo:
            return photo

        content_type = getattr(photo, "content_type", "")
        if content_type and not content_type.startswith("image/"):
            raise forms.ValidationError("Upload an image file only.")
        if photo.size > 5 * 1024 * 1024:
            raise forms.ValidationError("Image size should be 5 MB or less.")
        return photo
