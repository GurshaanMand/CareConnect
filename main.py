from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

import heapq
import random

from PatientProfile import PatientProfile
from careConnect import buildPatients
from scoring import priorityHeap

# from brain


app = FastAPI()

# Templates + static files
templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

# In-memory demo database
patients_db = buildPatients()


class PatientView:
    def __init__(self, p: PatientProfile):
        self.id = p.id
        self.name = p.name
        self.age = p.age

        self.vaccines = list(getattr(p, "vaccines", []))
        self.risk_factors = list(getattr(p, "riskFactors", []))
        self.due_vaccines = list(getattr(p, "dueVaccines", []))

@app.post("/patient", response_class=HTMLResponse)
def patient_post(
    request: Request,
    name: str = Form(...),
    pid: str = Form(...)
):
    found = None

    for p in patients_db:
        if str(p.id).strip() == pid.strip() and \
           p.name.strip().lower() == name.strip().lower():
            found = p
            break

    if not found:
        return templates.TemplateResponse("patient.html", {
            "request": request,
            "patient": None,
            "due_vaccines": [],
            "due_reasons": [],
            "error": "No matching record found."
        })

    return templates.TemplateResponse("patient.html", {
    "request": request,
    "patient": PatientView(found),
    "due_vaccines": getattr(found, "dueVaccines", []),
    "due_reasons": []
})

def ranked_patients():
    """
    Returns [(PatientView, score_int_0_100, reasons_list)]
    sorted highest priority first.
    """
    heap = priorityHeap(patients_db)

    out = []
    temp = list(heap)
    heapq.heapify(temp)

    while temp:
        neg_score, _, p, reasons = heapq.heappop(temp)
        score = -neg_score
        score100 = int(round(score * 100))
        out.append((PatientView(p), score100, reasons))

    return out


def parse_semicolon_list(s: str):
    s = (s or "").replace(",", ";")
    return [x.strip() for x in s.split(";") if x.strip()]


@app.get("/", response_class=HTMLResponse)
def landing(request: Request):
    return templates.TemplateResponse("landing.html", {
        "request": request
    })


@app.get("/staff", response_class=HTMLResponse)
def staff(request: Request):
    return templates.TemplateResponse("staff.html", {
        "request": request,
        "patients": ranked_patients(),
        "message": None,
        "error": None
    })


@app.get("/patient", response_class=HTMLResponse)
def patient_get(request: Request):
    return templates.TemplateResponse("patient.html", {
        "request": request,
        "patient": None,
        "error": None,
        "due_vaccines": [],
        "due_reasons": []
    })
