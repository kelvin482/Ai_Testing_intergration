import calendar
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.urls import reverse
from django.utils import timezone

from users.permissions import role_required
from users.services import get_dashboard_url_for_user, get_or_create_profile


def _build_navigation_sections():
    urgent_case_count = sum(
        1 for item in _build_patient_records() if item["tone"] == "rose"
    )
    return [
        {
            "label": "Main",
            "items": [
                {
                    "label": "Overview",
                    "url": reverse("veterinary_dashboard:dashboard"),
                    "view_name": "veterinary_dashboard:dashboard",
                    "icon": "overview",
                },
                {
                    "label": "Active Case",
                    "url": reverse("veterinary_dashboard:patients"),
                    "view_name": "veterinary_dashboard:patients",
                    "icon": "case",
                    "badge": str(urgent_case_count),
                },
                {
                    "label": "Farm Map",
                    "url": reverse("veterinary_dashboard:farm_map"),
                    "view_name": "veterinary_dashboard:farm_map",
                    "icon": "map",
                },
            ],
        },
        {
            "label": "Farms",
            "items": [
                {
                    "label": "My Farms",
                    "url": reverse("veterinary_dashboard:farms"),
                    "view_name": "veterinary_dashboard:farms",
                    "icon": "farms",
                    "badge": str(len(_build_farm_overview())),
                },
                {
                    "label": "Medical Records",
                    "url": reverse("veterinary_dashboard:medical_records"),
                    "view_name": "veterinary_dashboard:medical_records",
                    "icon": "records",
                },
            ],
        },
    ]


def _build_workspace_menu():
    return [
        {
            "label": "Account",
            "items": [
                {"label": "Overview", "description": "Return to the main command center.", "url": reverse("veterinary_dashboard:dashboard")},
                {"label": "My Profile", "description": "Review saved account details.", "url": reverse("users:profile")},
                {"label": "Edit Profile", "description": "Update account information.", "url": reverse("users:profile_edit")},
            ],
        },
        {
            "label": "Workspace",
            "items": [
                {"label": "Schedule", "description": "Open today's route planner.", "url": reverse("veterinary_dashboard:schedule")},
                {"label": "AI Workspace", "description": "Open guided support.", "url": reverse("cow_calving_ai:index")},
            ],
        },
    ]


def _build_summary_cards():
    overview_cases = _build_overview_case_rows()
    schedule_rows = _build_overview_schedule_rows()
    return [
        {
            "label": "Active cases",
            "value": str(len(overview_cases)),
            "detail": "Open patient files",
            "tone": "rose",
        },
        {
            "label": "Today's visits",
            "value": str(len(schedule_rows)),
            "detail": "Scheduled for today",
            "tone": "navy",
        },
        {
            "label": "Urgent now",
            "value": str(sum(1 for item in overview_cases if item["tone"] == "rose")),
            "detail": "Need immediate review",
            "tone": "amber",
        },
    ]


def _build_visit_cards():
    return [
        {"time": "08:00", "title": "Moi Farm - John Otieno", "detail": "Rosa #011 - labour complications - Kisii", "status": "Urgent", "tag": "Calving", "tone": "rose"},
        {"time": "10:30", "title": "Green Acres - Mary Wanjiku", "detail": "Herd vaccination - FMD booster - 8 cows", "status": "Scheduled", "tag": "Vaccination", "tone": "teal"},
        {"time": "14:00", "title": "Sunrise Dairy - Peter Kamau", "detail": "Daisy #003 - suspected mastitis - milk drop 30%", "status": "Pending", "tag": "Health check", "tone": "amber"},
    ]


def _build_priority_actions():
    return [
        {"title": "Urgent case", "detail": "Rosa #011 needs labour follow-up before 09:00.", "meta": "Telehealth ready", "tone": "rose"},
        {"title": "Lab review queue", "detail": "CBC and mastitis panels are ready for sign-off.", "meta": "3 pending", "tone": "navy"},
        {"title": "Prescription renewal", "detail": "Bella #004 requires treatment review today.", "meta": "Withholding note", "tone": "teal"},
    ]


def _build_farm_overview():
    return [
        {"name": "Moi Farm", "detail": "24 cows - 2 active alerts - Kisii", "risk": "High risk", "risk_percent": 86, "tone": "rose"},
        {"name": "Sunrise Dairy", "detail": "31 cows - mastitis review pending - Kericho", "risk": "Medium risk", "risk_percent": 58, "tone": "amber"},
        {"name": "Green Acres", "detail": "18 cows - vaccination plan on track - Nakuru", "risk": "Low risk", "risk_percent": 18, "tone": "teal"},
    ]


def _build_analytics_bars():
    return [
        {"label": "Mastitis", "value": "4 cases", "width": "80%", "tone": "rose"},
        {"label": "Difficult calving", "value": "2 cases", "width": "46%", "tone": "amber"},
        {"label": "Tick-borne fever", "value": "1 case", "width": "24%", "tone": "navy"},
    ]


def _build_lab_panels():
    return [
        {"title": "Complete blood count", "detail": "Nuru #025 - elevated WBC and low haematocrit need review.", "status": "Review first"},
        {"title": "Milk quality panel", "detail": "Rear-left quarter CMT is positive and SCC is above threshold.", "status": "Share after sign-off"},
    ]


def _build_case_snapshots():
    return [
        {"title": "Rosa #011", "detail": "Active labour case with escalation already in telehealth.", "status": "Open case", "tone": "rose"},
        {"title": "Bella #004", "detail": "Treatment course ends today and needs prescription review.", "status": "Rx follow-up", "tone": "amber"},
        {"title": "Nuru #025", "detail": "Lab interpretation is pending before farmer sharing.", "status": "Awaiting sign-off", "tone": "navy"},
    ]


