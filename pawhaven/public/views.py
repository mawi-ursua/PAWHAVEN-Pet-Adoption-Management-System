from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render

from .forms import AdoptionApplicationForm, ContactForm, RescueReportForm
from .models import Pet, RescueReport, ShelterSettings


def home(request):
    return render(request, "public/home.html")


def adoptable_pets(request):
    pets = Pet.objects.exclude(status=Pet.Status.ADOPTED)
    context = {
        "cats": pets.filter(species=Pet.Species.CAT),
        "dogs": pets.filter(species=Pet.Species.DOG),
    }
    return render(request, "public/adoptable_pets.html", context)


def apply_to_adopt(request, pk):
    pet = get_object_or_404(Pet, pk=pk)
    if not pet.can_adopt:
        messages.error(request, f"{pet.name} has already been adopted.")
        return redirect("adoptable_pets")

    if request.method == "POST":
        form = AdoptionApplicationForm(request.POST)
        if form.is_valid():
            application = form.save(commit=False)
            application.pet = pet
            application.save()
            messages.success(
                request,
                f"Thanks! Your application for {pet.name} was submitted. "
                "We'll be in touch soon.",
            )
            return redirect("adoptable_pets")
    else:
        form = AdoptionApplicationForm()
    return render(request, "public/apply.html", {"form": form, "pet": pet})


def report_rescue(request):
    if request.method == "POST":
        form = RescueReportForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(
                request, "Thank you! Your report was sent to our rescue team."
            )
            return redirect("report_rescue")
    else:
        form = RescueReportForm()
    return render(request, "public/report_rescue.html", {"form": form})


def contact(request):
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Message sent! We'll get back to you soon.")
            return redirect("contact")
    else:
        form = ContactForm()
    return render(
        request,
        "public/contact.html",
        {"form": form, "shelter": ShelterSettings.load()},
    )