# 🏥 Medicare Appointment Management System

A role-based, secure online platform for managing doctor availability and patient appointments — built using Django and Django REST Framework.

![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)
![Django](https://img.shields.io/badge/Django-4.0-green.svg)
![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)
![Redis](https://img.shields.io/badge/Redis-Enabled-red.svg)
![Celery](https://img.shields.io/badge/Celery-Asynchronous%20Tasks-orange.svg)

---

## ✨ Features

### 👩‍⚕️ Doctor Module
- Secure login with brute-force protection
- Add/edit/delete availability slots (single-day or repeat by weekday)
- View patients who booked appointments
- View upcoming & past appointment history
- Delete availability with modal confirmation (no page reload)

### 👨‍💼 Admin Module
- Admin login with lockout protection
- Dashboard with total doctor, patient, and appointment counts
- Search, filter, and paginate doctors and appointments
- View patients excluding staff and doctor accounts

### 🧑‍💻 Patient/User Functionality
- Book appointment with any listed doctor
- Smart time-slot validation:
  - Checks doctor availability
  - Avoids double booking
- Confirmation email sent via background task

---

## 🔐 Login Security (with `django-axes`)
- Limits login to 3 failed attempts
- Lockout for 1 minute on breach
- Cooldown messages shown inline in UI (no redirects)
- Failed attempts auto-reset after cooldown or successful login

---

## 💻 Tech Stack

### Backend
- Python 3.9+
- Django 4+
- Django REST Framework
- Celery
- Redis
- django-axes (for login security)

### Frontend
- HTML5
- CSS3 (custom styling, no Bootstrap)
- Vanilla JavaScript
- Font Awesome / Boxicons (for icons)

### Database
- SQLite (default) — can easily migrate to PostgreSQL or MySQL

---

## 📧 Email Notifications

- **When**: Appointment is booked
- **How**: Email sent asynchronously using Celery + Redis
- **Where**: Email configured via Django's email backend

---

## 📦 Optional & Configurable
- Pagination using `Paginator`
- Admin dashboard styled separately
- Delete confirmations via modal
- Time and date formatting in human-readable format
- Custom error boxes for all login and lockout messages

---

## 🚀 Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/medicare-appointment-system.git
cd medicare-appointment-system
```

### 2. Create a Virtual Environment

```
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```
### 3. Install Requirements
```
pip install -r requirements.txt
```
### 4. Apply Migrations
```
python manage.py makemigrations
python manage.py migrate
```
### 5. Run Redis Server
```
# For Windows (using Redis installed manually)
redis-server

# Or on Linux/macOS
brew services start redis  # or sudo systemctl start redis
```
### 6. Run Celery Worker

```
celery -A your_project_name worker --loglevel=info
```
### 7. Start the Development Server
```
python manage.py runserver
```
## 🧪 Admin & Demo Logins

Create superuser:
```
python manage.py createsuperuser
```
You can log in via:

- /admin/ → Django Admin
- /doctor/login/ → Doctor portal
- /admin/login/ → Admin dashboard login

## 📁 Project Structure (Simplified)  
```
medicare_project/
│
├── templates/
│   ├── doctor_login.html
│   ├── admin_login.html
│   ├── dashboard.html
│   └── ...
├── static/
│   └── css/, js/, images/
├── apps/
│   └── medicareApp/
│       ├── models.py
│       ├── views.py
│       ├── forms.py
│       ├── serializers.py
│       └── urls.py
├── celery.py
├── settings.py
├── urls.py
└── ...
```

## 🔐 Environment Variables to Configure
In your .env or settings.py, make sure to configure:

```python
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'your-email@gmail.com'
EMAIL_HOST_PASSWORD = 'your-app-password'
```
---

# 🏥 Medicare App – REST API for Online Doctor Appointment Booking

## 📌 Overview

Medicare App is a RESTful API built using Django and Django REST Framework (DRF) that allows patients to:

* Register, login, and manage their profiles.
* View doctors and their availability.
* Book appointments with doctors.
* View and cancel appointments.
* Upload medical reports.

This backend system is secure, scalable, and uses JWT authentication, custom responses, and clean exception handling.

---

## 🧱 Tech Stack

| Layer            | Stack/Tool                              |
| ---------------- | --------------------------------------- |
| Backend          | Django 4.x, Django REST Framework (DRF) |
| Auth             | JWT (`rest_framework_simplejwt`)        |
| Database         | SQLite/PostgreSQL                       |
| Async (Optional) | Celery + Redis (for OTPs/emails)        |
| File Storage     | Django `FileField`                      |

---

## 👤 User Roles

* **UserProfile**: Custom user model based on `AbstractUser`.
* **Doctor**: Linked one-to-one with UserProfile.

---

## 📅 Models & Relationships

### `UserProfile`

* Login with `email`
* Fields: `name`, `email`, `phone_number`, `gender`, `age`, `place`, `otp`, `is_email_verified`

### `Doctors`

* Fields: `specialization`, `hospital`, `address`, `image`

### `DoctorAvailability`

* Fields: `doctor`, `start_date`, `end_date`, `start_time`, `end_time`, `repeat_pattern`, `repeat_days`

### `Appointment`

* Fields: `doctor`, `patient`, `date`, `time`
* Constraint: Unique per doctor/date/time

### `Records`

* Fields: `patient`, `report`, `report_type`, `notes`, `file`

---

## 🔐 Authentication & Security

* JWT-based login/logout
* `IsAuthenticated` permissions
* Centralized error handling with `try_except_wrapper`

---

## 📡 API Endpoints

### 🔐 Auth

* `POST /api/register/`
* `POST /api/login/`
* `POST /api/logout/`
* `POST /api/token/`
* `POST /api/refresh/`

### 👤 Profile

* `GET /api/profile/`

### 🩺 Doctor

* `POST /api/create-doctor/`
* `GET /api/doctors/`
* `GET /api/doctor/<id>/availability/?date=YYYY-MM-DD`
* `GET /api/doctor/<id>/timeslots/?date=YYYY-MM-DD`

### 📅 Appointments

* `POST /api/book-appointment/`
* `GET /api/appointments/history/`
* `DELETE /api/appointments/<id>/cancel/`

### 📄 Reports

* `POST /api/reports/upload/`

---

## ✅ Custom Response Format

```json
{
  "status": "Success",
  "status_code": 200,
  "message": "Available time slots fetched successfully.",
  "data": {
    "available_slots": ["09:00", "09:30", "10:00"]
  }
}
```

### ❌ Error Format

```json
{
  "status": "Bad Request",
  "status_code": 400,
  "message": "Booking failed",
  "errors": {
    "date": ["This field is required."]
  }
}
```

---

## 🔄 Utilities

* `custom200()`, `custom201()`, `custom400()`, `custom401()`, `custom404()`
* `flatten_errors()`
* `try_except_wrapper`

---

## 🧪 Sample Postman Request – Book Appointment

**URL:** `POST /api/book-appointment/`

**Headers:**

```
Authorization: Bearer <access_token>
Content-Type: application/json
```

**Body:**

```json
{
  "doctor": 13,
  "date": "2025-06-14",
  "time": "10:30"
}
```

---



