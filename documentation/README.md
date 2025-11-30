# Facial Attendance System

Structure: Django backend + simple HTML/CSS/JS frontend. Images are sent as binary blobs (no Base64) from browser canvas via `canvas.toBlob()` -> `FormData` -> POST.

## Quick setup (summary)
1. Create virtualenv and activate.
2. Install requirements: `pip install -r requirements.txt`
3. Configure MySQL and update `facial_attendance/settings.py` with DB credentials.
4. Run `database/mysql_setup.sql` in your MySQL server or allow Django to create tables via migrations.
5. Run:
