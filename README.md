# CareConnect

A small FastAPI demo that ranks clinic patients for vaccination outreach and lets a patient look up their own record.

Built at a hackathon by a team of five.

All patient data is randomly generated when the server starts. Nothing here is real medical data, and the scoring is a demonstration, not clinical guidance.

## What It Does

- **Staff dashboard** (`/staff`): every patient, ranked by an outreach priority score from 0 to 100, with the reasons behind the score and a button that copies a reminder message.
- **Patient portal** (`/patient`): a patient enters their name and ID and sees vaccines taken, vaccines due, and risk factors.

## How It Works

1. On startup, `careConnect.py` reads the vaccine codes from `Vaccination schedule.csv` with pandas and generates one random patient per row: age, sex, vaccines taken, vaccines due, and risk factors.
2. `scoring.py` scores each patient from three parts:
   - **Age** (up to 0.40): highest for children under 5 and adults 95+, lowest for adults 18–64.
   - **Risk factors** (up to about 0.13): immunocompromised, chronic disease, pregnancy.
   - **Vaccination gap** (up to 0.30): fewer vaccines on record means a higher score.
3. Patients are pushed onto a heap keyed on the negated score, so the dashboard pops them in priority order.
4. FastAPI renders both pages with Jinja2 templates.

Patients are held in memory. There is no database, and the data is regenerated on every restart.

## Tech Stack

Python · FastAPI · Jinja2 · pandas · HTML/CSS

## Run It

```bash
pip install fastapi uvicorn jinja2 pandas python-multipart
uvicorn main:app --reload
```

Then open `http://127.0.0.1:8000`. To try the patient portal, copy a name and ID from the staff dashboard.

## Project Structure

```text
main.py            routes and view models
careConnect.py     random patient generation from the vaccine schedule
scoring.py         priority score and heap
PatientProfile.py  patient data class
templates/         landing, patient, and staff pages
static/            stylesheet and clipboard helper
```

## Limitations

- No authentication: the staff dashboard is open to anyone who can reach the server.
- "Vaccines due" is chosen at random from the vaccines a patient has not taken. The age and target-group rules in the CSV are not applied.
- The score weights are hand-picked.
