from copy import deepcopy

from database import (
    create_database,
    clear_database,
    add_developer,
    add_skill,
    add_task,
    add_dependency,
    update_task_status,
    add_task_assignment,
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


# ==========================================
# DEVELOPERS DATA
# ==========================================

developers = [
    {
        "name": "Rahul",
        "skills": ["Python", "SQL"],
        "available_hours": 8
    },
    {
        "name": "Aman",
        "skills": ["React", "JavaScript"],
        "available_hours": 6
    },
    {
        "name": "Priya",
        "skills": ["Python", "React"],
        "available_hours": 7
    },
    {
        "name": "Neha",
        "skills": ["JavaScript", "HTML", "CSS"],
        "available_hours": 8
    },
    {
        "name": "Arjun",
        "skills": ["Python", "FastAPI"],
        "available_hours": 6
    },
    {
        "name": "Sneha",
        "skills": ["SQL", "Python"],
        "available_hours": 5
    },
    {
        "name": "Vikram",
        "skills": ["React", "Node.js"],
        "available_hours": 7
    }
]


# ==========================================
# TASKS DATA
# ==========================================

tasks = [
    {
        "name": "Database Setup",
        "required_skill": "SQL",
        "priority": "High",
        "hours": 4,
        "deadline": "2026-09-27",
        "dependencies": []
    },
    {
        "name": "UI Design",
        "required_skill": "Canva",
        "priority": "High",
        "hours": 4,
        "deadline": "2026-09-27",
        "dependencies": []
    },
    {
        "name": "Authentication API",
        "required_skill": "Python",
        "priority": "High",
        "hours": 5,
        "deadline": "2026-09-28",
        "dependencies": ["Database Setup"]
    },
    {
        "name": "User Registration API",
        "required_skill": "FastAPI",
        "priority": "High",
        "hours": 3,
        "deadline": "2026-09-28",
        "dependencies": ["Authentication API"]
    },
    {
        "name": "Login Page",
        "required_skill": "React",
        "priority": "High",
        "hours": 3,
        "deadline": "2026-09-29",
        "dependencies": ["Authentication API"]
    },
    {
        "name": "Dashboard",
        "required_skill": "React",
        "priority": "Medium",
        "hours": 4,
        "deadline": "2026-09-30",
        "dependencies": ["Login Page"]
    },
    {
        "name": "API Integration",
        "required_skill": "JavaScript",
        "priority": "Medium",
        "hours": 3,
        "deadline": "2026-09-30",
        "dependencies": [
            "User Registration API",
            "Login Page"
        ]
    },
    {
        "name": "Database Optimization",
        "required_skill": "SQL",
        "priority": "Medium",
        "hours": 3,
        "deadline": "2026-09-18",
        "dependencies": ["Database Setup"]
    },
    {
        "name": "Frontend Styling",
        "required_skill": "CSS",
        "priority": "Low",
        "hours": 2,
        "deadline": "2026-09-23",
        "dependencies": ["Login Page"]
    },
    {
        "name": "Backend Testing",
        "required_skill": "Python",
        "priority": "Medium",
        "hours": 3,
        "deadline": "2026-09-28",
        "dependencies": ["Authentication API"]
    },
    {
        "name": "Deployment Setup",
        "required_skill": "Node.js",
        "priority": "High",
        "hours": 3,
        "deadline": "2026-09-23",
        "dependencies": [
            "Dashboard",
            "API Integration"
        ]
    }
]


# ==========================================
# RUN SCHEDULER
# ==========================================

def run_scheduler():

    # Each scheduler run starts with fresh developer/task data.
    scheduled_developers = deepcopy(developers)
    scheduled_tasks = deepcopy(tasks)

    # ==========================================
    # DATABASE INITIALIZATION
    # ==========================================

    create_database()

    clear_database()

    # ==========================================
    # SAVE DEVELOPERS TO DATABASE
    # ==========================================

    developer_ids = {}

    for developer in developers:

        developer_id = add_developer(
            developer["name"],
            developer["available_hours"]
        )

        developer_ids[developer["name"]] = developer_id

        for skill in developer["skills"]:

            add_skill(
                developer_id,
                skill
            )

    # ==========================================
    # SAVE TASKS TO DATABASE
    # ==========================================

    task_ids = {}

    for task in tasks:

        task_id = add_task(
            task["name"],
            task["required_skill"],
            task["priority"],
            task["hours"],
            task["deadline"]
        )

        task_ids[task["name"]] = task_id

    # ==========================================
    # SAVE TASK DEPENDENCIES TO DATABASE
    # ==========================================

    for task in tasks:

        task_id = task_ids[task["name"]]

        for dependency_name in task["dependencies"]:

            dependency_task_id = task_ids[dependency_name]

            add_dependency(
                task_id,
                dependency_task_id
            )

    # ==========================================
    # CALCULATE SKILL AVAILABILITY
    # ==========================================

    skill_count = calculate_skill_count(
        scheduled_developers
    )

    # ==========================================
    # CALCULATE SPECIALIZATION
    # ==========================================

    min_specialization, max_specialization = (
        calculate_specialization(
            scheduled_developers,
            skill_count
        )
    )

    # ==========================================
    # SCHEDULE TASKS
    # ==========================================

    task_status, task_assignment, scheduled_developers = (
        schedule_tasks(
            scheduled_developers,
            scheduled_tasks,
            skill_count,
            min_specialization,
            max_specialization
        )
    )

    # ==========================================
    # SAVE SCHEDULER RESULTS TO DATABASE
    # ==========================================

    for task in tasks:

        task_name = task["name"]

        task_id = task_ids[task_name]

        status = task_status[task_name]

        update_task_status(
            task_id,
            status
        )

        if task_name in task_assignment:

            developer_name = task_assignment[task_name]

            developer_id = developer_ids[developer_name]

            add_task_assignment(
                task_id,
                developer_id,
                task["hours"]
            )

    # ==========================================
    # FINAL TASK REPORT
    # ==========================================

    print("\nFINAL TASK REPORT")

    for task in tasks:

        task_name = task["name"]

        print("\nTask:", task_name)

        print(
            "Status:",
            task_status[task_name]
        )

        if task_name in task_assignment:

            print(
                "Assigned Developer:",
                task_assignment[task_name]
            )

    # ==========================================
    # DEVELOPER WORKLOAD REPORT
    # ==========================================

    print("\nDEVELOPER WORKLOAD REPORT")

    for developer in scheduled_developers:

        assigned_hours = developer["assigned_hours"]

        available_hours = developer["available_hours"]

        remaining_hours = (
            available_hours
            - assigned_hours
        )

        workload_percentage = (
            assigned_hours
            / available_hours
        ) * 100

        print(
            "\nDeveloper:",
            developer["name"]
        )

        print(
            "Assigned Hours:",
            assigned_hours
        )

        print(
            "Available Hours:",
            available_hours
        )

        print(
            "Remaining Hours:",
            remaining_hours
        )

        print(
            "Workload:",
            round(workload_percentage, 2),
            "%"
        )

    # ==========================================
    # PROJECT SUMMARY
    # ==========================================

    print("\nPROJECT SUMMARY")

    total_tasks = len(tasks)

    assigned_tasks = 0
    cannot_assign_tasks = 0
    blocked_tasks = 0
    pending_tasks = 0
    deadline_passed_tasks = 0

    for task in tasks:

        task_name = task["name"]

        status = task_status[task_name]

        if status == "Assigned":

            assigned_tasks += 1

        elif status == "Cannot Assign":

            cannot_assign_tasks += 1

        elif status == "Blocked":

            blocked_tasks += 1

        elif status == "Pending":

            pending_tasks += 1

        elif status == "Deadline Passed":

            deadline_passed_tasks += 1

    print("Total Tasks:", total_tasks)
    print("Assigned Tasks:", assigned_tasks)
    print("Cannot Assign Tasks:", cannot_assign_tasks)
    print("Blocked Tasks:", blocked_tasks)
    print("Pending Tasks:", pending_tasks)
    print("Deadline Passed Tasks:", deadline_passed_tasks)

    # ==========================================
    # DATABASE REPORT
    # ==========================================

    print("\nDATABASE DEVELOPERS")

    developers_data = get_all_developers()

    for developer in developers_data:
        print(developer)

    print("\nDATABASE TASKS")

    tasks_data = get_all_tasks()

    for task in tasks_data:
        print(task)

    print("\nDATABASE ASSIGNMENTS")

    assignments_data = get_task_assignments()

    for assignment in assignments_data:
        print(assignment)

    print("\nDEVELOPERS WITH SKILLS")

    developers_with_skills = get_developers_with_skills()

    for developer_id, developer in developers_with_skills.items():

        print("\nID:", developer_id)

        print("Name:", developer["name"])

        print(
            "Available Hours:",
            developer["available_hours"]
        )

        print("Skills:", developer["skills"])

    return {
        "message": "Scheduler completed successfully",
        "total_tasks": total_tasks,
        "assigned_tasks": assigned_tasks,
        "cannot_assign_tasks": cannot_assign_tasks,
        "blocked_tasks": blocked_tasks,
        "pending_tasks": pending_tasks,
        "deadline_passed_tasks": deadline_passed_tasks
    }


if __name__ == "__main__":
    run_scheduler()