import { useEffect, useState } from "react"
import "./App.css"

function App() {

  const [developers, setDevelopers] = useState([])
  const [tasks, setTasks] = useState([])
  const [assignments, setAssignments] = useState([])
  const [schedulerMessage, setSchedulerMessage] = useState("")
  const [isScheduling, setIsScheduling] = useState(false)
  const [activePage, setActivePage] = useState("Dashboard")
  const [developerName, setDeveloperName] = useState("")
  const [developerHours, setDeveloperHours] = useState("")
  const [developerSkills, setDeveloperSkills] = useState("")
  const [taskName, setTaskName] = useState("")
  const [taskSkill, setTaskSkill] = useState("")
  const [taskPriority, setTaskPriority] = useState("")
  const [taskHours, setTaskHours] = useState("")
  const [taskDeadline, setTaskDeadline] = useState("")
  const [dependencyTask, setDependencyTask] = useState("")
  const [dependencyOn, setDependencyOn] = useState("")
  const [dependencies, setDependencies] = useState([])

  const loadData = () => {

    fetch("http://127.0.0.1:8000/developers")
      .then(response => response.json())
      .then(data => setDevelopers(data))

    fetch("http://127.0.0.1:8000/tasks")
      .then(response => response.json())
      .then(data => setTasks(data))

    fetch("http://127.0.0.1:8000/assignments")
      .then(response => response.json())
      .then(data => setAssignments(data))

    fetch("http://127.0.0.1:8000/dependencies")
      .then(response => response.json())
      .then(data => setDependencies(data))
  }


  useEffect(() => {

    loadData()

  }, [])


  const assignedTasks = tasks.filter(
    task => task.status === "Assigned"
  )

  const pendingTasks = tasks.filter(
    task => task.status === "Pending"
  )

  const totalAvailableHours = developers.reduce(
    (total, developer) =>
      total + developer.available_hours,
    0
  )

  const totalAssignedHours = developers.reduce(
    (total, developer) =>
      total + developer.assigned_hours,
    0
  )

  const totalRemainingHours = developers.reduce(
    (total, developer) =>
      total + developer.remaining_hours,
    0
  )

  const handleRunScheduler = async () => {

    setIsScheduling(true)

    try {

      const response = await fetch(
        "http://127.0.0.1:8000/run-scheduler",
        {
          method: "POST"
        }
      )

      if (!response.ok) {
        throw new Error("Scheduler request failed")
      }

      const result = await response.json()

      setSchedulerMessage(
        `Scheduler completed — ${result.assigned_tasks} task(s) assigned.`
      )

      setTimeout(() => {
        loadData()
        setIsScheduling(false)
      }, 1800)

    } catch (error) {

      setSchedulerMessage(
        "Could not run the scheduler. Check that FastAPI is running."
      )

      setIsScheduling(false)
    }
  }
  const handleAddDeveloper = async (event) => {

    event.preventDefault()

    const skills = developerSkills
      .split(",")
      .map(skill => skill.trim())
      .filter(skill => skill !== "")

    try {

      const response = await fetch(
        "http://127.0.0.1:8000/developers",
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json"
          },
          body: JSON.stringify({
            name: developerName,
            available_hours: Number(developerHours),
            skills: skills
          })
        }
      )

      if (!response.ok) {
        throw new Error("Failed to add developer")
      }

      setDeveloperName("")
      setDeveloperHours("")
      setDeveloperSkills("")

      loadData()

    } catch (error) {

      console.error(error)

    }
  }
  const handleAddTask = async (event) => {

    event.preventDefault()

    try {

      const response = await fetch(
        "http://127.0.0.1:8000/tasks",
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json"
          },
          body: JSON.stringify({
            name: taskName,
            required_skill: taskSkill,
            priority: taskPriority,
            hours: Number(taskHours),
            deadline: taskDeadline
          })
        }
      )

      if (!response.ok) {
        throw new Error("Failed to add task")
      }

      setTaskName("")
      setTaskSkill("")
      setTaskPriority("")
      setTaskHours("")
      setTaskDeadline("")

      loadData()

    } catch (error) {

      console.error(error)

    }
  }
  const handleAddDependency = async (event) => {

    event.preventDefault()

    try {

      const response = await fetch(
        "http://127.0.0.1:8000/dependencies",
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json"
          },
          body: JSON.stringify({
            task_id: Number(dependencyTask),
            dependency_task_id: Number(dependencyOn)
          })
        }
      )

      if (!response.ok) {
        throw new Error("Failed to add dependency")
      }

      setDependencyTask("")
      setDependencyOn("")

      loadData()

    } catch (error) {

      console.error(error)

    }
  }
  return (
    <div className="app">

      {/* Sidebar */}

      <aside className="sidebar">

        <h2>Smart Scheduler</h2>

        <nav>

          <button
            onClick={() => setActivePage("Dashboard")}
          >
            Dashboard
          </button>

          <button
            onClick={() => setActivePage("Tasks")}
          >
            Tasks
          </button>

          <button
            onClick={() => setActivePage("Developers")}
          >
            Developers
          </button>

          <button
            onClick={() => setActivePage("Assignments")}
          >
            Assignments
          </button>

        </nav>

      </aside>


      {/* Main Content */}

      <main className="main-content">

        <header className="header">

          <div>
            <h1>{activePage}</h1>
            <p>Smart Task Scheduler</p>
          </div>

          <button
            className="schedule-button"
            onClick={handleRunScheduler}
            disabled={isScheduling}
          >
            {isScheduling ? "Running..." : "Run Scheduler"}
          </button>
          {schedulerMessage && (
            <div className="scheduler-message">
              {schedulerMessage}
            </div>
          )}

        </header>


        {/* Dashboard */}

        {activePage === "Dashboard" && (

          <>

            <section className="stats">

              <div className="stat-card">
                <h3>Total Tasks</h3>
                <p>{tasks.length}</p>
              </div>

              <div className="stat-card">
                <h3>Assigned Tasks</h3>
                <p>{assignedTasks.length}</p>
              </div>

              <div className="stat-card">
                <h3>Developers</h3>
                <p>{developers.length}</p>
              </div>

              <div className="stat-card">
                <h3>Pending Tasks</h3>
                <p>{pendingTasks.length}</p>
              </div>

              <div className="stat-card">
                <h3>Available Hours</h3>
                <p>{totalAvailableHours}</p>
              </div>

              <div className="stat-card">
                <h3>Assigned Hours</h3>
                <p>{totalAssignedHours}</p>
              </div>

              <div className="stat-card">
                <h3>Remaining Hours</h3>
                <p>{totalRemainingHours}</p>
              </div>

            </section>


            <section className="dashboard-grid">

              <div className="panel">

                <h2>Recent Tasks</h2>

                {tasks.slice(0, 5).map(task => (

                  <div
                    className="task-row"
                    key={task.id}
                  >

                    <span>{task.name}</span>

                    <span
                      className={`status ${task.status
                        .toLowerCase()
                        .replaceAll(" ", "-")
                        }`}
                    >
                      {task.status}
                    </span>

                  </div>

                ))}

              </div>


              <div className="panel">

                <h2>Task Assignments</h2>

                {assignments.slice(0, 5).map(
                  (assignment, index) => (

                    <div
                      className="workload"
                      key={index}
                    >

                      <span>
                        {assignment.task}
                      </span>

                      <span>
                        {assignment.developer}
                      </span>

                    </div>

                  )
                )}

              </div>

            </section>

          </>

        )}


        {/* Tasks */}

        {activePage === "Tasks" && (

          <div className="panel">

            <h2>All Tasks</h2>
            <form onSubmit={handleAddTask} className="task-form">

              <input
                type="text"
                placeholder="Task name"
                value={taskName}
                onChange={(event) =>
                  setTaskName(event.target.value)
                }
                required
              />

              <input
                type="text"
                placeholder="Required skill"
                value={taskSkill}
                onChange={(event) =>
                  setTaskSkill(event.target.value)
                }
                required
              />

              <select
                value={taskPriority}
                onChange={(event) =>
                  setTaskPriority(event.target.value)
                }
                required
              >
                <option value="">Select priority</option>
                <option value="High">High</option>
                <option value="Medium">Medium</option>
                <option value="Low">Low</option>
              </select>

              <input
                type="number"
                placeholder="Hours"
                value={taskHours}
                onChange={(event) =>
                  setTaskHours(event.target.value)
                }
                min="1"
                required
              />

              <input
                type="date"
                value={taskDeadline}
                onChange={(event) =>
                  setTaskDeadline(event.target.value)
                }
                required
              />

              <button type="submit">
                Add Task
              </button>

            </form>
            <form
              onSubmit={handleAddDependency}
              className="dependency-form"
            >

              <select
                value={dependencyTask}
                onChange={(event) =>
                  setDependencyTask(event.target.value)
                }
                required
              >
                <option value="">Select task</option>

                {tasks.map(task => (
                  <option
                    key={task.id}
                    value={task.id}
                  >
                    {task.name}
                  </option>
                ))}
              </select>


              <select
                value={dependencyOn}
                onChange={(event) =>
                  setDependencyOn(event.target.value)
                }
                required
              >
                <option value="">Depends on</option>

                {tasks.map(task => (
                  <option
                    key={task.id}
                    value={task.id}
                  >
                    {task.name}
                  </option>
                ))}
              </select>


              <button type="submit">
                Add Dependency
              </button>

            </form>

            <div className="panel dependency-panel">

              <h2>Task Dependencies</h2>

              {dependencies.length === 0 ? (

                <p>No dependencies added yet.</p>

              ) : (

                dependencies.map((dependency, index) => (

                  <div
                    className="dependency-row"
                    key={index}
                  >

                    <span>
                      {dependency.task}
                    </span>

                    <span>
                      depends on
                    </span>

                    <span>
                      {dependency.depends_on}
                    </span>

                  </div>

                ))

              )}

            </div>

            <table>

              <thead>

                <tr>
                  <th>Task</th>
                  <th>Skill</th>
                  <th>Priority</th>
                  <th>Hours</th>
                  <th>Deadline</th>
                  <th>Status</th>
                </tr>

              </thead>

              <tbody>

                {tasks.map(task => (

                  <tr key={task.id}>

                    <td>{task.name}</td>
                    <td>{task.required_skill}</td>
                    <td>{task.priority}</td>
                    <td>{task.hours}</td>
                    <td>{task.deadline}</td>
                    <td>{task.status}</td>

                  </tr>

                ))}

              </tbody>

            </table>

          </div>

        )}


        {/* Developers */}

        {activePage === "Developers" && (

          <div className="panel">

            <h2>Developers</h2>
            <form onSubmit={handleAddDeveloper} className="developer-form">

              <input
                type="text"
                placeholder="Developer name"
                value={developerName}
                onChange={(event) =>
                  setDeveloperName(event.target.value)
                }
                required
              />

              <input
                type="number"
                placeholder="Available hours"
                value={developerHours}
                onChange={(event) =>
                  setDeveloperHours(event.target.value)
                }
                min="1"
                required
              />

              <input
                type="text"
                placeholder="Skills (e.g. Python, SQL)"
                value={developerSkills}
                onChange={(event) =>
                  setDeveloperSkills(event.target.value)
                }
                required
              />

              <button type="submit">
                Add Developer
              </button>

            </form>
            <table>

              <thead>

                <tr>
                  <th>Name</th>
                  <th>Skills</th>
                  <th>Available Hours</th>
                  <th>Assigned Hours</th>
                  <th>Remaining Hours</th>
                  <th>Workload</th>
                </tr>

              </thead>

              <tbody>

                {developers.map(developer => (

                  <tr key={developer.id}>

                    <td>{developer.name}</td>

                    <td>
                      {developer.skills.join(", ")}
                    </td>

                    <td>
                      {developer.available_hours}
                    </td>

                    <td>
                      {developer.assigned_hours}
                    </td>

                    <td>
                      {developer.remaining_hours}
                    </td>

                    <td>
                      {developer.workload}%
                    </td>


                  </tr>

                ))}

              </tbody>

            </table>

          </div>

        )}


        {/* Assignments */}

        {activePage === "Assignments" && (

          <div className="panel">

            <h2>Task Assignments</h2>

            <table>

              <thead>

                <tr>
                  <th>Task</th>
                  <th>Developer</th>
                  <th>Assigned Hours</th>
                </tr>

              </thead>

              <tbody>

                {assignments.map(
                  (assignment, index) => (

                    <tr key={index}>

                      <td>{assignment.task}</td>

                      <td>
                        {assignment.developer}
                      </td>

                      <td>{assignment.assigned_hours}</td>

                    </tr>

                  )
                )}

              </tbody>

            </table>

          </div>

        )}

      </main>

    </div>
  )
}

export default App