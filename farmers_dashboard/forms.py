from django import forms

from .models import Cow


class CowRegistrationForm(forms.ModelForm):
    reproductive_status = forms.ChoiceField(
        choices=Cow.REPRODUCTIVE_STATUS_CHOICES,
        required=True,
        widget=forms.RadioSelect(
            attrs={"class": "sr-only peer reproductive-status-input"}
        ),
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["insemination_type"].choices = [
            ("", "Choose insemination type")
        ] + list(Cow.INSEMINATION_TYPE_CHOICES)

    class Meta:
        model = Cow
        fields = [
            "cow_number",
            "name",
            "breed",
            "date_of_birth",
            "reproductive_status",
            "last_heat_date",
            "insemination_type",
            "insemination_date",
            "pregnancy_confirmation_date",
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
            "last_heat_date": forms.DateInput(
                attrs={"type": "date", "class": "form-input"}
            ),
            "insemination_type": forms.Select(
                attrs={"class": "form-input"}
            ),
            "insemination_date": forms.DateInput(
                attrs={"type": "date", "class": "form-input"}
            ),
            "pregnancy_confirmation_date": forms.DateInput(
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
            "last_heat_date": "Last Heat Date",
            "insemination_type": "Insemination Type",
            "insemination_date": "Insemination Date",
            "pregnancy_confirmation_date": "Pregnancy Confirmation Date",
            "expected_calving_date": "Expected Calving Date",
            "is_pregnant": "Currently Pregnant?",
            "is_lactating": "Currently Lactating?",
            "photo": "Cow Image",
        }

    def clean(self):
        cleaned_data = super().clean()
        reproductive_status = cleaned_data.get("reproductive_status")
        last_heat_date = cleaned_data.get("last_heat_date")
        insemination_type = cleaned_data.get("insemination_type")
        insemination_date = cleaned_data.get("insemination_date")
        pregnancy_confirmation_date = cleaned_data.get("pregnancy_confirmation_date")
        is_pregnant = cleaned_data.get("is_pregnant")
        expected_calving_date = cleaned_data.get("expected_calving_date")

        if not reproductive_status:
            self.add_error(
                "reproductive_status",
                "Choose the current reproductive starting point for this cow.",
            )
            return cleaned_data

        if reproductive_status == Cow.REPRODUCTIVE_STATUS_NOT_INSEMINATED:
            if not last_heat_date:
                self.add_error(
                    "last_heat_date",
                    "Add the latest observed heat date to start the cow on the right path.",
                )
            if not insemination_type:
                self.add_error(
                    "insemination_type",
                    "Choose the insemination type you want to prepare for this cow.",
                )

        if reproductive_status == Cow.REPRODUCTIVE_STATUS_INSEMINATED:
            if not insemination_date:
                self.add_error(
                    "insemination_date",
                    "Add the insemination date to continue with the tracker.",
                )

        if reproductive_status == Cow.REPRODUCTIVE_STATUS_PREGNANCY_CONFIRMED:
            if not (pregnancy_confirmation_date or expected_calving_date):
                self.add_error(
                    "pregnancy_confirmation_date",
                    "Add a pregnancy confirmation date or an expected calving date.",
                )

        if reproductive_status == Cow.REPRODUCTIVE_STATUS_NEAR_CALVING:
            if not expected_calving_date:
                self.add_error(
                    "expected_calving_date",
                    "Add the expected calving date before starting the calving watch.",
                )

        if expected_calving_date and reproductive_status in {
            Cow.REPRODUCTIVE_STATUS_PREGNANCY_CONFIRMED,
            Cow.REPRODUCTIVE_STATUS_NEAR_CALVING,
        }:
            cleaned_data["is_pregnant"] = True
        elif reproductive_status in {
            Cow.REPRODUCTIVE_STATUS_NOT_INSEMINATED,
            Cow.REPRODUCTIVE_STATUS_INSEMINATED,
        }:
            cleaned_data["is_pregnant"] = False

        if expected_calving_date and reproductive_status == Cow.REPRODUCTIVE_STATUS_NOT_INSEMINATED:
            self.add_error(
                "expected_calving_date",
                "Expected calving date comes later after insemination or pregnancy confirmation.",
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
