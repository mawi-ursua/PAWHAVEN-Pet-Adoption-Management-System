from django.contrib import admin

from .models import (
    AdoptionApplication,
    ContactMessage,
    Pet,
    RescueReport,
    ShelterSettings,
)


@admin.register(Pet)
class PetAdmin(admin.ModelAdmin):
    list_display = ("name", "species", "status", "pending_count")
    list_filter = ("species", "status")
    search_fields = ("name",)


@admin.register(AdoptionApplication)
class AdoptionApplicationAdmin(admin.ModelAdmin):
    list_display = ("applicant_name", "pet", "status", "created_at")
    list_filter = ("status",)


@admin.register(RescueReport)
class RescueReportAdmin(admin.ModelAdmin):
    list_display = ("location", "urgency", "status", "created_at")
    list_filter = ("urgency", "status")


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "created_at")
    readonly_fields = ("created_at",)


admin.site.register(ShelterSettings)