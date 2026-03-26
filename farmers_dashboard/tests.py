import shutil
from datetime import timedelta
from pathlib import Path

from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase, override_settings
from django.urls import reverse
from django.utils import timezone

from users.models import Profile, Role

from .models import Cow


class FarmersDashboardViewTests(TestCase):
    def setUp(self):
        self.media_root = Path("c:/Users/PC/OneDrive/Documents/DIGITAL FARM/.test_media")
        shutil.rmtree(self.media_root, ignore_errors=True)
        self.media_root.mkdir(parents=True, exist_ok=True)
        self.override = override_settings(MEDIA_ROOT=self.media_root)
        self.override.enable()
        self.addCleanup(self.override.disable)
        self.addCleanup(lambda: shutil.rmtree(self.media_root, ignore_errors=True))

        self.role, _ = Role.objects.get_or_create(
            slug="farmer",
            defaults={
                "name": "Farmer",
                "dashboard_namespace": "farmers_dashboard",
                "default_path": "/farmers/",
            },
        )
        self.user = User.objects.create_user(
            username="farmer-user",
            email="farmer@example.com",
            password="StrongPass123!",
            first_name="John",
        )

    def _login_farmer(self):
        Profile.objects.create(user=self.user, role=self.role)
        self.client.force_login(self.user)

    def _create_cow(self, **overrides):
        defaults = {
            "owner": self.user,
            "cow_number": "COW-001",
            "name": "Daisy",
            "breed": Cow.BREED_FRIESIAN,
            "is_pregnant": True,
            "expected_calving_date": timezone.localdate() + timedelta(days=10),
            "tracking_stage": Cow.STAGE_NEARING_CALVING,
        }
        defaults.update(overrides)
        return Cow.objects.create(**defaults)

    def test_farmer_dashboard_requires_login(self):
        response = self.client.get(reverse("farmers_dashboard:dashboard"))
        self.assertEqual(response.status_code, 302)
        self.assertIn("/accounts/login/", response["Location"])

    def test_dashboard_shows_empty_state_without_cows(self):
        self._login_farmer()

        response = self.client.get(reverse("farmers_dashboard:dashboard"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No cows registered yet")
        self.assertContains(response, "Register First Cow")
        self.assertContains(response, "Total cows")
        self.assertContains(response, "Add Cow")

    def test_register_cow_creates_record_and_redirects_to_tracking(self):
        self._login_farmer()

        response = self.client.post(
            reverse("farmers_dashboard:cow_register"),
            data={
                "cow_number": "COW-009",
                "name": "Bella",
                "breed": Cow.BREED_AYRSHIRE,
                "date_of_birth": "2023-02-14",
                "is_pregnant": "on",
                "expected_calving_date": (timezone.localdate() + timedelta(days=8)).isoformat(),
                "is_lactating": "",
                "notes": "First pregnancy for this cow.",
                "photo": SimpleUploadedFile(
                    "bella.png",
                    b"fake-image-content",
                    content_type="image/png",
                ),
            },
            follow=False,
        )

        cow = Cow.objects.get()
        self.assertRedirects(
            response,
            reverse("farmers_dashboard:cow_tracking", args=[cow.pk]),
            fetch_redirect_response=False,
        )
        self.assertEqual(cow.owner, self.user)
        self.assertEqual(cow.cow_number, "COW-009")
        self.assertEqual(cow.tracking_stage, Cow.STAGE_NEARING_CALVING)
        self.assertTrue(cow.photo.name)

    def test_farmer_pages_render_registered_cow_content(self):
        self._login_farmer()
        cow = self._create_cow()

        dashboard_response = self.client.get(reverse("farmers_dashboard:dashboard"))
        herd_response = self.client.get(reverse("farmers_dashboard:herd"))
        alerts_response = self.client.get(reverse("farmers_dashboard:alerts"))
        reports_response = self.client.get(reverse("farmers_dashboard:reports"))
        service_response = self.client.get(reverse("farmers_dashboard:service_finder"))

        self.assertContains(dashboard_response, "Herd overview")
        self.assertContains(dashboard_response, cow.name)
        self.assertContains(dashboard_response, "Track calving")
        self.assertContains(herd_response, "My cows")
        self.assertContains(herd_response, cow.cow_number)
        self.assertContains(alerts_response, "Cow alerts")
        self.assertContains(alerts_response, cow.name)
        self.assertContains(reports_response, "Follow-up schedule")
        self.assertContains(reports_response, cow.name)
        self.assertContains(service_response, "Find veterinary support by county")

    def test_tracking_page_updates_stage_and_attention(self):
        self._login_farmer()
        cow = self._create_cow(needs_attention=False, tracking_stage=Cow.STAGE_PREGNANT)

        stage_response = self.client.post(
            reverse("farmers_dashboard:cow_tracking", args=[cow.pk]),
            {"tracking_stage": Cow.STAGE_ACTIVE_LABOR},
            follow=True,
        )
        cow.refresh_from_db()
        self.assertEqual(cow.tracking_stage, Cow.STAGE_ACTIVE_LABOR)
        self.assertContains(stage_response, "tracking stage updated")

        attention_response = self.client.post(
            reverse("farmers_dashboard:cow_tracking", args=[cow.pk]),
            {"toggle_attention": "1"},
            follow=True,
        )
        cow.refresh_from_db()
        self.assertTrue(cow.needs_attention)
        self.assertContains(attention_response, "marked as needing attention")

    def test_farmer_dashboard_redirects_other_roles(self):
        other_role, _ = Role.objects.get_or_create(
            slug="veterinary",
            defaults={
                "name": "Veterinary",
                "dashboard_namespace": "veterinary_dashboard",
                "default_path": "/veterinary/",
            },
        )
        Profile.objects.create(user=self.user, role=other_role)
        self.client.force_login(self.user)

        response = self.client.get(reverse("farmers_dashboard:dashboard"))

        self.assertRedirects(response, "/veterinary/", fetch_redirect_response=False)
