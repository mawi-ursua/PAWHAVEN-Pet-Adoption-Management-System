from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.forms import PasswordChangeForm
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from public.models import AdoptionApplication, Pet, RescueReport, ShelterSettings

from .forms import (
    AdminProfileForm,
    PetForm,
    ShelterSettingsForm,
)


def staff_required(view):
    return user_passes_test(
        lambda u: u.is_active and u.is_staff, login_url="private:login"
    )(view)


# ---------------------------------------------------------------- Dashboard
@staff_required
def dashboard(request):
    context = {
        "section": "dashboard",
        "total_pets": Pet.objects.count(),
        "pending_applications": AdoptionApplication.objects.filter(
            status=AdoptionApplication.Status.PENDING
        ).count(),
        "rescue_requests": RescueReport.objects.filter(
            status=RescueReport.Status.NEW
        ).count(),
        "recent_applications": AdoptionApplication.objects.filter(
            status=AdoptionApplication.Status.PENDING
        ).select_related("pet")[:5],
    }
    return render(request, "private/dashboard.html", context)


# --------------------------------------------------------------------- Pets
PET_CATEGORIES = [
    ("all", "All Pets"),
    ("cats", "Cats"),
    ("dogs", "Dogs"),
    ("kittens", "Kittens"),
]


@staff_required
def pet_list(request):
    pets = Pet.objects.all()
    category = request.GET.get("category", "all")
    status = request.GET.get("status", "")

    if category == "cats":
        pets = pets.filter(species=Pet.Species.CAT)
    elif category == "dogs":
        pets = pets.filter(species=Pet.Species.DOG)
    elif category == "kittens":
        pets = pets.filter(species=Pet.Species.CAT, age_months__lt=12)
    else:
        category = "all"

    if status in Pet.Status.values:
        pets = pets.filter(status=status)
    else:
        status = ""

    context = {
        "section": "pets",
        "pets": pets,
        "categories": PET_CATEGORIES,
        "category": category,
        "status": status,
        "statuses": Pet.Status.choices,
    }
    return render(request, "private/pet_list.html", context)


@staff_required
def pet_create(request):
    form = PetForm(request.POST or None, request.FILES or None)
    if request.method == "POST" and form.is_valid():
        pet = form.save()
        messages.success(request, f"{pet.name} was registered.")
        return redirect("private:pets")
    return render(
        request,
        "private/pet_form.html",
        {"section": "pets", "form": form, "editing": False},
    )


@staff_required
def pet_edit(request, pk):
    pet = get_object_or_404(Pet, pk=pk)
    form = PetForm(request.POST or None, request.FILES or None, instance=pet)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, f"{pet.name} was updated.")
        return redirect("private:pets")
    return render(
        request,
        "private/pet_form.html",
        {"section": "pets", "form": form, "editing": True, "pet": pet},
    )


@staff_required
@require_POST
def pet_delete(request, pk):
    pet = get_object_or_404(Pet, pk=pk)
    name = pet.name
    pet.delete()
    messages.success(request, f"{name} was removed.")
    return redirect("private:pets")


# ------------------------------------------------------------- Applications
@staff_required
def application_list(request):
    applications = AdoptionApplication.objects.select_related("pet")
    status = request.GET.get("status", "all")
    if status in AdoptionApplication.Status.values:
        applications = applications.filter(status=status)
    else:
        status = "all"
    return render(
        request,
        "private/application_list.html",
        {
            "section": "applications",
            "applications": applications,
            "status": status,
            "filters": [("all", "All")]
            + [(v, l) for v, l in AdoptionApplication.Status.choices],
        },
    )


@staff_required
@require_POST
def application_decide(request, pk, decision):
    application = get_object_or_404(AdoptionApplication, pk=pk)
    if decision not in (
        AdoptionApplication.Status.APPROVED,
        AdoptionApplication.Status.REJECTED,
    ):
        return redirect("private:applications")

    application.status = decision
    application.save(update_fields=["status"])
    if decision == AdoptionApplication.Status.APPROVED:
        application.pet.status = Pet.Status.ADOPTED
        application.pet.save(update_fields=["status"])
    messages.success(
        request,
        f"Application from {application.applicant_name} marked {decision}.",
    )
    return redirect("private:applications")


# ------------------------------------------------------------------- Rescue
@staff_required
def rescue_list(request):
    reports = RescueReport.objects.all()
    flt = request.GET.get("filter", "all")
    if flt == "critical":
        reports = reports.filter(urgency=RescueReport.Urgency.HIGH)
    elif flt == "dispatched":
        reports = reports.filter(status=RescueReport.Status.DISPATCHED)
    else:
        flt = "all"
    return render(
        request,
        "private/rescue_list.html",
        {
            "section": "rescue",
            "reports": reports,
            "filter": flt,
            "filters": [
                ("all", "All"),
                ("critical", "Critical"),
                ("dispatched", "Dispatched"),
            ],
        },
    )


@staff_required
@require_POST
def rescue_update(request, pk, new_status):
    report = get_object_or_404(RescueReport, pk=pk)
    if new_status in RescueReport.Status.values:
        report.status = new_status
        report.save(update_fields=["status"])
        messages.success(request, f"Report marked {report.get_status_display().lower()}.")
    return redirect("private:rescue")


# ----------------------------------------------------------------- Settings
@staff_required
def settings_view(request):
    shelter = ShelterSettings.load()
    shelter_form = ShelterSettingsForm(instance=shelter)
    profile_form = AdminProfileForm(user=request.user)

    if request.method == "POST":
        if "save_shelter" in request.POST:
            shelter_form = ShelterSettingsForm(request.POST, instance=shelter)
            if shelter_form.is_valid():
                shelter_form.save()
                messages.success(request, "Shelter settings saved.")
                return redirect("private:settings")
        elif "save_profile" in request.POST:
            profile_form = AdminProfileForm(request.POST, user=request.user)
            if profile_form.is_valid():
                profile_form.save()
                messages.success(request, "Profile updated.")
                return redirect("private:settings")

    return render(
        request,
        "private/settings.html",
        {
            "section": "settings",
            "shelter_form": shelter_form,
            "profile_form": profile_form,
        },
    )


@staff_required
def password_change(request):
    form = PasswordChangeForm(request.user, request.POST or None)
    if request.method == "POST" and form.is_valid():
        user = form.save()
        update_session_auth_hash(request, user)  # keep the admin logged in
        messages.success(request, "Password changed.")
        return redirect("private:settings")
    return render(
        request,
        "private/password_change.html",
        {"section": "settings", "form": form},
    )