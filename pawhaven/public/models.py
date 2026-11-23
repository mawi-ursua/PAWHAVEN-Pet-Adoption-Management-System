from django.db import models


class Pet(models.Model):
    class Species(models.TextChoices):
        CAT = "cat", "Cat"
        DOG = "dog", "Dog"

    class Status(models.TextChoices):
        AVAILABLE = "available", "Available"
        MEDICAL_CARE = "medical_care", "Under Medical Care"
        PENDING = "pending", "Pending Evaluation"
        ADOPTED = "adopted", "Adopted"

    class Gender(models.TextChoices):
        MALE = "male", "Male"
        FEMALE = "female", "Female"

    name = models.CharField(max_length=60)
    species = models.CharField("category", max_length=3, choices=Species.choices)
    status = models.CharField(
        max_length=20, choices=Status.choices, default=Status.AVAILABLE
    )
    age_months = models.PositiveSmallIntegerField(
        "age (months)", null=True, blank=True
    )
    gender = models.CharField(max_length=6, choices=Gender.choices, blank=True)
    breed = models.CharField(max_length=80, blank=True)
    photo = models.FileField(upload_to="pets/", blank=True)
    description = models.TextField(blank=True)
    pending_count = models.PositiveIntegerField(
        default=0,
        help_text="Number of pending evaluations (shown when status is Pending).",
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return f"{self.name} ({self.get_species_display()})"

    @property
    def status_label(self):
        if self.status == self.Status.PENDING and self.pending_count:
            return f"{self.pending_count} Pending Evaluation"
        return self.get_status_display()

    @property
    def can_adopt(self):
        return self.status != self.Status.ADOPTED

    @property
    def is_kitten(self):
        return (
            self.species == self.Species.CAT
            and self.age_months is not None
            and self.age_months < 12
        )

    @property
    def age_label(self):
        if self.age_months is None:
            return ""
        if self.age_months < 12:
            return f"{self.age_months} mo"
        years, months = divmod(self.age_months, 12)
        return f"{years} yr" + (f" {months} mo" if months else "")


class AdoptionApplication(models.Model):
    class Status(models.TextChoices):
        PENDING = "pending", "Pending"
        APPROVED = "approved", "Approved"
        REJECTED = "rejected", "Rejected"

    pet = models.ForeignKey(
        Pet, on_delete=models.CASCADE, related_name="applications"
    )
    applicant_name = models.CharField("full name", max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=30, blank=True)
    home_experience = models.TextField(
        "home and experience",
        help_text="Tell us about your home and any experience with pets.",
    )
    status = models.CharField(
        max_length=10, choices=Status.choices, default=Status.PENDING
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.applicant_name} -> {self.pet.name}"


class RescueReport(models.Model):
    class Urgency(models.TextChoices):
        LOW = "low", "Low"
        MEDIUM = "medium", "Medium"
        HIGH = "high", "High/Critical Medical Need"

    class Status(models.TextChoices):
        NEW = "new", "New"
        DISPATCHED = "dispatched", "Dispatched"
        RESOLVED = "resolved", "Resolved"

    location = models.CharField(max_length=255)
    image = models.FileField(upload_to="reports/")
    urgency = models.CharField(
        max_length=10, choices=Urgency.choices, default=Urgency.LOW
    )
    description = models.TextField(blank=True)
    status = models.CharField(
        max_length=10, choices=Status.choices, default=Status.NEW
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.get_urgency_display()} - {self.location}"


class ContactMessage(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.name} <{self.email}>"


class ShelterSettings(models.Model):
    """Single-row table holding the shelter's public information."""

    name = models.CharField("shelter name", max_length=100, default="PawHaven")
    address = models.CharField(max_length=255, default="Isabang, Lucena City")
    contact_number = models.CharField(max_length=30, default="09325869545")
    email = models.EmailField("email address", default="pawhaven@gmail.com")
    description = models.TextField(default="Every pet deserves a home.")

    class Meta:
        verbose_name = "shelter settings"
        verbose_name_plural = "shelter settings"

    def __str__(self):
        return self.name

    @classmethod
    def load(cls):
        obj, _ = cls.objects.get_or_create(pk=1)
        return obj