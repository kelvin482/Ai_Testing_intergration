from django.conf import settings
from django.core.validators import FileExtensionValidator
from django.db import models
from django.utils import timezone
from django.utils.functional import cached_property


class Cow(models.Model):
    BREED_FRIESIAN = "friesian"
    BREED_AYRSHIRE = "ayrshire"
    BREED_JERSEY = "jersey"
    BREED_GUERNSEY = "guernsey"
    BREED_SAHIWAL = "sahiwal"
    BREED_CROSSBREED = "crossbreed"
    BREED_OTHER = "other"

    BREED_CHOICES = [
        (BREED_FRIESIAN, "Friesian"),
        (BREED_AYRSHIRE, "Ayrshire"),
        (BREED_JERSEY, "Jersey"),
        (BREED_GUERNSEY, "Guernsey"),
        (BREED_SAHIWAL, "Sahiwal"),
        (BREED_CROSSBREED, "Crossbreed"),
        (BREED_OTHER, "Other"),
    ]

    REPRODUCTIVE_STATUS_NOT_INSEMINATED = "not_inseminated"
    REPRODUCTIVE_STATUS_INSEMINATED = "inseminated"
    REPRODUCTIVE_STATUS_PREGNANCY_CONFIRMED = "pregnancy_confirmed"
    REPRODUCTIVE_STATUS_NEAR_CALVING = "near_calving"

    REPRODUCTIVE_STATUS_CHOICES = [
        (REPRODUCTIVE_STATUS_NOT_INSEMINATED, "Not inseminated yet"),
        (REPRODUCTIVE_STATUS_INSEMINATED, "Already inseminated"),
        (REPRODUCTIVE_STATUS_PREGNANCY_CONFIRMED, "Pregnancy confirmed"),
        (REPRODUCTIVE_STATUS_NEAR_CALVING, "Near calving"),
    ]

    INSEMINATION_TYPE_ARTIFICIAL = "artificial_insemination"
    INSEMINATION_TYPE_NATURAL = "natural_service"

    INSEMINATION_TYPE_CHOICES = [
        (INSEMINATION_TYPE_ARTIFICIAL, "Artificial insemination"),
        (INSEMINATION_TYPE_NATURAL, "Natural service"),
    ]

    STAGE_REGISTERED = "registered"
    STAGE_INSEMINATED = "inseminated"
    STAGE_PREGNANT = "pregnant"
    STAGE_NEARING_CALVING = "nearing_calving"
    STAGE_ACTIVE_LABOR = "active_labor"
    STAGE_POST_CALVING = "post_calving"

    TRACKING_STAGE_CHOICES = [
        (STAGE_REGISTERED, "Registered"),
        (STAGE_INSEMINATED, "Inseminated"),
        (STAGE_PREGNANT, "Pregnant"),
        (STAGE_NEARING_CALVING, "Nearing calving"),
        (STAGE_ACTIVE_LABOR, "Active labor"),
        (STAGE_POST_CALVING, "Post-calving"),
    ]

    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="cows",
    )
    cow_number = models.CharField(max_length=40)
    name = models.CharField(max_length=120)
    breed = models.CharField(max_length=40, choices=BREED_CHOICES)
    date_of_birth = models.DateField(blank=True, null=True)
    reproductive_status = models.CharField(
        max_length=32,
        choices=REPRODUCTIVE_STATUS_CHOICES,
        blank=True,
        default="",
    )
    last_heat_date = models.DateField(blank=True, null=True)
    insemination_type = models.CharField(
        max_length=32,
        choices=INSEMINATION_TYPE_CHOICES,
        blank=True,
        default="",
    )
    insemination_date = models.DateField(blank=True, null=True)
    pregnancy_confirmation_date = models.DateField(blank=True, null=True)
    expected_calving_date = models.DateField(blank=True, null=True)
    is_pregnant = models.BooleanField(default=False)
    is_lactating = models.BooleanField(default=False)
    needs_attention = models.BooleanField(default=False)
    tracking_stage = models.CharField(
        max_length=32,
        choices=TRACKING_STAGE_CHOICES,
        default=STAGE_REGISTERED,
    )
    photo = models.FileField(
        upload_to="cow_photos/",
        blank=True,
        validators=[
            FileExtensionValidator(
                allowed_extensions=["jpg", "jpeg", "png", "webp", "gif"]
            )
        ],
    )
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["name", "cow_number"]
        constraints = [
            models.UniqueConstraint(
                fields=["owner", "cow_number"],
                name="unique_cow_number_per_owner",
            )
        ]

    def __str__(self):
        return f"{self.name} ({self.cow_number})"

    def is_due_this_month(self):
        if not self.expected_calving_date:
            return False
        today = timezone.localdate()
        return (
            self.expected_calving_date.year == today.year
            and self.expected_calving_date.month == today.month
        )

    def is_nearing_calving(self):
        if not self.expected_calving_date:
            return False
        days_until_due = (self.expected_calving_date - timezone.localdate()).days
        return 0 <= days_until_due <= 30

    @cached_property
    def photo_url(self):
        return self.photo.url if self.photo else ""

    @property
    def reproductive_status_label(self):
        if self.reproductive_status:
            return dict(self.REPRODUCTIVE_STATUS_CHOICES).get(
                self.reproductive_status,
                "Reproductive status",
            )
        if self.is_nearing_calving():
            return "Near calving"
        if self.is_pregnant:
            return "Pregnancy confirmed"
        return "Registered"

    @property
    def status_tone(self):
        if self.needs_attention:
            return "rose"
        if self.is_nearing_calving():
            return "amber"
        if self.tracking_stage == self.STAGE_INSEMINATED:
            return "violet"
        if self.is_pregnant:
            return "sky"
        return "emerald"

    @property
    def status_label(self):
        if self.needs_attention:
            return "Needs attention"
        if self.is_nearing_calving():
            return "Nearing calving"
        if self.tracking_stage == self.STAGE_INSEMINATED:
            return "Inseminated"
        if self.is_pregnant:
            return "Pregnant"
        return "Registered"

    @property
    def summary_text(self):
        if self.reproductive_status == self.REPRODUCTIVE_STATUS_NOT_INSEMINATED:
            if self.last_heat_date:
                return f"Last heat observed {self.last_heat_date:%d %b %Y}"
            return "Ready for insemination planning"
        if self.insemination_date and self.tracking_stage == self.STAGE_INSEMINATED:
            return f"Inseminated on {self.insemination_date:%d %b %Y}"
        if self.pregnancy_confirmation_date:
            return (
                f"Pregnancy confirmed {self.pregnancy_confirmation_date:%d %b %Y}"
            )
        if self.expected_calving_date and self.is_nearing_calving():
            return f"Expected calving {self.expected_calving_date:%d %b %Y}"
        if self.expected_calving_date and self.is_pregnant:
            return f"Expected calving {self.expected_calving_date:%d %b %Y}"
        if self.is_lactating:
            return "Currently lactating"
        return "Cow profile ready for tracking"

    @property
    def alert_category(self):
        if self.needs_attention:
            return "Needs attention"
        if self.is_nearing_calving():
            return "Nearing calving"
        if self.tracking_stage == self.STAGE_INSEMINATED:
            return "Inseminated"
        if self.is_pregnant:
            return "Pregnant"
        return "Registered"

    @property
    def next_action_text(self):
        if self.needs_attention:
            return "Review the cow and open support if the issue continues."
        if self.tracking_stage == self.STAGE_ACTIVE_LABOR:
            return "Track labour progress closely and prepare for escalation."
        if self.tracking_stage == self.STAGE_INSEMINATED:
            return "Keep watch after service and plan the pregnancy check."
        if self.is_nearing_calving():
            return "Start calving watch and keep the pen ready."
        if self.is_pregnant:
            return "Keep pregnancy follow-up and calving dates visible."
        if self.reproductive_status == self.REPRODUCTIVE_STATUS_NOT_INSEMINATED:
            return "Keep heat dates visible and prepare the next insemination step."
        return "Complete registration details and start tracking when ready."