def _build_patient_records():
    return [
        {
            "id": "rosa-011",
            "name": "Rosa #011",
            "farm": "Moi Farm",
            "owner": "John Otieno",
            "location": "Kisii",
            "breed": "Ayrshire",
            "tag_number": "011",
            "status": "Open case",
            "tone": "rose",
            "issue": "Labour follow-up",
            "summary": "Active labour case with escalation already in telehealth.",
            "status_banner": "Labour in progress",
            "next_step": "Visit first and record delivery outcome.",
            "last_update": "08:04 today",
            "care_stages": ["Pre-calving", "Early labour", "Active labour", "Delivery", "Post-calving"],
            "current_stage": 2,
            "medical_note": "Cow presented BCS 2.8 at the last check. Monitor for dystocia risk and move quickly if contractions stall.",
            "medications": ["Oxytocin 10 IU", "Calcium borogluconate", "Lubricant gel", "Dystocia kit"],
            "ai_recommendation": "AI recommends maintaining close labour monitoring and escalating to assisted delivery if progress stalls after the next check-in.",
            "stats": [
                {"label": "Age", "value": "5 yr"},
                {"label": "Weight", "value": "390 kg"},
                {"label": "Parity", "value": "P3"},
                {"label": "Temp", "value": "39.2 C"},
            ],
            "history": [
                {"date": "09:12", "title": "Labour signs reported by farmer", "detail": "James Mwangi submitted an alert from the farm app."},
                {"date": "09:18", "title": "Vet acknowledged and reviewed remotely", "detail": "Remote assessment started after the escalation came through telehealth."},
                {"date": "09:45", "title": "Video call confirmed contractions", "detail": "Contractions reported every 8 minutes and farmer advised to prepare the pen."},
                {"date": "10:20", "title": "On-site follow-up arranged", "detail": "Field visit is underway with the labour kit ready."},
            ],
            "primary_url": reverse("veterinary_dashboard:diagnosis"),
            "primary_label": "Log update",
            "secondary_url": reverse("veterinary_dashboard:telehealth"),
            "secondary_label": "Call farmer",
            "extra_url": reverse("veterinary_dashboard:schedule"),
            "extra_label": "Open route",
        },
        {
            "id": "bella-004",
            "name": "Bella #004",
            "farm": "Moi Farm",
            "owner": "John Otieno",
            "location": "Kisii",
            "breed": "Friesian",
            "tag_number": "004",
            "status": "Rx follow-up",
            "tone": "amber",
            "issue": "Treatment renewal",
            "summary": "Treatment course ends today and needs prescription review.",
            "status_banner": "Treatment review due",
            "next_step": "Review medication and renew only if symptoms persist.",
            "last_update": "09:10 today",
            "care_stages": ["Reported", "Assessment", "Treatment", "Follow-up", "Closed"],
            "current_stage": 3,
            "medical_note": "Treatment is ending today. Review hydration, appetite, and udder status before renewing the prescription.",
            "medications": ["Oxytetracycline", "NSAID", "Milk withholding card"],
            "ai_recommendation": "AI recommends confirming symptom persistence before issuing a renewal and documenting withholding guidance for the farmer.",
            "stats": [
                {"label": "Age", "value": "4 yr"},
                {"label": "Weight", "value": "420 kg"},
                {"label": "Milk", "value": "16 L"},
                {"label": "Course", "value": "Ends today"},
            ],
            "history": [
                {"date": "18 Mar", "title": "Course review due", "detail": "Farmer reminded that current treatment finishes today."},
                {"date": "12 Mar", "title": "Initial diagnosis", "detail": "Clinical note recorded with antibiotic treatment plan."},
                {"date": "07 Jan", "title": "Routine check", "detail": "No active concerns recorded during herd review."},
            ],
            "primary_url": reverse("veterinary_dashboard:prescriptions"),
            "primary_label": "Open Rx",
            "secondary_url": reverse("veterinary_dashboard:diagnosis"),
            "secondary_label": "Open diagnosis",
            "extra_url": reverse("veterinary_dashboard:telehealth"),
            "extra_label": "Message farmer",
        },
        {
            "id": "nuru-025",
            "name": "Nuru #025",
            "farm": "Moi Farm",
            "owner": "John Otieno",
            "location": "Kisii",
            "breed": "Jersey cross",
            "tag_number": "025",
            "status": "Awaiting sign-off",
            "tone": "navy",
            "issue": "Lab interpretation",
            "summary": "Lab interpretation is pending before farmer sharing.",
            "status_banner": "Lab review pending",
            "next_step": "Review CBC and milk panel before sending advice.",
            "last_update": "11:00 today",
            "care_stages": ["Sample sent", "Lab ready", "Review", "Share guidance", "Closed"],
            "current_stage": 2,
            "medical_note": "Elevated WBC and high SCC need veterinary interpretation before the farmer acts on the result.",
            "medications": ["CMT strips", "CBC panel", "Milk panel summary"],
            "ai_recommendation": "AI recommends linking the lab result to the active case note before issuing treatment guidance.",
            "stats": [
                {"label": "Age", "value": "3 yr"},
                {"label": "Weight", "value": "350 kg"},
                {"label": "WBC", "value": "14.8"},
                {"label": "SCC", "value": "450k"},
            ],
            "history": [
                {"date": "20 Mar", "title": "CBC ready", "detail": "Elevated WBC and low haematocrit flagged for veterinary review."},
                {"date": "19 Mar", "title": "Milk panel", "detail": "Rear-left quarter CMT positive with high SCC."},
                {"date": "02 Feb", "title": "Routine milk check", "detail": "Previous milk quality panel returned within range."},
            ],
            "primary_url": reverse("veterinary_dashboard:labs"),
            "primary_label": "Open labs",
            "secondary_url": reverse("veterinary_dashboard:diagnosis"),
            "secondary_label": "Add findings",
            "extra_url": reverse("veterinary_dashboard:telehealth"),
            "extra_label": "Share later",
        },
        {
            "id": "daisy-003",
            "name": "Daisy #003",
            "farm": "Sunrise Dairy",
            "owner": "Peter Kamau",
            "location": "Kericho",
            "breed": "Friesian",
            "tag_number": "003",
            "status": "Pending visit",
            "tone": "amber",
            "issue": "Suspected mastitis",
            "summary": "Symptoms logged ahead of the afternoon visit with milk drop reported.",
            "status_banner": "Visit pending",
            "next_step": "Confirm mastitis signs during the 14:00 health check.",
            "last_update": "11:40 today",
            "care_stages": ["Reported", "Remote triage", "Visit scheduled", "Treatment", "Recovery"],
            "current_stage": 2,
            "medical_note": "Farmer reported milk drop and tenderness. Confirm quarter involvement and rule out fever on site.",
            "medications": ["CMT kit", "Thermometer", "Intramammary tube"],
            "ai_recommendation": "AI recommends confirming mastitis severity during the visit before choosing between local treatment and full escalation.",
            "stats": [
                {"label": "Age", "value": "6 yr"},
                {"label": "Weight", "value": "410 kg"},
                {"label": "Milk", "value": "-30%"},
                {"label": "Visit", "value": "14:00"},
            ],
            "history": [
                {"date": "20 Mar", "title": "Telehealth note", "detail": "Farmer logged mastitis symptoms before field visit."},
                {"date": "15 Jan", "title": "Herd review", "detail": "Routine check completed with no treatment required."},
                {"date": "04 Oct", "title": "Vaccination", "detail": "Scheduled herd vaccination completed."},
            ],
            "primary_url": reverse("veterinary_dashboard:schedule"),
            "primary_label": "Open schedule",
            "secondary_url": reverse("veterinary_dashboard:telehealth"),
            "secondary_label": "Open telehealth",
            "extra_url": reverse("veterinary_dashboard:labs"),
            "extra_label": "Review labs",
        },
    ]


