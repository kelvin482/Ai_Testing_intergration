from django import forms
from django.contrib.auth.forms import (
    AuthenticationForm,
    SetPasswordForm,
    UserCreationForm,
)
from django.contrib.auth.models import User

try:
    from allauth.account.models import EmailAddress
except ImportError:  # pragma: no cover - fallback if allauth account app changes
    EmailAddress = None


ROLE_CHOICES = [
    ("farmer", "Farmer"),
    ("vet", "Veterinarian"),
    ("manager", "Farm Manager"),
    ("assistant", "Farm Assistant"),
]


def _apply_widget_attrs(field, placeholder, extra_classes=""):
    # Centralize auth field styling so the templates stay focused on layout.
    classes = (
        "auth-input w-full bg-transparent border-b border-sage/40 text-slate-900 "
        "placeholder:text-slate-400 focus:outline-none focus:border-forest "
        "focus:ring-0 py-2 transition"
    )
    if extra_classes:
        classes = f"{classes} {extra_classes}"
    field.widget.attrs.update(
        {
            "class": classes,
            "placeholder": placeholder,
        }
    )


class CowCalvingLoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Restore the original username/password sign-in fields from the
        # earlier auth flow while keeping the newer page structure intact.
        _apply_widget_attrs(self.fields["username"], "Enter your username")
        _apply_widget_attrs(self.fields["password"], "Enter your password")


class PasswordResetCodeRequestForm(forms.Form):
    email = forms.EmailField(required=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        _apply_widget_attrs(self.fields["email"], "name@example.com")


class PasswordResetCodeConfirmForm(SetPasswordForm):
    code = forms.CharField(max_length=6, min_length=6, required=True)

    def __init__(self, user, *args, **kwargs):
        super().__init__(user, *args, **kwargs)
        _apply_widget_attrs(self.fields["code"], "Enter the 6-digit code")
        _apply_widget_attrs(self.fields["new_password1"], "Create a new password")
        _apply_widget_attrs(self.fields["new_password2"], "Confirm the new password")

    def clean_code(self):
        # Keeping the code numeric makes it faster to enter from an email screen.
        code = (self.cleaned_data.get("code") or "").strip()
        if not code.isdigit():
            raise forms.ValidationError("Enter the 6-digit code from your email.")
        return code


class CowCalvingRegisterForm(UserCreationForm):
    first_name = forms.CharField(max_length=150, required=True)
    last_name = forms.CharField(max_length=150, required=True)
    email = forms.EmailField(required=True)
    role = forms.ChoiceField(choices=ROLE_CHOICES, required=False)
    farm_name = forms.CharField(max_length=200, required=False)

    class Meta(UserCreationForm.Meta):
        model = User
        fields = (
            "first_name",
            "last_name",
            "username",
            "email",
            "role",
            "farm_name",
            "password1",
            "password2",
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["role"].choices = [("", "Select role")] + list(ROLE_CHOICES)
        _apply_widget_attrs(self.fields["first_name"], "First name")
        _apply_widget_attrs(self.fields["last_name"], "Last name")
        _apply_widget_attrs(self.fields["username"], "Choose a username")
        _apply_widget_attrs(self.fields["email"], "name@example.com")
        _apply_widget_attrs(self.fields["role"], "Select role")
        _apply_widget_attrs(self.fields["farm_name"], "Optional farm name")
        _apply_widget_attrs(self.fields["password1"], "Create a password")
        _apply_widget_attrs(self.fields["password2"], "Confirm your password")

        for field in self.fields.values():
            if field.required:
                field.widget.attrs.setdefault("data-progress", "1")

    def clean_email(self):
        # Manual signup should honor the same unique-email expectation as account recovery.
        email = (self.cleaned_data.get("email") or "").strip()
        if not email:
            return email

        if User.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError("An account with this email already exists.")

        if EmailAddress and EmailAddress.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError("An account with this email already exists.")

        return email

    def save(self, commit=True):
        user = super().save(commit=False)
        user.first_name = self.cleaned_data.get("first_name", "")
        user.last_name = self.cleaned_data.get("last_name", "")
        user.email = self.cleaned_data.get("email", "")

        if commit:
            user.save()
        # role and farm_name stay on the form for now until a dedicated profile
        # model is added for storing those extra signup details.
        return user
