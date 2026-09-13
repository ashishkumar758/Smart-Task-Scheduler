from fastapi import FastAPI
from pydantic import BaseModel
from main import run_scheduler
from fastapi.middleware.cors import CORSMiddleware
from database import (
    get_all_developers,
    get_all_tasks,
    get_task_assignments,
    get_developers_with_skills,
    get_developer_assigned_hours,
    add_developer,
    add_skill,
    add_task,
    add_dependency,
    get_task_dependencies
)
from scheduler import (
    calculate_skill_count,
    calculate_specialization,
    schedule_tasks
)
class Developer(BaseModel):
    name: str
    available_hours: int
    skills: list[str]

class Dependency(BaseModel):
    task_id: int
    dependency_task_id: int

class Task(BaseModel):
    name: str
    required_skill: str
    priority: str
    hours: int
    deadline: str
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

    assigned_hours = get_developer_assigned_hours()

    result = []

    for developer_id, developer in developers.items():

        assigned = assigned_hours.get(
            developer_id,
            0
        )

        remaining = (
            developer["available_hours"]
            - assigned
        )

        workload = (
            assigned
            / developer["available_hours"]
        ) * 100

        result.append({
            "id": developer_id,
            "name": developer["name"],
            "skills": developer["skills"],
            "available_hours": developer["available_hours"],
            "assigned_hours": assigned,
            "remaining_hours": remaining,
            "workload": round(workload, 2)
        })

    return result
@app.post("/developers")
def create_developer(developer: Developer):

    developer_id = add_developer(
        developer.name,
        developer.available_hours
    )

    for skill in developer.skills:
        add_skill(
            developer_id,
            skill
        )

    return {
        "message": "Developer added successfully",
        "id": developer_id
    }
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

@app.post("/tasks")
def create_task(task: Task):

    task_id = add_task(
        task.name,
        task.required_skill,
        task.priority,
        task.hours,
        task.deadline
    )

    return {
        "message": "Task added successfully",
        "id": task_id
    }

@app.post("/dependencies")
def create_dependency(dependency: Dependency):

    add_dependency(
        dependency.task_id,
        dependency.dependency_task_id
    )

    return {
        "message": "Dependency added successfully"
    }

@app.get("/dependencies")
def get_dependencies():

    dependencies = get_task_dependencies()

    result = []

    for dependency in dependencies:

        result.append({
            "task_id": dependency[0],
            "task": dependency[1],
            "dependency_task_id": dependency[2],
            "depends_on": dependency[3]
        })

    return result

@app.get("/assignments")
def get_assignments():

    assignments = get_task_assignments()

    result = []

    for assignment in assignments:

        result.append({
            "task": assignment[0],
            "developer": assignment[1],
            "assigned_hours": assignment[2]
        })

    return result
