from django.urls import path

from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("adoptable-pets/", views.adoptable_pets, name="adoptable_pets"),
    path("adopt/<int:pk>/", views.apply_to_adopt, name="apply"),
    path("report-rescue/", views.report_rescue, name="report_rescue"),
    path("contact/", views.contact, name="contact"),
]