def _build_prescription_notes():
    return [
        {"title": "Milk withholding warning", "detail": "Keep withholding guidance visible on every treatment summary before sending to the farmer.", "status": "Safety first", "tone": "amber"},
        {"title": "Dose validation", "detail": "Check weight-based dosing from the patient file before issuing or renewing Rx.", "status": "Clinical check", "tone": "navy"},
        {"title": "Renewal reminders", "detail": "Group ending courses into one follow-up list instead of scattering them across pages.", "status": "Workflow", "tone": "teal"},
    ]


def _build_telehealth_updates():
    return [
        {"farmer": "John Otieno", "message": "Labour case update received with photo evidence.", "time": "08:04"},
        {"farmer": "Mary Wanjiku", "message": "Vaccination visit confirmed for the 10:30 slot.", "time": "09:12"},
        {"farmer": "Peter Kamau", "message": "Mastitis symptoms logged ahead of the afternoon visit.", "time": "11:40"},
    ]


def _build_schedule_planner():
    # Keep the hackathon schedule flow simple and demo-friendly: one visible
    # month, a selected day, and a small set of realistic visit records.
    year = 2026
    month = 3
    selected_day = 20

    visits_by_day = {
        20: [
            {
                "id": "moi-labour",
                "time": "08:00",
                "farm": "Moi Farm",
                "farmer": "John Otieno",
                "animal": "Rosa #011",
                "type": "Labour follow-up",
                "detail": "Labour complications - Kisii",
                "status": "Urgent",
                "tone": "rose",
                "primary_url": reverse("veterinary_dashboard:telehealth"),
                "primary_label": "Open telehealth",
                "secondary_url": reverse("veterinary_dashboard:patients"),
                "secondary_label": "Open case",
            },
            {
                "id": "green-acres-vax",
                "time": "10:30",
                "farm": "Green Acres",
                "farmer": "Mary Wanjiku",
                "animal": "Herd visit",
                "type": "Vaccination",
                "detail": "FMD booster - 8 cows",
                "status": "Scheduled",
                "tone": "emerald",
                "primary_url": reverse("veterinary_dashboard:patients"),
                "primary_label": "Open patients",
                "secondary_url": reverse("veterinary_dashboard:diagnosis"),
                "secondary_label": "Add note",
            },
            {
                "id": "sunrise-mastitis",
                "time": "14:00",
                "farm": "Sunrise Dairy",
                "farmer": "Peter Kamau",
                "animal": "Daisy #003",
                "type": "Health check",
                "detail": "Suspected mastitis - milk drop 30%",
                "status": "Pending",
                "tone": "amber",
                "primary_url": reverse("veterinary_dashboard:patients"),
                "primary_label": "Open patient",
                "secondary_url": reverse("veterinary_dashboard:labs"),
                "secondary_label": "Open labs",
            },
        ],
        21: [
            {
                "id": "baraka-route",
                "time": "09:15",
                "farm": "Baraka Ranch",
                "farmer": "Samuel Kipchoge",
                "animal": "Herd visit",
                "type": "Routine check",
                "detail": "Quarterly herd health check",
                "status": "Scheduled",
                "tone": "emerald",
                "primary_url": reverse("veterinary_dashboard:farms"),
                "primary_label": "Open farm",
                "secondary_url": reverse("veterinary_dashboard:patients"),
                "secondary_label": "Open files",
            }
        ],
        24: [
            {
                "id": "nuru-lab-review",
                "time": "11:00",
                "farm": "Moi Farm",
                "farmer": "John Otieno",
                "animal": "Nuru #025",
                "type": "Lab review",
                "detail": "CBC and mastitis panel sign-off",
                "status": "Review",
                "tone": "navy",
                "primary_url": reverse("veterinary_dashboard:labs"),
                "primary_label": "Review labs",
                "secondary_url": reverse("veterinary_dashboard:patients"),
                "secondary_label": "Open patient",
            }
        ],
        26: [
            {
                "id": "ngugi-follow-up",
                "time": "15:30",
                "farm": "Ngugi Family Farm",
                "farmer": "Grace Ngugi",
                "animal": "Vaccination drive",
                "type": "Follow-up",
                "detail": "3 cows overdue for vaccination",
                "status": "Pending",
                "tone": "amber",
                "primary_url": reverse("veterinary_dashboard:farms"),
                "primary_label": "Open farms",
                "secondary_url": reverse("veterinary_dashboard:telehealth"),
                "secondary_label": "Message farmer",
            }
        ],
    }

    month_weeks = calendar.Calendar(firstweekday=0).monthdayscalendar(year, month)
    calendar_days = []
    for week in month_weeks:
        for day in week:
            if day == 0:
                calendar_days.append({"empty": True})
                continue

            visits = visits_by_day.get(day, [])
            tones = {item["tone"] for item in visits}
            calendar_days.append(
                {
                    "day": day,
                    "empty": False,
                    "selected": day == selected_day,
                    "visit_count": len(visits),
                    "has_urgent": "rose" in tones,
                    "has_items": bool(visits),
                }
            )

    selected_visits = visits_by_day[selected_day]
    total_planned_days = len([day for day, items in visits_by_day.items() if items])
    total_urgent_visits = sum(
        1
        for items in visits_by_day.values()
        for item in items
        if item["tone"] == "rose"
    )
    return {
        "month_label": f"{calendar.month_name[month]} {year}",
        "weekday_labels": ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"],
        "calendar_days": calendar_days,
        "selected_day": selected_day,
        "selected_date_label": "Friday, 20 March 2026",
        "selected_day_summary": "3 visits planned, 1 urgent case, 1 follow-up pending.",
        "schedule_seed_items": visits_by_day,
        "schedule_initial_items": selected_visits,
        "planner_stats": [
            {"label": "Planned days", "value": str(total_planned_days)},
            {"label": "Urgent visits", "value": str(total_urgent_visits)},
            {"label": "Assigned farms", "value": "4"},
        ],
        "planner_help": [
            "Pick a date on the calendar to review that day's route.",
            "Use Add visit to draft a new assignment in this browser for the demo.",
            "Open the linked patient, lab, or telehealth page only when needed.",
        ],
    }


