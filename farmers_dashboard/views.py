from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse

from users.permissions import role_required
from users.services import get_or_create_profile

from .forms import CowRegistrationForm
from .models import Cow


KENYA_COUNTY_OPTIONS = [
    ("baringo", "Baringo County"),
    ("bomet", "Bomet County"),
    ("bungoma", "Bungoma County"),
    ("busia", "Busia County"),
    ("elgeyo-marakwet", "Elgeyo-Marakwet County"),
    ("embu", "Embu County"),
    ("garissa", "Garissa County"),
    ("homa-bay", "Homa Bay County"),
    ("isiolo", "Isiolo County"),
    ("kajiado", "Kajiado County"),
    ("kakamega", "Kakamega County"),
    ("kericho", "Kericho County"),
    ("kiambu", "Kiambu County"),
    ("kilifi", "Kilifi County"),
    ("kirinyaga", "Kirinyaga County"),
    ("kisii", "Kisii County"),
    ("kisumu", "Kisumu County"),
    ("kitui", "Kitui County"),
    ("kwale", "Kwale County"),
    ("laikipia", "Laikipia County"),
    ("lamu", "Lamu County"),
    ("machakos", "Machakos County"),
    ("makueni", "Makueni County"),
    ("mandera", "Mandera County"),
    ("marsabit", "Marsabit County"),
    ("meru", "Meru County"),
    ("migori", "Migori County"),
    ("mombasa", "Mombasa County"),
    ("muranga", "Murang'a County"),
    ("nairobi", "Nairobi County"),
    ("nakuru", "Nakuru County"),
    ("nandi", "Nandi County"),
    ("narok", "Narok County"),
    ("nyamira", "Nyamira County"),
    ("nyandarua", "Nyandarua County"),
    ("nyeri", "Nyeri County"),
    ("samburu", "Samburu County"),
    ("siaya", "Siaya County"),
    ("taita-taveta", "Taita-Taveta County"),
    ("tana-river", "Tana River County"),
    ("tharaka-nithi", "Tharaka-Nithi County"),
    ("trans-nzoia", "Trans Nzoia County"),
    ("turkana", "Turkana County"),
    ("uasin-gishu", "Uasin Gishu County"),
    ("vihiga", "Vihiga County"),
    ("wajir", "Wajir County"),
    ("west-pokot", "West Pokot County"),
]

SERVICE_TYPE_OPTIONS = [
    ("veterinary", "Veterinary"),
]

