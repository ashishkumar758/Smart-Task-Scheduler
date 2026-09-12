from datetime import datetime


def dependencies_completed(task, completed_tasks):

    for dependency in task["dependencies"]:

        if dependency not in completed_tasks:
            return False

    return True


def deadline_passed(task):

    task_deadline = datetime.strptime(
        task["deadline"],
        "%Y-%m-%d"
    ).date()

    current_date = datetime.now().date()

    return current_date > task_deadline


def calculate_skill_count(developers):

    skill_count = {}

    for developer in developers:

        for skill in developer["skills"]:

            if skill not in skill_count:
                skill_count[skill] = 0

            skill_count[skill] += 1

    return skill_count


def calculate_specialization(developers, skill_count):

    for developer in developers:

        specialization_score = 0

        for skill in developer["skills"]:

            specialization_score += (
                1 / skill_count[skill]
            )

        developer[
            "specialization_score"
        ] = specialization_score


    specialization_scores = [

        developer["specialization_score"]

        for developer in developers

    ]


    min_specialization = min(
        specialization_scores
    )

    max_specialization = max(
        specialization_scores
    )


    return (
        min_specialization,
        max_specialization
    )


def calculate_developer_score(
    developer,
    task,
    skill_count,
    min_specialization,
    max_specialization
):

    remaining_hours = (
        developer["available_hours"]
        - developer["assigned_hours"]
    )

    workload = (
        developer["assigned_hours"]
        / developer["available_hours"]
    )

    workload_factor = 1 - workload

    capacity_factor = (
        remaining_hours
        / developer["available_hours"]
    )

    if max_specialization == min_specialization:

        specialization_factor = 1

    else:

        specialization_factor = (
            max_specialization
            - developer["specialization_score"]
        ) / (
            max_specialization
            - min_specialization
        )

    scarcity_factor = (
        1 / skill_count[task["required_skill"]]
    )

    score = (
        0.40 * specialization_factor
        + 0.30 * workload_factor
        + 0.20 * capacity_factor
        + 0.10 * scarcity_factor
    )

    return score

def schedule_tasks(
    developers,
    tasks,
    skill_count,
    min_specialization,
    max_specialization
):

    completed_tasks = []

    remaining_tasks = tasks.copy()

    task_status = {}

    task_assignment = {}

    for task in tasks:

        task_status[
            task["name"]
        ] = "Pending"


    for developer in developers:

        developer["assigned_hours"] = 0


    while remaining_tasks:

        progress = False


        for task in remaining_tasks.copy():

            # Check deadline
            if deadline_passed(task):

                task_status[
                    task["name"]
                ] = "Deadline Passed"

                remaining_tasks.remove(task)

                print(
                    "\nTask:",
                    task["name"]
                )

                print(
                    "Status: Deadline Passed"
                )

                progress = True

                continue


            # Check dependencies
            if not dependencies_completed(
                task,
                completed_tasks
            ):

                task_status[
                    task["name"]
                ] = "Blocked"

                print(
                    "\nTask:",
                    task["name"]
                )

                print(
                    "Status: Blocked by dependency"
                )

                continue


            best_developer = None

            best_score = -1

            skill_available = False

            capacity_available = False


            for developer in developers:

                has_skill = (
                    task["required_skill"]
                    in developer["skills"]
                )


                if has_skill:

                    skill_available = True


                remaining_hours = (
                    developer["available_hours"]
                    - developer["assigned_hours"]
                )


                has_capacity = (
                    remaining_hours
                    >= task["hours"]
                )


                if has_skill and has_capacity:

                    capacity_available = True


                    score = (
                        calculate_developer_score(
                            developer,
                            task,
                            skill_count,
                            min_specialization,
                            max_specialization
                        )
                    )


                    if score > best_score:

                        best_developer = developer

                        best_score = score


            # Assign task
            if best_developer:

                best_developer[
                    "assigned_hours"
                ] += task["hours"]


                completed_tasks.append(
                    task["name"]
                )


                remaining_tasks.remove(task)


                task_status[
                    task["name"]
                ] = "Assigned"


                task_assignment[
                    task["name"]
                ] = best_developer["name"]


                progress = True


                print(
                    "\nTask:",
                    task["name"]
                )

                print(
                    "Assigned to:",
                    best_developer["name"]
                )

                print(
                    "Best score:",
                    best_score
                )


            else:

                task_status[
                    task["name"]
                ] = "Cannot Assign"


                print(
                    "\nTask:",
                    task["name"]
                )


                if not skill_available:

                    print(
                        "Reason: No developer has the required skill"
                    )


                elif not capacity_available:

                    print(
                        "Reason: Developers with this skill do not have enough hours"
                    )


                remaining_tasks.remove(task)

                progress = True


        if not progress:

            break


    return (
        task_status,
        task_assignment,
        developers
    )