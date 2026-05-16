# Smart Tourism

A full-stack tourism management system for Tour and Travels with a Django REST API and a React admin/visitor frontend. The app supports tourist place discovery, user dashboards, bookings, favorites, reviews, analytics, cab booking, email verification, Google login, and admin content management.

## Tech Stack

- Backend: Django, Django REST Framework, Simple JWT, SQLite, django-filter, Celery settings, SMTP email
- Frontend: React, Vite, React Bootstrap, React Router, Axios, React Toastify, React Icons
- Auth: JWT email/password login, signed email verification links, Google Identity Services ID token login
- Maps and location: OpenStreetMap embed for admin place pinning, geopy distance calculation, optional Google Maps API key
- Weather: Optional OpenWeatherMap API integration

## Main Features

- Visitor registration and login
- Google account login for visitors and admins
- Email verification with signed 24-hour verification tokens
- Visitor dashboard with bookings, favorites, reviews, and account controls
- Visitor self-delete account option through safe deactivation
- Admin user management with delete/deactivate account option
- Admin place management with add, edit, delete, gallery upload, and category controls
- Quick admin category creation for Cafes and Lodges
- Tourist place search, filters, details, weather, nearby places, and favorites
- Cab booking, booking management, reviews, payments, analytics, notifications, and AI assistant modules

## Project Structure

```text
kalahandi-tourism/
  apps/                       Django apps
    users/                    Custom user, auth, profiles
    places/                   Categories, tourist places, images, favorites
    bookings/                 Booking workflows
    cabs/                     Cab management
    reviews/                  Reviews and ratings
    analytics/                Visitor activity tracking
    notifications/            Notification models/tasks
  smart_tourism/              Django settings and root URLs
  smart-tourism-frontend/     Vite React frontend
  media/                      Uploaded files
  db.sqlite3                  Local development database
```

## Backend Setup

1. Create and activate a virtual environment.
2. Install the Django project dependencies used by the environment.
3. Configure `.env`.
4. Run migrations and checks.

```powershell
.\.venv\Scripts\python.exe manage.py migrate
.\.venv\Scripts\python.exe manage.py check
.\.venv\Scripts\python.exe manage.py runserver
```

Important backend environment variables:

```env
SECRET_KEY=django-secret-key
DEBUG=True
ALLOWED_HOSTS=127.0.0.1,localhost
FRONTEND_URL=http://localhost:5173
GOOGLE_CLIENT_ID=
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=
EMAIL_HOST_PASSWORD=
WEATHER_API_KEY=
```

## Frontend Setup

```powershell
cd smart-tourism-frontend
npm install
npm run dev -- --host 127.0.0.1
```

Frontend environment variables:

```env
VITE_API_BASE_URL=http://127.0.0.1:8000/api/
VITE_GOOGLE_CLIENT_ID=
```

## Auth Logic

Email/password login uses Simple JWT. On successful login, the backend returns access and refresh tokens. The access token includes custom claims for email, full name, role, and admin status, allowing the frontend route guard to send admins to the admin panel and visitors to the dashboard.

Email verification uses Django `TimestampSigner`. Registration creates a signed token containing the user id. The verification endpoint accepts the token, validates its signature and 24-hour age, then sets `is_verified` and `email_verified_at`.

Google login uses the Google Identity Services browser script on the frontend. The frontend receives a Google ID token and sends it to the Django API. The backend verifies the token through Google's `tokeninfo` endpoint, checks the configured `GOOGLE_CLIENT_ID` audience when present, confirms the Google email is verified, and then creates or logs in the local user with JWT tokens.

Account deletion is implemented as soft deletion. Visitor self-delete and admin user delete set `is_active=False`, preserving booking/review history for audit and reporting.

## Place Management Logic

Tourist places are stored with categories, coordinates, fees, timing, images, status, and recommendation flags. Admins can create, update, and delete places through DRF viewsets. Public users only see published places.

Slugs are generated automatically from the place name. If a slug already exists, the model appends a number to keep it unique.

Nearby places use a latitude/longitude bounding-box approximation around the selected place before returning nearby published results. Distance calculation uses the Haversine/geodesic method through `geopy`.

## Key API Routes

- `POST /api/register/` register visitor and send verification email
- `POST /api/login/` login with email/password
- `POST /api/google/` login or create account with Google ID token
- `POST /api/verify-email/` verify signed email token
- `POST /api/resend-verification/` resend verification email
- `GET/PATCH /api/users/profile/` visitor profile
- `DELETE /api/users/delete-account/` visitor self-delete/deactivate
- `GET/DELETE /api/users/{id}/` admin user management
- `GET/POST /api/places/` list or create tourist places
- `GET/PATCH/DELETE /api/places/{slug}/` place detail, edit, delete
- `POST /api/places/{slug}/upload_images/` upload place gallery images
- `GET/POST /api/places/categories/` list or create categories

## Admin Workflow

1. Login as an admin.
2. Open `/admin/places` to manage destinations.
3. Add Cafes or Lodges as categories when needed.
4. Use Add Place to create a destination, cafe, or lodge.
5. Use Edit to fix uploaded place mistakes.
6. Use Delete to remove places from listings.
7. Open Users to deactivate visitor or admin accounts.

## Visitor Workflow

1. Register with email/password or login with Google.
2. Verify email from the verification link.
3. Browse places, save favorites, submit reviews, and book cabs.
4. Use the dashboard to review stats and resend verification email.
5. Use Delete my account to deactivate the account.

## Verification

Recommended checks before committing:

```powershell
.\.venv\Scripts\python.exe manage.py check
cd smart-tourism-frontend
npm run lint
npm run build
```
