## Setup

    python -m venv .venv
    venv\Scripts\activate
    pip install -r requirements.txt
    python manage.py makemigrations public
    python manage.py migrate
    python manage.py createsuperuser
    python manage.py runserver

## Public pages

| URL | Page |
| `/` | Home |
| `/adoptable-pets/` | Adoptable Pets (cats and dogs) |
| `/adopt/<id>/` | Adoption application for one pet |
| `/report-rescue/` | Report a Pet in Need |
| `/contact/` | Contact Us |

## Admin portal (staff only)

Sign in at `/manage/login/` with a superuser/staff account.

| URL | Page |
|---|---|
| `/pawhaven-admin/` | Dashboard |
| `/pawhaven-admin/pets/` | Adoptable Pets: filter, register, edit, delete |
| `/pawhaven-admin/applications/` | Adoption Applications: filter, approve, reject |
| `/pawhaven-admin/rescue/` | Rescue Control: filter, dispatch, resolve |
| `/pawhaven-admin/settings/` | Shelter info, admin profile, change password |

Approving an application marks the pet as Adopted.
Django's built-in admin is still available at `/admin/`.


## Images to add

Put `hero-room.jpg` and `hero-cat.png` in `static/img/`.
Pet photos and rescue report uploads are saved to `media/`.