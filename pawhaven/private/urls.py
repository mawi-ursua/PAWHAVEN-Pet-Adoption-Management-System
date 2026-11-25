from django.contrib.auth import views as auth_views
from django.urls import path

from . import views
from .forms import StaffAuthenticationForm

app_name = "private"

urlpatterns = [
    path(
        "login/",
        auth_views.LoginView.as_view(
            template_name="private/login.html",
            authentication_form=StaffAuthenticationForm,
        ),
        name="login",
    ),
    path(
        "logout/",
        auth_views.LogoutView.as_view(next_page="private:login"),
        name="logout",
    ),
    path("", views.dashboard, name="dashboard"),
    path("pets/", views.pet_list, name="pets"),
    path("pets/new/", views.pet_create, name="pet_create"),
    path("pets/<int:pk>/edit/", views.pet_edit, name="pet_edit"),
    path("pets/<int:pk>/delete/", views.pet_delete, name="pet_delete"),
    path("applications/", views.application_list, name="applications"),
    path(
        "applications/<int:pk>/<str:decision>/",
        views.application_decide,
        name="application_decide",
    ),
    path("rescue/", views.rescue_list, name="rescue"),
    path(
        "rescue/<int:pk>/<str:new_status>/",
        views.rescue_update,
        name="rescue_update",
    ),
    path("settings/", views.settings_view, name="settings"),
    path("settings/password/", views.password_change, name="password_change"),
]