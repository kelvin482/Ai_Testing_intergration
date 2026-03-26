from django.contrib import admin

from .models import Cow, InseminationRequest, ReproductiveEvent


@admin.register(Cow)
class CowAdmin(admin.ModelAdmin):
    list_display = (
        "cow_number",
        "name",
        "owner",
        "reproductive_status",
        "tracking_stage",
        "needs_attention",
    )
    list_filter = ("reproductive_status", "tracking_stage", "needs_attention")
    search_fields = ("cow_number", "name", "owner__username", "owner__email")


@admin.register(InseminationRequest)
class InseminationRequestAdmin(admin.ModelAdmin):
    list_display = ("cow", "farmer", "service_type", "status", "submitted_at")
    list_filter = ("status", "service_type")
    search_fields = ("cow__name", "cow__cow_number", "farmer__username", "farmer__email")


@admin.register(ReproductiveEvent)
class ReproductiveEventAdmin(admin.ModelAdmin):
    list_display = ("cow", "event_type", "event_date", "recorded_by", "created_at")
    list_filter = ("event_type", "event_date")
    search_fields = ("cow__name", "cow__cow_number", "recorded_by__username", "recorded_by__email")
