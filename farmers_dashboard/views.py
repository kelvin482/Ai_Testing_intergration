from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.urls import reverse

from users.permissions import role_required
from users.services import get_or_create_profile


def _build_due_soon_cows():
    return [
        {
            "cow_id": "#C-042",
            "name": "Bessie",
            "detail": "Due in 2 days",
            "status": "Urgent",
            "status_tone": "rose",
        },
        {
            "cow_id": "#C-017",
            "name": "Nasha",
            "detail": "Due in 4 days",
            "status": "Soon",
            "status_tone": "amber",
        },
        {
            "cow_id": "#C-031",
            "name": "Daisy",
            "detail": "Due in 5 days",
            "status": "Soon",
            "status_tone": "amber",
        },
        {
            "cow_id": "#C-009",
            "name": "Rosa",
            "detail": "Due in 7 days",
            "status": "On track",
            "status_tone": "emerald",
        },
    ]


def _build_recent_alert_feed():
    return [
        {
            "title": "#C-042 showing early labour signs",
            "detail": "15 min ago - Vet notified",
            "tone": "rose",
        },
        {
            "title": "#C-017 missed feeding",
            "detail": "2 hrs ago - Check required",
            "tone": "amber",
        },
        {
            "title": "#C-031 weight below target",
            "detail": "Yesterday - Review feeding plan",
            "tone": "amber",
        },
        {
            "title": "Calf #B-011 health check completed",
            "detail": "Yesterday - All clear",
            "tone": "emerald",
        },
    ]


def _build_navigation_sections():
    return [
        {
            "label": "Main",
            "items": [
                {
                    "label": "Overview",
                    "url": reverse("farmers_dashboard:dashboard"),
                    "view_name": "farmers_dashboard:dashboard",
                    "icon": "overview",
                },
                {
                    "label": "My herd",
                    "url": reverse("farmers_dashboard:herd"),
                    "view_name": "farmers_dashboard:herd",
                    "icon": "herd",
                    "badge": str(len(_build_due_soon_cows())),
                },
                {
                    "label": "Alerts",
                    "url": reverse("farmers_dashboard:alerts"),
                    "view_name": "farmers_dashboard:alerts",
                    "icon": "alerts",
                    "badge": str(len(_build_recent_alert_feed())),
                },
            ],
        },
        {
            "label": "Farm",
            "items": [
                {
                    "label": "Reports",
                    "url": reverse("farmers_dashboard:reports"),
                    "view_name": "farmers_dashboard:reports",
                    "icon": "reports",
                },
            ],
        },
    ]


def _build_farmer_workspace_menu_sections():
    return [
        {
            "label": "Workspace",
            "items": [
                {
                    "label": "Profile details",
                    "description": "Review farm and account information.",
                    "url": reverse("users:profile"),
                },
                {
                    "label": "Update farm profile",
                    "description": "Keep the farm contact details ready.",
                    "url": reverse("users:profile_edit"),
                },
            ],
        },
        {
            "label": "Support",
            "items": [
                {
                    "label": "Ask AI",
                    "description": "Open quick guidance when you are stuck.",
                    "url": reverse("cow_calving_ai:index"),
                },
                {
                    "label": "Support hub",
                    "description": "Open escalation help for urgent issues.",
                    "url": reverse("Core_Web:support"),
                },
            ],
        },
    ]


def _build_profile_readiness(user, profile):
    readiness_items = [
        {
            "label": "Display name",
            "value": user.get_full_name() or user.username,
            "is_complete": bool(user.get_full_name() or user.username),
        },
        {
            "label": "Email address",
            "value": user.email or "Add an email address",
            "is_complete": bool(user.email),
        },
        {
            "label": "Farm name",
            "value": profile.farm_name or "Add your farm name",
            "is_complete": bool(profile.farm_name),
        },
        {
            "label": "Phone number",
            "value": profile.phone_number or "Add a phone number",
            "is_complete": bool(profile.phone_number),
        },
    ]
    completed_items = sum(item["is_complete"] for item in readiness_items)
    readiness_percent = int((completed_items / len(readiness_items)) * 100)
    return readiness_items, completed_items, readiness_percent


