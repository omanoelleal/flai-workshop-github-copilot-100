"""
High School Management System API

A super simple FastAPI application that allows students to view and sign up
for extracurricular activities at Mergington High School.
"""

from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse
import os
from pathlib import Path

app = FastAPI(title="Escola do Futuro API",
              description="API para visualizar e se inscrever em atividades extracurriculares inovadoras")

# Mount the static files directory
current_dir = Path(__file__).parent
app.mount("/static", StaticFiles(directory=os.path.join(Path(__file__).parent,
          "static")), name="static")
          

# In-memory activity database
activities = {
    "Chess Club": {
        "description": "Aprenda estratégias e compita em torneios de xadrez",
        "schedule": "Sextas-feiras, 15:30 - 17:00",
        "max_participants": 12,
        "participants": ["michael@escolafuturo.edu", "daniel@escolafuturo.edu"]
    },
    "Programação e IA": {
        "description": "Aprenda programação e inteligência artificial para o futuro",
        "schedule": "Terças e quintas, 15:30 - 16:30",
        "max_participants": 20,
        "participants": ["emma@escolafuturo.edu", "sophia@escolafuturo.edu"]
    },
    "Educação Física": {
        "description": "Atividades físicas e esportes para saúde e bem-estar",
        "schedule": "Segundas, quartas e sextas, 14:00 - 15:00",
        "max_participants": 30,
        "participants": ["john@escolafuturo.edu", "olivia@escolafuturo.edu"]
    },
    "Basquete": {
        "description": "Basquete competitivo com treinamentos e jogos",
        "schedule": "Segundas e quartas, 16:00 - 17:30",
        "max_participants": 15,
        "participants": ["alex@escolafuturo.edu", "jordan@escolafuturo.edu"]
    },
    "Tênis": {
        "description": "Aprenda técnicas de tênis e compete em partidas",
        "schedule": "Terças e quintas, 16:00 - 17:00",
        "max_participants": 10,
        "participants": ["sarah@escolafuturo.edu"]
    },
    "Estúdio de Arte Digital": {
        "description": "Explore pintura digital, design e técnicas de arte moderna",
        "schedule": "Quartas e sextas, 15:30 - 17:00",
        "max_participants": 18,
        "participants": ["maya@escolafuturo.edu", "lucas@escolafuturo.edu"]
    },
    "Banda Musical": {
        "description": "Toque em banda escolar e apresente em eventos",
        "schedule": "Segundas e sextas, 16:00 - 17:00",
        "max_participants": 25,
        "participants": ["evan@escolafuturo.edu", "isabella@escolafuturo.edu"]
    },
    "Clube de Robótica": {
        "description": "Construa e programe robôs para competições inovadoras",
        "schedule": "Terças e quintas, 16:30 - 18:00",
        "max_participants": 16,
        "participants": ["aiden@escolafuturo.edu", "chloe@escolafuturo.edu"]
    },
    "Olimpíada de Ciências": {
        "description": "Participe em eventos científicos e experimentos práticos",
        "schedule": "Quartas, 15:30 - 17:00",
        "max_participants": 14,
        "participants": ["noah@escolafuturo.edu", "ava@escolafuturo.edu"]
    }
}


@app.get("/")
def root():
    return RedirectResponse(url="/static/index.html")


@app.get("/activities")
def get_activities():
    return activities


@app.post("/activities/{activity_name}/signup")
def signup_for_activity(activity_name: str, email: str):
    """Sign up a student for an activity"""
    # Validate activity exists
    if activity_name not in activities:
        raise HTTPException(status_code=404, detail="Activity not found")

    # Get the specific activity
    activity = activities[activity_name]

    # Validate student is not already signed up
    if email in activity["participants"]:
        raise HTTPException(status_code=400, detail="Student already signed up")

    # Add student
    activity["participants"].append(email)
    return {"message": f"Signed up {email} for {activity_name}"}


@app.delete("/activities/{activity_name}/participants")
def remove_participant(activity_name: str, email: str):
    """Unregister a student from an activity"""
    if activity_name not in activities:
        raise HTTPException(status_code=404, detail="Activity not found")

    activity = activities[activity_name]

    if email not in activity["participants"]:
        raise HTTPException(status_code=404, detail="Participant not found")

    activity["participants"].remove(email)
    return {"message": f"Removed {email} from {activity_name}"}