def _build_dashboard_greeting() -> str:
    hour = timezone.localtime().hour
    if hour < 12:
        return "good morning"
    if hour < 18:
        return "good afternoon"
    return "good evening"


def _build_overview_case_rows():
    case_flags = {
        "rose": "Respond now",
        "amber": "Monitor",
        "navy": "Review",
    }
    rows = []
    for record in _build_patient_records():
        rows.append(
            {
                "code": f"#C-{record['tag_number']}",
                "detail": f"{record['farm']} · {record['issue']}",
                "flag": case_flags.get(record["tone"], record["status"]),
                "tone": record["tone"],
            }
        )
    return rows


def _build_dashboard_farm_cards():
    farm_flags = {
        "rose": "2 urgent",
        "amber": "Monitoring",
        "teal": "Stable",
    }
    cards = []
    for farm in _build_farm_overview():
        words = farm["name"].replace("-", " ").split()
        initials = "".join(word[0].upper() for word in words[:2] if word) or "FM"
        cards.append(
            {
                "name": farm["name"],
                "detail": farm["detail"],
                "flag": farm_flags.get(farm["tone"], farm["risk"]),
                "initials": initials,
                "tone": farm["tone"],
            }
        )
    return cards


def _build_overview_schedule_rows():
    return [
        {
            "time": "08:00",
            "farm": "Moi Farm",
            "visit_type": "Pre-calving check",
            "detail": "Cow #C-055",
        },
        {
            "time": "10:30",
            "farm": "Green Acres",
            "visit_type": "Vaccination run",
            "detail": "8 cows",
        },
        {
            "time": "14:00",
            "farm": "Moi Farm",
            "visit_type": "Follow-up check",
            "detail": "Calf #B-009",
        },
    ]


def _build_dashboard_quick_links():
    return [
        {
            "label": "Open farm map",
            "description": "Check the region visually when routing needs more context than the overview shows.",
            "url": reverse("veterinary_dashboard:farm_map"),
        },
        {
            "label": "My farms",
            "description": "Review assigned farms only when you need counts, alerts, and due-soon work.",
            "url": reverse("veterinary_dashboard:farms"),
        },
        {
            "label": "Medical records",
            "description": "Open treatment history and recent lab summaries without crowding the homepage.",
            "url": reverse("veterinary_dashboard:medical_records"),
        },
    ]