# Keep the provider directory in code until the self-serve registration flow
# for professionals is added, so the farmer support page stays demo-ready.
SERVICE_PROVIDER_DIRECTORY = [
    {
        "name": "Dr. James Mwangi",
        "county": "nairobi",
        "county_label": "Nairobi County",
        "service_type": "veterinary",
        "service_type_label": "Veterinary",
        "summary": "Experienced large animal veterinarian supporting dairy herd health, calving readiness, and urgent reproductive follow-up.",
        "phone": "+254712345678",
        "email": "jmwangi@vetkenya.co.ke",
        "coverage": "Nairobi and nearby peri-urban farms",
        "availability": "Same-day callback",
        "is_verified": True,
    },
    {
        "name": "Dr. Grace Wanjiku",
        "county": "kiambu",
        "county_label": "Kiambu County",
        "service_type": "veterinary",
        "service_type_label": "Veterinary",
        "summary": "Focuses on fertility checks, pregnancy confirmation, post-calving review, and milk herd health visits.",
        "phone": "+254723456789",
        "email": "gwanjiku@vetkenya.co.ke",
        "coverage": "Kiambu, Limuru, and Githunguri",
        "availability": "Available this afternoon",
        "is_verified": True,
    },
    {
        "name": "Dr. Peter Kiptoo",
        "county": "uasin-gishu",
        "county_label": "Uasin Gishu County",
        "service_type": "veterinary",
        "service_type_label": "Veterinary",
        "summary": "Supports large dairy farms with heat follow-up, calving supervision, calf recovery, and herd vaccination planning.",
        "phone": "+254734567890",
        "email": "pkiptoo@riftvet.co.ke",
        "coverage": "Eldoret and surrounding dairy belt",
        "availability": "Morning rounds only",
        "is_verified": True,
    },
    {
        "name": "Dr. Mercy Atieno",
        "county": "kisumu",
        "county_label": "Kisumu County",
        "service_type": "veterinary",
        "service_type_label": "Veterinary",
        "summary": "Handles reproductive health reviews, difficult calving follow-up, and newborn calf stabilization for smallholder farms.",
        "phone": "+254745678901",
        "email": "matieno@lakevet.co.ke",
        "coverage": "Kisumu and Nyando corridor",
        "availability": "Responds within 2 hours",
        "is_verified": True,
    },
    {
        "name": "Dr. John Kamau",
        "county": "nakuru",
        "county_label": "Nakuru County",
        "service_type": "veterinary",
        "service_type_label": "Veterinary",
        "summary": "Offers herd fertility planning, retained placenta follow-up, and preventive dairy farm check-ins.",
        "phone": "+254756789012",
        "email": "jkamau@highlandvet.co.ke",
        "coverage": "Nakuru town, Molo, and Subukia",
        "availability": "On-call for urgent calving cases",
        "is_verified": True,
    },
    {
        "name": "Dr. Lucy Muthoni",
        "county": "nyeri",
        "county_label": "Nyeri County",
        "service_type": "veterinary",
        "service_type_label": "Veterinary",
        "summary": "Supports mountain dairy farms with breeding decisions, post-service review, and postpartum recovery checks.",
        "phone": "+254767890123",
        "email": "lmuthoni@centralvet.co.ke",
        "coverage": "Nyeri, Othaya, and Kieni",
        "availability": "Book for next-day visits",
        "is_verified": True,
    },
    {
        "name": "Dr. Brian Mutua",
        "county": "machakos",
        "county_label": "Machakos County",
        "service_type": "veterinary",
        "service_type_label": "Veterinary",
        "summary": "Works with mixed dairy operations on reproductive case reviews, calf health, and emergency labour escalation.",
        "phone": "+254778901234",
        "email": "bmutua@easternvet.co.ke",
        "coverage": "Machakos, Kangundo, and Athi River",
        "availability": "Next available slot tomorrow",
        "is_verified": True,
    },
    {
        "name": "Dr. Faith Akinyi",
        "county": "kakamega",
        "county_label": "Kakamega County",
        "service_type": "veterinary",
        "service_type_label": "Veterinary",
        "summary": "Specialises in dairy cow reproductive management, clean calving setup, and first-day calf care.",
        "phone": "+254789012345",
        "email": "fakinyi@westernvet.co.ke",
        "coverage": "Kakamega and nearby western counties",
        "availability": "Weekend support available",
        "is_verified": True,
    },
    {
        "name": "Dr. Daniel Kibet",
        "county": "kericho",
        "county_label": "Kericho County",
        "service_type": "veterinary",
        "service_type_label": "Veterinary",
        "summary": "Helps farmers plan insemination timing, confirm pregnancy windows, and reduce repeat breeding losses.",
        "phone": "+254790123456",
        "email": "dkibet@highlandanimalcare.co.ke",
        "coverage": "Kericho and Bureti farms",
        "availability": "Available this evening",
        "is_verified": True,
    },
    {
        "name": "Dr. Esther Kathure",
        "county": "meru",
        "county_label": "Meru County",
        "service_type": "veterinary",
        "service_type_label": "Veterinary",
        "summary": "Supports calf survival, difficult deliveries, dairy fertility follow-up, and routine farm visits for growing herds.",
        "phone": "+254701234567",
        "email": "ekathure@uppereastvet.co.ke",
        "coverage": "Meru central and nearby dairy areas",
        "availability": "Responds within 24 hours",
        "is_verified": True,
    },
]


TRACKING_STEPS = [
    (Cow.STAGE_REGISTERED, "Registered"),
    (Cow.STAGE_INSEMINATED, "Inseminated"),
    (Cow.STAGE_PREGNANT, "Pregnant"),
    (Cow.STAGE_NEARING_CALVING, "Nearing calving"),
    (Cow.STAGE_ACTIVE_LABOR, "Active labor"),
    (Cow.STAGE_POST_CALVING, "Post-calving"),
]