def _build_farmer_summary_cards(readiness_percent):
    return [
        {
            "label": "Total cows",
            "value": "48",
            "detail": "Active herd ready for daily review.",
            "tone": "sky",
        },
        {
            "label": "Due this week",
            "value": str(len(_build_due_soon_cows())),
            "detail": "Calving checks expected soon.",
            "tone": "amber",
        },
        {
            "label": "Active alerts",
            "value": str(len(_build_recent_alert_feed())),
            "detail": "Items that need attention now.",
            "tone": "rose",
        },
        {
            "label": "Profile ready",
            "value": f"{readiness_percent}%",
            "detail": "Farm essentials saved for this account.",
            "tone": "emerald",
        },
    ]


def _build_farmer_quick_actions():
    return [
        {
            "label": "My herd",
            "detail": "Open animal records and due-soon cows.",
            "url": reverse("farmers_dashboard:herd"),
            "tone": "sky",
        },
        {
            "label": "Reports",
            "detail": "See simple farm trends when needed.",
            "url": reverse("farmers_dashboard:reports"),
            "tone": "emerald",
        },
        {
            "label": "Update profile",
            "detail": "Keep farm contact details ready.",
            "url": reverse("users:profile_edit"),
            "tone": "amber",
        },
    ]


def _build_dashboard_quick_links():
    return [
        {
            "label": "Herd records",
            "description": "Open full animal details, due dates, and follow-up notes.",
            "url": reverse("farmers_dashboard:herd"),
        },
        {
            "label": "Reports",
            "description": "See trends only when you need a deeper farm summary.",
            "url": reverse("farmers_dashboard:reports"),
        },
        {
            "label": "Ask AI",
            "description": "Use quick guidance to unblock the next farm action.",
            "url": reverse("cow_calving_ai:index"),
        },
    ]


def _build_herd_preview_cards():
    return [
        {
            "name": "Bella 004",
            "breed": "Friesian",
            "status": "Milking well",
            "status_tone": "emerald",
            "detail": "Latest yield placeholder: 18.4 L",
            "supporting_text": "Use this card pattern for daily production, notes, and next checks.",
        },
        {
            "name": "Daisy 007",
            "breed": "Sahiwal",
            "status": "Due soon",
            "status_tone": "amber",
            "detail": "Expected calving placeholder: 26 Mar",
            "supporting_text": "Reserve this surface for calving watch, checklists, and vet follow-up.",
        },
        {
            "name": "Rosa 011",
            "breed": "Ayrshire",
            "status": "Needs review",
            "status_tone": "rose",
            "detail": "Alert placeholder: labour monitoring",
            "supporting_text": "This slot can highlight urgent cases without mixing them into every page.",
        },
        {
            "name": "Mable 022",
            "breed": "Jersey",
            "status": "Breeding plan",
            "status_tone": "sky",
            "detail": "Follow-up placeholder: insemination history",
            "supporting_text": "Keep breeding entries separated from milk logs for easier scanning.",
        },
    ]


def _build_alert_preview_cards():
    return [
        {
            "level": "Urgent",
            "title": "Calving monitor needs fast follow-up",
            "detail": "Use a high-emphasis alert card here for labour progress, time checks, and next actions.",
            "action_label": "Open support guidance",
            "action_url": reverse("Core_Web:support"),
            "tone": "rose",
        },
        {
            "level": "Attention",
            "title": "Production change review",
            "detail": "This card style works for milk-drop investigations, mastitis screening, or feeding checks.",
            "action_label": "Open reports page",
            "action_url": reverse("farmers_dashboard:reports"),
            "tone": "amber",
        },
        {
            "level": "Planned",
            "title": "Vaccination reminder slot",
            "detail": "Keep lower-pressure reminders visible without giving them the same weight as urgent items.",
            "action_label": "Ask the AI workspace",
            "action_url": reverse("cow_calving_ai:index"),
            "tone": "emerald",
        },
    ]


def _build_report_highlights():
    return [
        {
            "label": "Milk trend",
            "value": "Layout ready",
            "detail": "Weekly and monthly charts can live in one reporting surface.",
        },
        {
            "label": "Herd ranking",
            "value": "Top performers",
            "detail": "Leaderboards help farmers spot the strongest animals quickly.",
        },
        {
            "label": "Breeding view",
            "value": "Summary cards",
            "detail": "Conception and expected-calving indicators belong here, not on the home page.",
        },
    ]


def _build_report_bars():
    return [
        {"label": "Mon", "height_class": "h-24"},
        {"label": "Tue", "height_class": "h-28"},
        {"label": "Wed", "height_class": "h-20"},
        {"label": "Thu", "height_class": "h-32"},
        {"label": "Fri", "height_class": "h-36"},
        {"label": "Sat", "height_class": "h-28"},
        {"label": "Sun", "height_class": "h-40"},
    ]