def _build_farm_map_context():
    return {
        "region_label": "Nakuru region",
        "vet_status_label": "Dr. Njenga en route",
        "legend_items": [
            {"label": "Urgent cases", "tone": "rose"},
            {"label": "Needs monitoring", "tone": "amber"},
            {"label": "All clear", "tone": "teal"},
            {"label": "Vet location", "tone": "navy"},
        ],
        "map_markers": [
            {"label": "MW", "name": "Mwangi", "status": "2 urgent", "tone": "rose", "top": "24%", "left": "43%"},
            {"label": "KM", "name": "Kamau", "status": "monitor", "tone": "amber", "top": "32%", "left": "70%"},
            {"label": "MK", "name": "Mutuku", "status": "all clear", "tone": "teal", "top": "27%", "left": "88%"},
            {"label": "VT", "name": "Dr. Njenga", "status": "en route", "tone": "navy", "top": "46%", "left": "53%"},
            {"label": "NG", "name": "Ngugi", "status": "all clear", "tone": "teal", "top": "62%", "left": "34%"},
            {"label": "WN", "name": "Wanjiku", "status": "all clear", "tone": "teal", "top": "74%", "left": "57%"},
            {"label": "OD", "name": "Odhiambo", "status": "overdue", "tone": "amber", "top": "60%", "left": "80%"},
        ],
        "status_cards": [
            {"name": "Mwangi Farm", "cows": "22", "due_soon": "6", "alerts": "3 active", "badge": "2 urgent", "tone": "rose"},
            {"name": "Kamau Farm", "cows": "15", "due_soon": "2", "alerts": "1 active", "badge": "Monitoring", "tone": "amber"},
            {"name": "Odhiambo Farm", "cows": "18", "due_soon": "3", "alerts": "1 active", "badge": "Overdue case", "tone": "amber"},
            {"name": "Ngugi Farm", "cows": "11", "due_soon": "0", "alerts": "None", "badge": "All clear", "tone": "teal"},
        ],
    }


def _build_medical_record_cards():
    return [
        {"title": "Rosa #011", "detail": "Labour follow-up timeline, intervention summary, and escalation notes.", "status": "Open case", "tone": "rose"},
        {"title": "Bella #004", "detail": "Treatment renewal review with withholding guidance recorded.", "status": "Follow-up", "tone": "amber"},
        {"title": "Nuru #025", "detail": "CBC and milk panel results waiting for sign-off and farmer sharing.", "status": "Lab linked", "tone": "navy"},
    ]


def _build_common_context(request, *, page_title, page_eyebrow, page_heading, page_intro):
    profile = get_or_create_profile(request.user)
    display_name = request.user.get_full_name().strip() or request.user.username
    initials = "".join(part[0].upper() for part in display_name.split()[:2] if part) or "VT"
    return {
        "dashboard_home_url": get_dashboard_url_for_user(request.user, fallback="/dashboard/profile/"),
        "back_to_website_url": reverse("Core_Web:home"),
        "ai_workspace_url": reverse("cow_calving_ai:index"),
        "ai_workspace_embed_url": f"{reverse('cow_calving_ai:index')}?embedded=1",
        "profile": profile,
        "display_name": display_name,
        "vet_initials": initials,
        "professional_id_display": profile.professional_id or "KE-VET-4921",
        "dashboard_greeting": _build_dashboard_greeting(),
        "page_title": page_title,
        "page_eyebrow": page_eyebrow,
        "page_heading": page_heading,
        "page_intro": page_intro,
        "navigation_sections": _build_navigation_sections(),
        "workspace_menu_sections": _build_workspace_menu(),
        "header_primary_action": {
            "label": "New case update",
            "url": reverse("veterinary_dashboard:patients"),
        },
    }


def _build_workspace_page_context(request, *, page_title, page_eyebrow, page_heading, page_intro, page_focus, page_quick_actions, main_section, support_section, extra_section):
    context = _build_common_context(
        request,
        page_title=page_title,
        page_eyebrow=page_eyebrow,
        page_heading=page_heading,
        page_intro=page_intro,
    )
    context.update(
        {
            "page_focus": page_focus,
            "page_quick_actions": page_quick_actions,
            "main_section": main_section,
            "support_section": support_section,
            "extra_section": extra_section,
        }
    )
    return context


@login_required
@role_required("veterinary")
def dashboard_view(request):
    context = _build_common_context(
        request,
        page_title="Veterinary Dashboard | CowCalving",
        page_eyebrow="Clinical operations",
        page_heading="Veterinary Dashboard",
        page_intro="Track urgent work, today's visits, and pending reviews.",
    )
    context.update(
        {
            "summary_cards": _build_summary_cards(),
            "overview_schedule_rows": _build_overview_schedule_rows(),
            # Keep the overview data intentionally compact so the dashboard
            # stays close to the shared mockup and leaves deeper workflows for
            # dedicated pages like patients, schedule, and farms.
            "overview_case_rows": _build_overview_case_rows(),
            "dashboard_quick_links": _build_dashboard_quick_links(),
        }
    )
    return render(request, "veterinary_dashboard/dashboard.html", context)


@login_required
@role_required("veterinary")
def schedule_view(request):
    context = _build_common_context(
        request,
        page_title="Veterinary Schedule | CowCalving",
        page_eyebrow="Schedule",
        page_heading="Plan the day clearly",
        page_intro="Use one simple planner for visits, follow-up, and route order.",
    )
    context.update(_build_schedule_planner())
    return render(request, "veterinary_dashboard/schedule.html", context)