def _sync_tracking_stage(cow):
    if cow.tracking_stage == Cow.STAGE_ACTIVE_LABOR:
        cow.is_pregnant = True
        return
    if cow.tracking_stage == Cow.STAGE_NEARING_CALVING:
        cow.is_pregnant = True
        return
    if cow.tracking_stage == Cow.STAGE_PREGNANT:
        cow.is_pregnant = True
        return
    if cow.tracking_stage in {Cow.STAGE_POST_CALVING, Cow.STAGE_REGISTERED, Cow.STAGE_INSEMINATED}:
        cow.is_pregnant = False


def _apply_default_tracking_stage(cow):
    # Guided registration chooses the first reproductive path, then we map it
    # into the current tracker stages so the rest of the farmer workflow stays
    # stable while we build the richer calendar and request flow next.
    if cow.reproductive_status == Cow.REPRODUCTIVE_STATUS_NOT_INSEMINATED:
        cow.tracking_stage = Cow.STAGE_REGISTERED
        cow.is_pregnant = False
    elif cow.reproductive_status == Cow.REPRODUCTIVE_STATUS_INSEMINATED:
        cow.tracking_stage = Cow.STAGE_INSEMINATED
        cow.is_pregnant = False
    elif cow.reproductive_status == Cow.REPRODUCTIVE_STATUS_PREGNANCY_CONFIRMED:
        cow.tracking_stage = Cow.STAGE_PREGNANT
        cow.is_pregnant = True
    elif cow.reproductive_status == Cow.REPRODUCTIVE_STATUS_NEAR_CALVING:
        cow.tracking_stage = Cow.STAGE_NEARING_CALVING
        cow.is_pregnant = True
    elif cow.expected_calving_date and cow.is_nearing_calving():
        cow.tracking_stage = Cow.STAGE_NEARING_CALVING
    elif cow.is_pregnant:
        cow.tracking_stage = Cow.STAGE_PREGNANT
    else:
        cow.tracking_stage = Cow.STAGE_REGISTERED
    _sync_tracking_stage(cow)


def _get_cows_for_user(user):
    cows = list(
        Cow.objects.filter(owner=user).order_by(
            "-needs_attention",
            "expected_calving_date",
            "name",
        )
    )
    alerts = [cow for cow in cows if cow.needs_attention or cow.is_nearing_calving()]
    follow_up = [cow for cow in cows if cow.expected_calving_date or cow.is_pregnant]
    return cows, alerts, follow_up


