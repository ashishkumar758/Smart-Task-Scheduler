import sqlite3

def create_database():

    connection = sqlite3.connect(
        "smart_scheduler.db"
    )

    cursor = connection.cursor()


    # ==============================
    # DEVELOPERS TABLE
    # ==============================

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS developers (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            name TEXT NOT NULL,

            available_hours INTEGER NOT NULL

        )
        """
    )


    # ==============================
    # SKILLS TABLE
    # ==============================

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS skills (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            developer_id INTEGER NOT NULL,

            skill TEXT NOT NULL,

            FOREIGN KEY (developer_id)
            REFERENCES developers(id)

        )
        """
    )


    # ==============================
    # TASKS TABLE
    # ==============================

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS tasks (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            name TEXT NOT NULL,

            required_skill TEXT NOT NULL,

            priority TEXT NOT NULL,

            hours INTEGER NOT NULL,

            deadline TEXT NOT NULL,

            status TEXT DEFAULT 'Pending'

        )
        """
    )


    # ==============================
    # DEPENDENCIES TABLE
    # ==============================

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS dependencies (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            task_id INTEGER NOT NULL,

            dependency_task_id INTEGER NOT NULL,

            FOREIGN KEY (task_id)
            REFERENCES tasks(id),

            FOREIGN KEY (dependency_task_id)
            REFERENCES tasks(id)

        )
        """
    )


    # ==============================
    # TASK ASSIGNMENTS TABLE
    # ==============================

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS task_assignments (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            task_id INTEGER NOT NULL,

            developer_id INTEGER NOT NULL,

            assigned_hours INTEGER NOT NULL,

            FOREIGN KEY (task_id)
            REFERENCES tasks(id),

            FOREIGN KEY (developer_id)
            REFERENCES developers(id)

        )
        """
    )


    connection.commit()

    connection.close()


    print(
        "Database and tables created successfully."
    )


def add_developer(name, available_hours):

    connection = sqlite3.connect(
        "smart_scheduler.db"
    )

    cursor = connection.cursor()

    cursor.execute(
        """
        INSERT INTO developers (
            name,
            available_hours
        )

        VALUES (?, ?)
        """,
        (
            name,
            available_hours
        )
    )

    developer_id = cursor.lastrowid # it will return the id of the last inserted row

    connection.commit()

    connection.close()

    return developer_id

def add_skill(developer_id, skill):

    connection = sqlite3.connect(
        "smart_scheduler.db"
    )

    cursor = connection.cursor()

    cursor.execute(
        """
        INSERT INTO skills (
            developer_id,
            skill
        )

        VALUES (?, ?)
        """,
        (
            developer_id,
            skill
        )
    )

    connection.commit()

    connection.close()

def add_task(
    name,
    required_skill,
    priority,
    hours,
    deadline
):

    connection = sqlite3.connect(
        "smart_scheduler.db"
    )

    cursor = connection.cursor()

    cursor.execute(
        """
        INSERT INTO tasks (
            name,
            required_skill,
            priority,
            hours,
            deadline
        )

        VALUES (?, ?, ?, ?, ?)
        """,
        (
            name,
            required_skill,
            priority,
            hours,
            deadline
        )
    )

    task_id = cursor.lastrowid

    connection.commit()

    connection.close()

    return task_id

def add_dependency(
    task_id,
    dependency_task_id
):

    connection = sqlite3.connect(
        "smart_scheduler.db"
    )

    cursor = connection.cursor()

    cursor.execute(
        """
        INSERT INTO dependencies (
            task_id,
            dependency_task_id
        )

        VALUES (?, ?)
        """,
        (
            task_id,
            dependency_task_id
        )
    )

    connection.commit()

    connection.close()

def get_task_dependencies():

    connection = sqlite3.connect(
        "smart_scheduler.db"
    )

    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT
            dependencies.task_id,
            tasks.name,
            dependencies.dependency_task_id,
            dependency_tasks.name

        FROM dependencies

        JOIN tasks
        ON dependencies.task_id = tasks.id

        JOIN tasks AS dependency_tasks
        ON dependencies.dependency_task_id = dependency_tasks.id
        """
    )

    dependencies = cursor.fetchall()

    connection.close()

    return dependencies

def clear_database():

    connection = sqlite3.connect(
        "smart_scheduler.db"
    )

    cursor = connection.cursor()

    cursor.execute(
        "DELETE FROM task_assignments"
    )

    cursor.execute(
        "DELETE FROM dependencies"
    )

    cursor.execute(
        "DELETE FROM tasks"
    )

    cursor.execute(
        "DELETE FROM skills"
    )

    cursor.execute(
        "DELETE FROM developers"
    )

    connection.commit()

    connection.close()

def update_task_status(task_id, status):

    connection = sqlite3.connect(
        "smart_scheduler.db"
    )

    cursor = connection.cursor()

    cursor.execute(
        """
        UPDATE tasks

        SET status = ?

        WHERE id = ?
        """,
        (
            status,
            task_id
        )
    )

    connection.commit()

    connection.close()

def add_task_assignment(
    task_id,
    developer_id,
    assigned_hours
):

    connection = sqlite3.connect(
        "smart_scheduler.db"
    )

    cursor = connection.cursor()

    cursor.execute(
        """
        INSERT INTO task_assignments (
            task_id,
            developer_id,
            assigned_hours
        )

        VALUES (?, ?, ?)
        """,
        (
            task_id,
            developer_id,
            assigned_hours
        )
    )

    connection.commit()

    connection.close()

def get_all_developers():

    connection = sqlite3.connect(
        "smart_scheduler.db"
    )

    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT
            id,
            name,
            available_hours

        FROM developers
        """
    )

    developers = cursor.fetchall()

    connection.close()

    return developers

def get_all_tasks():

    connection = sqlite3.connect(
        "smart_scheduler.db"
    )

    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT
            id,
            name,
            required_skill,
            priority,
            hours,
            deadline,
            status

        FROM tasks
        """
    )

    tasks = cursor.fetchall()

    connection.close()

    return tasks

def get_task_assignments():

    connection = sqlite3.connect(
        "smart_scheduler.db"
    )

    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT
            tasks.name,
            developers.name,
            task_assignments.assigned_hours

        FROM task_assignments

        JOIN tasks
        ON task_assignments.task_id = tasks.id

        JOIN developers
        ON task_assignments.developer_id = developers.id
        """
    )

    assignments = cursor.fetchall()

    connection.close()

    return assignments

def get_developer_assigned_hours():

    connection = sqlite3.connect(
        "smart_scheduler.db"
    )

    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT
            developer_id,
            SUM(assigned_hours)

        FROM task_assignments

        GROUP BY developer_id
        """
    )

    rows = cursor.fetchall()

    connection.close()

    assigned_hours = {}

    for row in rows:

        developer_id = row[0]
        hours = row[1]

        assigned_hours[developer_id] = hours

    return assigned_hours

def get_developers_with_skills():

    connection = sqlite3.connect(
        "smart_scheduler.db"
    )

    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT
            developers.id,
            developers.name,
            developers.available_hours,
            skills.skill

        FROM developers

        LEFT JOIN skills
        ON developers.id = skills.developer_id
        """
    )

    rows = cursor.fetchall()

    connection.close()

    developers = {}

    for row in rows:

        developer_id = row[0]
        developer_name = row[1]
        available_hours = row[2]
        skill = row[3]

        if developer_id not in developers:

            developers[developer_id] = {

                "name": developer_name,

                "available_hours": available_hours,

                "skills": []

            }

        if skill:

            developers[developer_id][
                "skills"
            ].append(skill)

    return developers