@login_required
@role_required("veterinary")
def farms_view(request):
    farm_cards = [{"title": farm["name"], "detail": farm["detail"], "status": farm["risk"], "tone": farm["tone"], "progress_width": f"{farm['risk_percent']}%"} for farm in _build_farm_overview()]
    return render(
        request,
        "veterinary_dashboard/workspace_page.html",
        _build_workspace_page_context(
            request,
            page_title="Veterinary Farms | CowCalving",
            page_eyebrow="My farms",
            page_heading="Manage assigned farms",
            page_intro="Keep the farm list short, scannable, and ready for a quick open when a route decision matters.",
            page_focus={"label": "My Farms", "title": "See farm risk clearly", "text": "This page keeps farm counts, due-soon work, and alert level in one controlled list.", "badges": ["Assigned only", "Risk first", "Open details when needed"]},
            page_quick_actions=[
                {"label": "Open farm map", "description": "Switch to the region view when routing matters more than the list.", "url": reverse("veterinary_dashboard:farm_map")},
                {"label": "Open schedule", "description": "Compare farm risk with today's visits.", "url": reverse("veterinary_dashboard:schedule")},
                {"label": "Open active case", "description": "Jump into the case that needs action next.", "url": reverse("veterinary_dashboard:patients")},
            ],
            main_section={"label": "Assigned farms", "title": "Farm list and alert level", "cards": farm_cards},
            support_section={"label": "Design rule", "title": "Why farms should be separate", "cards": [
                {"title": "Avoid duplicate context", "detail": "Farm location, alerts, and counts are easier to read once here than on every page.", "status": "Lower cognitive load", "tone": "navy"},
                {"title": "Support routing decisions", "detail": "Pair this page with the farm map or schedule instead of crowding the overview.", "status": "Better planning", "tone": "teal"},
                {"title": "Hackathon-ready scope", "detail": "The list stays compact now and can expand into notes or coverage history later.", "status": "Expandable", "tone": "amber"},
            ]},
            extra_section={"label": "Connected workflows", "title": "Pages that use this farm context", "cards": [
                {"title": "Active Case", "detail": "Open the current cow case after choosing the farm context.", "url": reverse("veterinary_dashboard:patients")},
                {"title": "Farm Map", "detail": "Switch to the region view for route and urgency context.", "url": reverse("veterinary_dashboard:farm_map")},
                {"title": "Medical Records", "detail": "Review recent farm-linked treatment and lab history.", "url": reverse("veterinary_dashboard:medical_records")},
            ]},
        ),
    )


@login_required
@role_required("veterinary")
def patients_view(request):
    patient_records = _build_patient_records()
    context = _build_common_context(
        request,
        page_title="Veterinary Active Case | CowCalving",
        page_eyebrow="Active case",
        page_heading="Work from one active case at a time",
        page_intro="Keep the case queue short, open one animal, and make the next action obvious for the vet.",
    )
    context.update(
        {
            "patient_records": patient_records,
            "patient_stats": [
                {"label": "Open cases", "value": "4"},
                {"label": "Need review", "value": "2"},
                {"label": "Lab linked", "value": "1"},
            ],
            "patient_page_notes": [
                "Open one case, act, then come back for the next one.",
                "Keep telehealth, diagnosis, and routing behind action buttons so the page stays controlled.",
                "Save a short local note first, then move to the next workflow only if needed.",
            ],
            "patient_seed_record": patient_records[0],
        }
    )
    return render(request, "veterinary_dashboard/patients.html", context)


@login_required
@role_required("veterinary")
def farm_map_view(request):
    context = _build_common_context(
        request,
        page_title="Veterinary Farm Map | CowCalving",
        page_eyebrow="Farm map",
        page_heading="Read the region at a glance",
        page_intro="Use the map only when the route or farm priority needs a wider view than the overview can show.",
    )
    context.update(_build_farm_map_context())
    return render(request, "veterinary_dashboard/farm_map.html", context)


@login_required
@role_required("veterinary")
def medical_records_view(request):
    record_cards = _build_medical_record_cards()
    return render(
        request,
        "veterinary_dashboard/workspace_page.html",
        _build_workspace_page_context(
            request,
            page_title="Veterinary Medical Records | CowCalving",
            page_eyebrow="Medical records",
            page_heading="Review concise case history",
            page_intro="Keep treatment history, lab summaries, and recent case notes accessible without crowding the live workflow pages.",
            page_focus={"label": "Medical Records", "title": "Review what happened before acting", "text": "This page is for recent records and continuity, not day-of triage.", "badges": ["History first", "Search next", "Controlled access"]},
            page_quick_actions=[
                {"label": "Open active case", "description": "Return to the live case when a history check is enough.", "url": reverse("veterinary_dashboard:patients")},
                {"label": "Open labs", "description": "Review full lab detail when the summary is not enough.", "url": reverse("veterinary_dashboard:labs")},
                {"label": "Open prescriptions", "description": "Check treatment planning after reviewing the record.", "url": reverse("veterinary_dashboard:prescriptions")},
            ],
            main_section={"label": "Recent records", "title": "Cases and summaries worth revisiting", "cards": record_cards},
            support_section={"label": "Why it matters", "title": "What this page keeps out of the overview", "cards": [
                {"title": "Less homepage clutter", "detail": "Treatment detail belongs here so the overview stays decision-focused.", "status": "Cleaner dashboard", "tone": "teal"},
                {"title": "Faster continuity", "detail": "The vet can reopen recent history before making a fresh call or visit.", "status": "Better context", "tone": "navy"},
                {"title": "Hackathon-safe scope", "detail": "A concise records page demos real value without building a full hospital system.", "status": "Demo ready", "tone": "amber"},
            ]},
            extra_section={"label": "Connected pages", "title": "What usually follows record review", "cards": [
                {"title": "Active Case", "detail": "Jump into the current case after reviewing the history.", "url": reverse("veterinary_dashboard:patients")},
                {"title": "Schedule", "detail": "Open the route if a follow-up visit is needed.", "url": reverse("veterinary_dashboard:schedule")},
                {"title": "Farm Map", "detail": "View the wider farm context if the pattern spans more than one farm.", "url": reverse("veterinary_dashboard:farm_map")},
            ]},
        ),
    )