def _build_report_leaderboard():
    return [
        {"name": "Bella 004", "detail": "Friesian | Milking", "value": "19.2 L"},
        {"name": "Daisy 007", "detail": "Sahiwal | Due soon", "value": "18.5 L"},
        {"name": "Cleo 003", "detail": "Ayrshire | Milking", "value": "16.0 L"},
    ]


def _build_farmer_dashboard_context(
    request,
    *,
    page_title,
    page_eyebrow,
    page_heading,
    page_intro,
):
    profile = get_or_create_profile(request.user)
    display_name = request.user.get_full_name().strip() or request.user.username
    first_name = request.user.first_name.strip() if request.user.first_name else display_name.split()[0]
    initials = "".join(part[0].upper() for part in display_name.split()[:2] if part) or "FM"
    readiness_items, completed_items, readiness_percent = _build_profile_readiness(
        request.user,
        profile,
    )
    return {
        "dashboard_home_url": reverse("farmers_dashboard:dashboard"),
        "back_to_website_url": reverse("Core_Web:home"),
        "ai_workspace_url": reverse("cow_calving_ai:index"),
        "ai_workspace_embed_url": f"{reverse('cow_calving_ai:index')}?embedded=1",
        "profile": profile,
        "display_name": display_name,
        "farmer_initials": initials,
        "dashboard_greeting": f"good morning, {first_name}",
        "page_title": page_title,
        "page_eyebrow": page_eyebrow,
        "page_heading": page_heading,
        "page_intro": page_intro,
        "navigation_sections": _build_navigation_sections(),
        "workspace_menu_sections": _build_farmer_workspace_menu_sections(),
        "summary_cards": _build_farmer_summary_cards(readiness_percent),
        "due_soon_cows": _build_due_soon_cows(),
        "recent_alert_feed": _build_recent_alert_feed(),
        "farmer_quick_actions": _build_farmer_quick_actions(),
        "dashboard_quick_links": _build_dashboard_quick_links(),
        "profile_readiness_items": readiness_items,
        "profile_readiness_percent": readiness_percent,
        "herd_preview_cards": _build_herd_preview_cards(),
        "alert_preview_cards": _build_alert_preview_cards(),
        "report_highlights": _build_report_highlights(),
        "report_bars": _build_report_bars(),
        "report_leaderboard": _build_report_leaderboard(),
        "header_primary_action": {
            "label": "Open alerts",
            "url": reverse("farmers_dashboard:alerts"),
        },
    }


@login_required
@role_required("farmer")
def dashboard_view(request):
    return render(
        request,
        "farmers_dashboard/dashboard.html",
        _build_farmer_dashboard_context(
            request,
            page_title="Farmer Dashboard | CowCalving",
            page_eyebrow="Farmer workspace",
            page_heading="Daily farm overview",
            page_intro="See what needs attention now, then open herd, alerts, or reports only when you need more detail.",
        ),
    )


@login_required
@role_required("farmer")
def herd_view(request):
    return render(
        request,
        "farmers_dashboard/herd.html",
        _build_farmer_dashboard_context(
            request,
            page_title="Herd Workspace | CowCalving",
            page_eyebrow="Herd records",
            page_heading="Organize animal information in one clear place",
            page_intro=(
                "This page gives the farmer app a dedicated herd records "
                "surface so future cow profiles, production logs, and "
                "breeding history do not all compete on the dashboard home."
            ),
        ),
    )


@login_required
@role_required("farmer")
def alerts_view(request):
    return render(
        request,
        "farmers_dashboard/alerts.html",
        _build_farmer_dashboard_context(
            request,
            page_title="Farmer Alerts | CowCalving",
            page_eyebrow="Alerts center",
            page_heading="Keep urgent actions visible and separated",
            page_intro=(
                "Alerts now live on their own page, which leaves the overview "
                "lighter and gives urgent cases a more intentional layout."
            ),
        ),
    )


@login_required
@role_required("farmer")
def reports_view(request):
    return render(
        request,
        "farmers_dashboard/reports.html",
        _build_farmer_dashboard_context(
            request,
            page_title="Farmer Reports | CowCalving",
            page_eyebrow="Reports and trends",
            page_heading="Present farm performance in a professional way",
            page_intro=(
                "The reports page now gives trend charts, rankings, and "
                "summary cards their own dedicated home instead of crowding "
                "the main dashboard."
            ),
        ),
    )
