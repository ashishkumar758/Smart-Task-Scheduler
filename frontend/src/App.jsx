import { useEffect, useState } from "react"
import "./App.css"

function App() {

  const [developers, setDevelopers] = useState([])
  const [tasks, setTasks] = useState([])
  const [assignments, setAssignments] = useState([])
  const [schedulerMessage, setSchedulerMessage] = useState("")

  const [activePage, setActivePage] = useState("Dashboard")


  useEffect(() => {

    fetch("http://127.0.0.1:8000/developers")
      .then(response => response.json())
      .then(data => setDevelopers(data))

    fetch("http://127.0.0.1:8000/tasks")
      .then(response => response.json())
      .then(data => setTasks(data))

    fetch("http://127.0.0.1:8000/assignments")
      .then(response => response.json())
      .then(data => setAssignments(data))

  }, [])


  const assignedTasks = tasks.filter(
    task => task.status === "Assigned"
  )

  const pendingTasks = tasks.filter(
    task => task.status === "Pending"
  )

  const handleRunScheduler = async () => {

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
        window.location.reload()
      }, 1800)

    } catch (error) {

      setSchedulerMessage(
        "Could not run the scheduler. Check that FastAPI is running."
      )
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
          >
            Run Scheduler
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
                      className={`status ${task.status === "Assigned"
                        ? "assigned"
                        : "blocked"
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

            <table>

              <thead>

                <tr>
                  <th>Name</th>
                  <th>Skills</th>
                  <th>Available Hours</th>
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