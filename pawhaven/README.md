# PawHaven

Django site for pet adoption and rescue reporting, built from the PawHaven wireframes.

## Public pages

| URL | Page |
|---|---|
| `/` | Home |
| `/adoptable-pets/` | Adoptable Pets (cats and dogs) |
| `/adopt/<id>/` | Adoption application for one pet |
| `/report-rescue/` | Report a Pet in Need |
| `/contact/` | Contact Us |

## Admin portal (staff only)

Sign in at `/manage/login/` with a superuser/staff account.

| URL | Page |
|---|---|
| `/manage/` | Dashboard |
| `/manage/pets/` | Adoptable Pets: filter, register, edit, delete |
| `/manage/applications/` | Adoption Applications: filter, approve, reject |
| `/manage/rescue/` | Rescue Control: filter, dispatch, resolve |
| `/manage/settings/` | Shelter info, admin profile, change password |

Approving an application marks the pet as Adopted.
Django's built-in admin is still available at `/admin/`.

## Setup

    python -m venv .venv
    source .venv/bin/activate        (Windows: .venv\Scripts\activate)
    pip install -r requirements.txt
    python manage.py makemigrations public
    python manage.py migrate
    python manage.py createsuperuser
    python manage.py runserver

Then open http://127.0.0.1:8000/manage/login/.

## Images to add

Put `hero-room.jpg` and `hero-cat.png` in `static/img/`.
Pet photos and rescue report uploads are saved to `media/`.