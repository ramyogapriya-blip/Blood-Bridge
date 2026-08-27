# BloodBridge 🩸

BloodBridge is a simple blood donor discovery and emergency blood-request web application built with Flask and SQLite.

## Features
- Register blood donors
- Search available donors by blood group and city
- Post blood requests
- View open blood requests
- Responsive UI
- SQLite database with automatic table creation
- Render-ready deployment configuration
- No API keys required

## Run locally

```bash
python -m venv venv
```

Windows:
```bash
venv\Scripts\activate
```

Then:
```bash
pip install -r requirements.txt
python app.py
```

Open `http://127.0.0.1:5000`

## Deploy on Render

1. Push this project to a GitHub repository.
2. On Render, create **New → Web Service**.
3. Connect the GitHub repository.
4. Render can use the included `render.yaml`, or set:
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `gunicorn app:app`
5. Deploy.

## Important
This is a portfolio/demo project. It does not verify donors, hospitals, blood availability, medical eligibility, or emergency claims. Do not use it as a substitute for a hospital, blood bank, ambulance service, or medical professional. Avoid entering real sensitive patient information in a public deployment.