@login_required
@role_required("veterinary")
def diagnosis_view(request):
    return render(
        request,
        "veterinary_dashboard/workspace_page.html",
        _build_workspace_page_context(
            request,
            page_title="Veterinary Diagnosis | CowCalving",
            page_eyebrow="Diagnosis",
            page_heading="Record the assessment",
            page_intro="Keep findings and next steps together.",
            page_focus={"label": "Diagnosis", "title": "Keep assessment work focused", "text": "Use one page for findings, severity, and the next action.", "badges": ["Severity first", "Structured notes", "Clear handoff"]},
            page_quick_actions=[
                {"label": "Open patient files", "description": "Review the case first.", "url": reverse("veterinary_dashboard:patients")},
                {"label": "Open Rx workflow", "description": "Prepare treatment next.", "url": reverse("veterinary_dashboard:prescriptions")},
                {"label": "Open telehealth", "description": "Send a farmer update.", "url": reverse("veterinary_dashboard:telehealth")},
            ],
            main_section={"label": "Diagnosis queue", "title": "Cases needing clinical attention", "cards": _build_priority_actions()},
            support_section={"label": "Workflow notes", "title": "How to reduce diagnosis friction", "cards": [
                {"title": "Capture only what drives action", "detail": "Use findings, severity, and treatment direction first before opening secondary detail.", "status": "Shorter forms", "tone": "teal"},
                {"title": "Keep note flow linear", "detail": "Patient file, diagnosis, then prescription is easier to remember than mixing all three together.", "status": "Cleaner mental model", "tone": "navy"},
                {"title": "Separate lab interpretation", "detail": "Leave deep result review on the lab page so diagnosis screens stay concise.", "status": "Dedicated review", "tone": "amber"},
            ]},
            extra_section={"label": "After diagnosis", "title": "The next likely pages", "cards": [
                {"title": "Prescriptions", "detail": "Move from diagnosis into medication, route, and withholding guidance.", "url": reverse("veterinary_dashboard:prescriptions")},
                {"title": "Labs", "detail": "Review supporting diagnostics if more evidence is needed.", "url": reverse("veterinary_dashboard:labs")},
                {"title": "Dashboard", "detail": "Return to the lighter overview once active case work is done.", "url": reverse("veterinary_dashboard:dashboard")},
            ]},
        ),
    )


@login_required
@role_required("veterinary")
def prescriptions_view(request):
    return render(
        request,
        "veterinary_dashboard/workspace_page.html",
        _build_workspace_page_context(
            request,
            page_title="Veterinary Prescriptions | CowCalving",
            page_eyebrow="Prescription workflow",
            page_heading="Issue treatment safely",
            page_intro="Keep medication details in one dedicated page.",
            page_focus={"label": "Prescriptions", "title": "Keep treatment clear and safe", "text": "Use this page for medication, withholding, and follow-up.", "badges": ["Safety checks", "Dose clarity", "Follow-up"]},
            page_quick_actions=[
                {"label": "Open diagnosis", "description": "Return to the note.", "url": reverse("veterinary_dashboard:diagnosis")},
                {"label": "Open patients", "description": "Confirm case and weight.", "url": reverse("veterinary_dashboard:patients")},
                {"label": "Open telehealth", "description": "Send the care plan.", "url": reverse("veterinary_dashboard:telehealth")},
            ],
            main_section={"label": "Prescription notes", "title": "Safety checks that must stay visible", "cards": _build_prescription_notes()},
            support_section={"label": "Design rule", "title": "Why Rx deserves its own page", "cards": [
                {"title": "Do not bury withholding periods", "detail": "Farmer-facing risk notes need a consistent place where they cannot be missed.", "status": "Legal and practical", "tone": "amber"},
                {"title": "Keep medication separate from notes", "detail": "Assessment and treatment are connected, but they are easier to review on separate pages.", "status": "Cleaner review", "tone": "navy"},
                {"title": "Use one renewal list", "detail": "A dedicated prescription page is the right home for course endings and refill reminders.", "status": "Less duplication", "tone": "teal"},
            ]},
            extra_section={"label": "Connected pages", "title": "What feeds the prescription workflow", "cards": [
                {"title": "Patient files", "detail": "Open the patient context before issuing treatment.", "url": reverse("veterinary_dashboard:patients")},
                {"title": "Diagnosis", "detail": "Return to findings if the medication plan needs adjustment.", "url": reverse("veterinary_dashboard:diagnosis")},
                {"title": "Telehealth", "detail": "Share final instructions after the prescription is ready.", "url": reverse("veterinary_dashboard:telehealth")},
            ]},
        ),
    )


@login_required
@role_required("veterinary")
def labs_view(request):
    lab_cards = [{"title": panel["title"], "detail": panel["detail"], "status": panel["status"], "tone": "amber"} for panel in _build_lab_panels()]
    return render(
        request,
        "veterinary_dashboard/workspace_page.html",
        _build_workspace_page_context(
            request,
            page_title="Veterinary Labs | CowCalving",
            page_eyebrow="Lab reviews",
            page_heading="Review lab results",
            page_intro="Interpret results before sharing them.",
            page_focus={"label": "Labs", "title": "Review first, share second", "text": "Keep sign-off in one place before results go back to the farmer.", "badges": ["Sign-off first", "Lower risk", "Clear review"]},
            page_quick_actions=[
                {"label": "Open patients", "description": "Match results to the case.", "url": reverse("veterinary_dashboard:patients")},
                {"label": "Open diagnosis", "description": "Add the findings.", "url": reverse("veterinary_dashboard:diagnosis")},
                {"label": "Open analytics", "description": "Check wider patterns.", "url": reverse("veterinary_dashboard:analytics")},
            ],
            main_section={"label": "Pending results", "title": "Reviews waiting for veterinary sign-off", "cards": lab_cards},
            support_section={"label": "Review logic", "title": "Why this page lowers cognitive load", "cards": [
                {"title": "Separate interpretation from communication", "detail": "Reviewing results in a dedicated page prevents chats and other tasks from interrupting analysis.", "status": "Cleaner judgment", "tone": "navy"},
                {"title": "Keep the queue visible", "detail": "A single lab page avoids hiding result review inside unrelated patient or dashboard sections.", "status": "Focused queue", "tone": "teal"},
                {"title": "Link back into cases", "detail": "Once reviewed, labs should feed diagnosis and patient pages rather than duplicate details everywhere.", "status": "Connected workflow", "tone": "amber"},
            ]},
            extra_section={"label": "Next pages", "title": "What usually follows lab review", "cards": [
                {"title": "Diagnosis", "detail": "Update the clinical note based on the reviewed result.", "url": reverse("veterinary_dashboard:diagnosis")},
                {"title": "Patient files", "detail": "Attach the result to the active case context.", "url": reverse("veterinary_dashboard:patients")},
                {"title": "Telehealth", "detail": "Communicate the reviewed result back to the farmer when appropriate.", "url": reverse("veterinary_dashboard:telehealth")},
            ]},
        ),
    )