def _build_navigation_sections(total_cows, alert_count):
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
                    "badge": str(total_cows) if total_cows else None,
                },
                {
                    "label": "Alerts",
                    "url": reverse("farmers_dashboard:alerts"),
                    "view_name": "farmers_dashboard:alerts",
                    "icon": "alerts",
                    "badge": str(alert_count) if alert_count else None,
                },
                {
                    "label": "Service finder",
                    "url": reverse("farmers_dashboard:service_finder"),
                    "view_name": "farmers_dashboard:service_finder",
                    "icon": "services",
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
    return readiness_items, readiness_percent


def _build_summary_cards(cows, alerts):
    pregnant_count = sum(1 for cow in cows if cow.is_pregnant)
    due_this_month_count = sum(1 for cow in cows if cow.is_due_this_month())
    needs_attention_count = sum(1 for cow in cows if cow.needs_attention)
    return [
        {
            "label": "Total cows",
            "value": str(len(cows)),
            "detail": "Registered in your herd",
            "tone": "sky",
        },
        {
            "label": "Pregnant",
            "value": str(pregnant_count),
            "detail": "Currently marked pregnant",
            "tone": "emerald",
        },
        {
            "label": "Due this month",
            "value": str(due_this_month_count),
            "detail": "Expected calving this month",
            "tone": "amber",
        },
        {
            "label": "Open / Needs attention",
            "value": str(needs_attention_count or len(alerts)),
            "detail": "Issues or near-calving cows",
            "tone": "rose",
        },
    ]


def _build_quick_links():
    return [
        {
            "label": "Ask AI",
            "description": "Use quick guidance when the next action is unclear.",
            "url": reverse("cow_calving_ai:index"),
        },
        {
            "label": "Find a vet",
            "description": "Open nearby veterinary support for urgent cases.",
            "url": reverse("farmers_dashboard:service_finder"),
        },
        {
            "label": "Support hub",
            "description": "Open escalation help for farm cases that cannot wait.",
            "url": reverse("Core_Web:support"),
        },
    ]


def _build_service_finder_context(request):
    valid_counties = {value for value, _label in KENYA_COUNTY_OPTIONS}
    valid_service_types = {value for value, _label in SERVICE_TYPE_OPTIONS}
    selected_county = request.GET.get("county", "").strip()
    selected_service_type = request.GET.get("service_type", "").strip()

    if selected_county not in valid_counties:
        selected_county = ""
    if selected_service_type not in valid_service_types:
        selected_service_type = ""

    providers = SERVICE_PROVIDER_DIRECTORY
    if selected_county:
        providers = [
            provider for provider in providers if provider["county"] == selected_county
        ]
    if selected_service_type:
        providers = [
            provider
            for provider in providers
            if provider["service_type"] == selected_service_type
        ]

    return {
        "selected_county": selected_county,
        "selected_service_type": selected_service_type,
        "county_options": [{"value": "", "label": "All counties"}]
        + [{"value": value, "label": label} for value, label in KENYA_COUNTY_OPTIONS],
        "service_type_options": [{"value": "", "label": "All types"}]
        + [
            {"value": value, "label": label}
            for value, label in SERVICE_TYPE_OPTIONS
        ],
        "service_providers": providers,
        "service_provider_count": len(providers),
        "service_directory_count": len(SERVICE_PROVIDER_DIRECTORY),
    }


def _build_farmer_dashboard_context(
    request,
    *,
    page_title,
    page_eyebrow,
    page_heading,
    page_intro,
    page_header_title=None,
    page_header_context=None,
    header_primary_action=None,
    extra_context=None,
):
    profile = get_or_create_profile(request.user)
    display_name = request.user.get_full_name().strip() or request.user.username
    initials = "".join(part[0].upper() for part in display_name.split()[:2] if part) or "FM"
    cows, alerts, follow_up_items = _get_cows_for_user(request.user)
    readiness_items, readiness_percent = _build_profile_readiness(request.user, profile)
    context = {
        "dashboard_home_url": reverse("farmers_dashboard:dashboard"),
        "back_to_website_url": reverse("Core_Web:home"),
        "ai_workspace_url": reverse("cow_calving_ai:index"),
        "ai_workspace_embed_url": f"{reverse('cow_calving_ai:index')}?embedded=1",
        "profile": profile,
        "display_name": display_name,
        "farmer_initials": initials,
        "page_title": page_title,
        "page_eyebrow": page_eyebrow,
        "page_heading": page_heading,
        "page_intro": page_intro,
        "page_header_title": page_header_title or page_heading,
        "page_header_context": page_header_context,
        "navigation_sections": _build_navigation_sections(len(cows), len(alerts)),
        "workspace_menu_sections": _build_farmer_workspace_menu_sections(),
        "profile_readiness_items": readiness_items,
        "profile_readiness_percent": readiness_percent,
        "summary_cards": _build_summary_cards(cows, alerts),
        "cow_records": cows,
        "cow_alerts": alerts,
        "follow_up_items": follow_up_items,
        "dashboard_quick_links": _build_quick_links(),
        "header_primary_action": header_primary_action
        or {
            "label": "Register cow",
            "url": reverse("farmers_dashboard:cow_register"),
        },
    }
    if extra_context:
        context.update(extra_context)
    return context


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
            page_heading="Herd overview",
            page_intro="Register cows, upload a photo, and start tracking calving from one place.",
            page_header_context="Interactive herd dashboard",
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
            page_title="My Herd | CowCalving",
            page_eyebrow="Herd dashboard",
            page_heading="My cows",
            page_intro="Keep each cow number, image, and next calving action visible.",
            header_primary_action={
                "label": "Add cow",
                "url": reverse("farmers_dashboard:cow_register"),
            },
        ),
    )


@login_required
@role_required("farmer")
def alerts_view(request):
    context = _build_farmer_dashboard_context(
        request,
        page_title="Cow Alerts | CowCalving",
        page_eyebrow="Alerts",
        page_heading="Cow alerts",
        page_intro="See cows with issues or those nearing calving, then open the next step.",
        header_primary_action={
            "label": "Open herd",
            "url": reverse("farmers_dashboard:herd"),
        },
    )
    context["alert_counts"] = {
        "all": len(context["cow_alerts"]),
        "nearing_calving": sum(
            1 for cow in context["cow_alerts"] if cow.alert_category == "Nearing calving"
        ),
        "needs_attention": sum(
            1 for cow in context["cow_alerts"] if cow.needs_attention
        ),
    }
    return render(request, "farmers_dashboard/alerts.html", context)


