# Smart City & Mobility Platform

A comprehensive Django-based urban management system with citizen dashboards, admin controls, GPS bus tracking, trip planning, and electronic ticketing.

## Features

### Two Dashboards
- **Admin Dashboard** (`/dashboard/`) — Manage citizens, vehicles, traffic signals, transport routes, public transport, payments, staff, calculations, schedules, bus tracking, tickets, and smart cards.
- **Citizen Dashboard** (`/user-dashboard/`) — Personal profile, vehicles, smart cards, tickets, live bus tracking, traffic signal status, and transport schedules.

### Core Modules
| Module | Description |
|---|---|
| **Citizen Management** | Register residents with auto-created user accounts |
| **Vehicle Management** | Track vehicles, ownership, and parking |
| **Smart Traffic Signals** | Monitor signal status and maintenance |
| **Transport Routes** | Define route networks and schedules |
| **Public Transport** | Manage buses, drivers, capacity, and fares |
| **Parking Spaces** | Allocate and track parking inventory |
| **Payments** | Process civic payments and transactions |
| **Staff Management** | Employee records and assignments |
| **Calculations & Reports** | Data-driven analytics |

### Smart City Features
- **Live GPS Bus Tracking** — Interactive Leaflet map showing real-time bus positions, speed, and headings
- **Trip Planning** — Search transport schedules by origin/destination
- **Electronic Ticketing** — Purchase tickets via smart card, mobile money, cash, or QR code
- **Smart Cards** — Pre-loaded balance cards for cashless payments
- **First-Login Flow** — Citizens log in with National ID and set their password on first visit

## Tech Stack

- **Backend:** Django 4.2, Python 3.14
- **Database:** SQLite (PostgreSQL/PostGIS recommended for production GeoDjango)
- **Frontend:** Server-side Django templates, Inter font, Lucide icons
- **Map:** Leaflet.js + OpenStreetMap tiles
- **Animations:** AOS (Animate On Scroll)

## Quick Start

```bash
# Clone the repo
git clone <repo-url>
cd smartcities

# Create and activate virtual environment
python -m venv venv
venv\Scripts\activate     # Windows
source venv/bin/activate  # Linux/Mac

# Install dependencies
pip install -r requirements.txt

# Run migrations
python manage.py migrate

# Seed sample data
python manage.py seed_data

# Start the server
python manage.py runserver
```

## Credentials

### Admin
| Username | Password |
|---|---|
| `admin` | `admin123` |

### Citizen Test Accounts
| Name | National ID | First Login? |
|---|---|---|
| John Mwangi | `NID001001` | Yes — set password on login |
| Mary Wanjiku | `NID002002` | Yes — set password on login |
| Peter Kamau | `NID003003` | Yes — set password on login |

Citizens log in at `/login/` using their **National ID**. On first login, no password is required — they are redirected to set their own password.

## Project Structure

```
smartcities/
├── manage.py
├── requirements.txt
├── smartcities/               # Django project config
│   ├── settings.py
│   ├── urls.py                # Root URL config
│   └── wsgi.py / asgi.py
├── sport/                     # Main application
│   ├── models.py              # 14 data models
│   ├── views.py               # 40+ view functions
│   ├── urls.py                # 40+ URL routes
│   ├── management/commands/
│   │   └── seed_data.py       # Sample data seeder
│   └── templates/
│       ├── base.html          # Public-facing layout
│       ├── dashboard_base.html # Admin sidebar layout
│       ├── home.html          # Landing page
│       ├── login.html         # Login page
│       ├── user_dashboard.html # Citizen dashboard
│       └── ... (45+ templates)
└── db.sqlite3
```

## Models (14 total)

| Model | Key Fields |
|---|---|
| `Citizen` | full_name, gender, phone, email, address, national_id |
| `Vehicle` | citizen (FK), plate_number, vehicle_type, brand, color |
| `TrafficSignal` | location, signal_status, installation_date |
| `TransportRoute` | route_name, start_point, end_point, distance |
| `PublicTransport` | vehicle (FK), route (FK), driver_name, capacity, fare |
| `ParkingSpace` | space_number, floor, section, status, parking_fee |
| `Payment` | amount, payment_method, payment_date, payment_status |
| `Staff` | first_name, last_name, phone, email, position, salary |
| `Calculation` | totals for vehicles, hours, and revenue |
| `UserProfile` | user (FK), citizen (FK), is_first_login |
| `BusLocation` | bus (FK), latitude, longitude, speed, heading |
| `TransportSchedule` | route (FK), departure_time, arrival_time, days_of_week |
| `SmartCard` | card_number, citizen (FK), balance, status |
| `Ticket` | ticket_number, citizen (FK), route (FK), payment_method, amount, qr_code |

## URLs

| Path | Description |
|---|---|
| `/` | Landing page |
| `/login/` | Login (National ID or admin username) |
| `/set-password/` | First-login password setup |
| `/user-dashboard/` | Citizen dashboard |
| `/dashboard/` | Admin dashboard |
| `/bus-tracking/` | Live GPS bus tracking map |
| `/api/bus-locations/` | JSON endpoint for bus positions |
| `/trip-planning/` | Search transport schedules |
| `/ticketing/` | Purchase e-tickets |
| `/citizens/` | Manage citizens |
| `/vehicles/` | Manage vehicles |
| `/signals/` | Manage traffic signals |
| `/routes/` | Manage transport routes |
| `/transport/` | Manage public transport |
| `/payments/` | Manage payments |
| `/staff/` | Manage staff |
| `/calculations/` | Manage calculations |
| `/schedules/` | Manage transport schedules |
| `/bus-locations/` | Manage GPS locations |
| `/tickets/` | Manage all tickets |
| `/smart-cards/` | Manage smart cards |
| `/logout/` | Sign out |

## GeoDjango (Production)

For production spatial queries (proximity searches, route calculations), switch to:

1. PostgreSQL with PostGIS extension
2. Update `DATABASES` engine to `django.contrib.gis.db.backends.postgis`
3. Add `django.contrib.gis` to `INSTALLED_APPS`
4. Change `BusLocation` lat/lng fields to `gis.PointField`