@login_required
@role_required("veterinary")
def telehealth_view(request):
    chat_cards = [{"title": item["farmer"], "detail": item["message"], "meta": item["time"], "tone": "navy"} for item in _build_telehealth_updates()]
    return render(
        request,
        "veterinary_dashboard/workspace_page.html",
        _build_workspace_page_context(
            request,
            page_title="Veterinary Telehealth | CowCalving",
            page_eyebrow="Telehealth",
            page_heading="Handle remote support clearly",
            page_intro="Keep messages separate from operational overview.",
            page_focus={"label": "Telehealth", "title": "Move from message to action quickly", "text": "Use this page for remote support, then step into the next clinical workflow.", "badges": ["Remote first", "Fast handoff", "Clear next action"]},
            page_quick_actions=[
                {"label": "Open patients", "description": "Open the clinical file.", "url": reverse("veterinary_dashboard:patients")},
                {"label": "Open diagnosis", "description": "Record the outcome.", "url": reverse("veterinary_dashboard:diagnosis")},
                {"label": "Open Rx workflow", "description": "Issue the care plan.", "url": reverse("veterinary_dashboard:prescriptions")},
            ],
            main_section={"label": "Recent updates", "title": "Remote messages and urgent farmer context", "cards": chat_cards},
            support_section={"label": "Communication rule", "title": "How to keep telehealth lighter", "cards": [
                {"title": "Do not mix chats into the dashboard home", "detail": "The overview should only point to urgent communication, not display entire conversation threads.", "status": "Less overload", "tone": "navy"},
                {"title": "Use quick handoffs", "detail": "Every conversation should connect cleanly to patient, diagnosis, or prescription work.", "status": "Workflow-ready", "tone": "teal"},
                {"title": "Highlight time-sensitive messages", "detail": "Urgent remote cases deserve strong priority treatment without burying routine conversations.", "status": "Triage support", "tone": "rose"},
            ]},
            extra_section={"label": "Connected pages", "title": "Where telehealth usually leads next", "cards": [
                {"title": "Schedule", "detail": "Convert an urgent message into a real visit plan.", "url": reverse("veterinary_dashboard:schedule")},
                {"title": "Patients", "detail": "Attach remote findings to the patient file.", "url": reverse("veterinary_dashboard:patients")},
                {"title": "Prescriptions", "detail": "Send treatment instructions after the conversation is complete.", "url": reverse("veterinary_dashboard:prescriptions")},
            ]},
        ),
    )


@login_required
@role_required("veterinary")
def analytics_view(request):
    analytic_cards = [{"title": item["label"], "detail": item["value"], "tone": item["tone"], "progress_width": item["width"]} for item in _build_analytics_bars()]
    farm_cards = [{"title": farm["name"], "detail": farm["detail"], "status": farm["risk"], "tone": farm["tone"], "progress_width": f"{farm['risk_percent']}%"} for farm in _build_farm_overview()]
    return render(
        request,
        "veterinary_dashboard/workspace_page.html",
        _build_workspace_page_context(
            request,
            page_title="Veterinary Analytics | CowCalving",
            page_eyebrow="Analytics",
            page_heading="Review trends separately",
            page_intro="Keep pattern review away from day-of triage.",
            page_focus={"label": "Analytics", "title": "See patterns without dashboard noise", "text": "Use this page for trends and planning, not live operational work.", "badges": ["Trend only", "Population view", "Planning support"]},
            page_quick_actions=[
                {"label": "Open farms", "description": "Return to assigned farms.", "url": reverse("veterinary_dashboard:farms")},
                {"label": "Open labs", "description": "Check diagnostic review.", "url": reverse("veterinary_dashboard:labs")},
                {"label": "Open dashboard", "description": "Return to day-of work.", "url": reverse("veterinary_dashboard:dashboard")},
            ],
            main_section={"label": "Disease trends", "title": "Signals worth tracking", "cards": analytic_cards},
            support_section={"label": "Farm risk", "title": "How the patterns connect to assigned farms", "cards": farm_cards},
            extra_section={"label": "Why this page matters", "title": "The professional value of separate analytics", "cards": [
                {"title": "Better prioritization", "detail": "Separate trends from triage so urgent work stays urgent and planning stays strategic."},
                {"title": "Cleaner executive view", "detail": "This page is easier to share or demo because it groups insights in one professional surface."},
                {"title": "Ready for future live data", "detail": "Once real metrics arrive, this page can grow without expanding the home dashboard again."},
            ]},
        ),
    )
