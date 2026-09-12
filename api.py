from fastapi import FastAPI
from main import run_scheduler
from fastapi.middleware.cors import CORSMiddleware
from database import (
    get_all_developers,
    get_all_tasks,
    get_task_assignments,
    get_developers_with_skills
)
from scheduler import (
    calculate_skill_count,
    calculate_specialization,
    schedule_tasks
)
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/run-scheduler")
def run_scheduler_endpoint():

    return run_scheduler()

@app.get("/")
def home():

    return {
        "message": "Smart Task Scheduler API is running"
    }
@app.get("/developers")
def get_developers():

    developers = get_developers_with_skills()

    result = []

    for developer in developers.values():

        result.append({
            "id": developer["name"],
            "name": developer["name"],
            "skills": developer["skills"],
            "available_hours": developer["available_hours"]
        })

    return result
@app.get("/tasks")
def get_tasks():

    tasks = get_all_tasks()

    result = []

    for task in tasks:

        result.append({
            "id": task[0],
            "name": task[1],
            "required_skill": task[2],
            "priority": task[3],
            "hours": task[4],
            "deadline": task[5],
            "status": task[6]
        })

    return result

@app.get("/assignments")
def get_assignments():

    assignments = get_task_assignments()

    result = []

    for assignment in assignments:

        result.append({
            "task": assignment[0],
            "developer": assignment[1]
        })

    return result