@login_required
@role_required("farmer")
def reports_view(request):
    return render(
        request,
        "farmers_dashboard/reports.html",
        _build_farmer_dashboard_context(
            request,
            page_title="Follow-up Schedule | CowCalving",
            page_eyebrow="Reports",
            page_heading="Follow-up schedule",
            page_intro="Keep follow-up dates and next review work visible for each cow.",
            header_primary_action={
                "label": "Open alerts",
                "url": reverse("farmers_dashboard:alerts"),
            },
        ),
    )


@login_required
@role_required("farmer")
def service_finder_view(request):
    return render(
        request,
        "farmers_dashboard/service_finder.html",
        _build_farmer_dashboard_context(
            request,
            page_title="Service Finder | CowCalving",
            page_eyebrow="Farmer support",
            page_heading="Service finder",
            page_intro="Filter by county and provider type, then contact the provider that best matches the case.",
            page_header_context="Find veterinary support by county",
            header_primary_action={
                "label": "Reset filters",
                "url": reverse("farmers_dashboard:service_finder"),
            },
            extra_context=_build_service_finder_context(request),
        ),
    )


@login_required
@role_required("farmer")
def cow_register_view(request):
    if request.method == "POST":
        form = CowRegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            cow = form.save(commit=False)
            cow.owner = request.user
            # Keep the tracker defaults and guided registration state aligned so
            # the user lands on the correct cow workflow page immediately after save.
            _apply_default_tracking_stage(cow)
            cow.save()
            messages.success(request, f"{cow.name} was added to your herd.")
            return redirect("farmers_dashboard:cow_tracking", cow_id=cow.pk)
    else:
        form = CowRegistrationForm()

    return render(
        request,
        "farmers_dashboard/cow_register.html",
        _build_farmer_dashboard_context(
            request,
            page_title="Register Cow | CowCalving",
            page_eyebrow="New cow",
            page_heading="New Cow Registration",
            page_intro="Add the cow details, choose the reproductive starting point, and continue into the right tracker flow.",
            header_primary_action={
                "label": "Back to dashboard",
                "url": reverse("farmers_dashboard:dashboard"),
            },
            extra_context={"form": form},
        ),
    )


@login_required
@role_required("farmer")
def cow_tracking_view(request, cow_id):
    cow = get_object_or_404(Cow, owner=request.user, pk=cow_id)

    if request.method == "POST":
        next_stage = request.POST.get("tracking_stage", "").strip()
        toggle_attention = request.POST.get("toggle_attention")

        if next_stage and next_stage in dict(Cow.TRACKING_STAGE_CHOICES):
            cow.tracking_stage = next_stage
            _sync_tracking_stage(cow)
            if cow.tracking_stage == Cow.STAGE_POST_CALVING:
                cow.needs_attention = False
            cow.save(update_fields=["tracking_stage", "is_pregnant", "needs_attention", "updated_at"])
            messages.success(request, f"{cow.name} tracking stage updated.")
            return redirect("farmers_dashboard:cow_tracking", cow_id=cow.pk)

        if toggle_attention:
            cow.needs_attention = not cow.needs_attention
            cow.save(update_fields=["needs_attention", "updated_at"])
            messages.success(
                request,
                f'{cow.name} is now marked as {"needing attention" if cow.needs_attention else "stable"}.',
            )
            return redirect("farmers_dashboard:cow_tracking", cow_id=cow.pk)

    stage_options = [
        {
            "value": value,
            "label": label,
            "is_active": cow.tracking_stage == value,
        }
        for value, label in TRACKING_STEPS
    ]

    return render(
        request,
        "farmers_dashboard/cow_tracking.html",
        _build_farmer_dashboard_context(
            request,
            page_title=f"{cow.name} Tracking | CowCalving",
            page_eyebrow="Cow tracking",
            page_heading=f"{cow.name} {cow.cow_number}",
            page_intro="Review the current reproductive path, then move through the calving stages and next actions for this cow.",
            header_primary_action={
                "label": "Back to herd",
                "url": reverse("farmers_dashboard:herd"),
            },
            extra_context={
                "cow": cow,
                "stage_options": stage_options,
            },
        ),
    )
