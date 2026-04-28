import { useEffect, useState } from "react";
import TaskList from "./components/TaskList";
import TaskForm from "./components/TaskForm";
import TaskDetail from "./components/TaskDetail";

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || "http://localhost:5000";

export default function App() {
  const [tasks, setTasks] = useState([]);
  const [status, setStatus] = useState("loading");
  const [error, setError] = useState("");
  const [sortOrder, setSortOrder] = useState("high_to_low");
  const [selectedTaskId, setSelectedTaskId] = useState(null);

  useEffect(() => {
    async function loadTasks() {
      try {
        const response = await fetch(`${API_BASE_URL}/api/tasks`);

        if (!response.ok) {
          throw new Error(`Request failed with status ${response.status}`);
        }

        const data = await response.json();
        setTasks(data || []);
        setStatus("success");
        setError("");
      } catch (loadError) {
        setError(loadError.message || "Unable to reach the backend.");
        setStatus("error");
      }
    }

    loadTasks();
    const intervalId = window.setInterval(loadTasks, 2500);

    return () => window.clearInterval(intervalId);
  }, []);

  async function handleCreateTask(task) {
    setStatus("submitting");

    try {
      const response = await fetch(`${API_BASE_URL}/api/tasks`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(task),
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.error || `Request failed with status ${response.status}`);
      }

      setTasks((prev) => [...prev, data]);
      setStatus("success");
      setError("");
      return { ok: true };
    } catch (createError) {
      setStatus("error");
      setError(createError.message || "Unable to create task.");
      return { ok: false, error: createError.message };
    }
  }

  async function handleMoveTask(taskId, nextStatus) {
    const previousTask = tasks.find((task) => task.id === taskId);
    const previousStatus = previousTask?.status;

    setTasks((prev) =>
      prev.map((task) =>
        task.id === taskId
          ? {
              ...task,
              status: nextStatus,
            }
          : task,
      ),
    );

    try {
      const response = await fetch(`${API_BASE_URL}/api/tasks/${taskId}`, {
        method: "PUT",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ status: nextStatus }),
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.error || `Request failed with status ${response.status}`);
      }

      setTasks((prev) => prev.map((task) => (task.id === taskId ? data : task)));
      setSelectedTaskId((current) => (current === taskId ? data.id : current));
      setStatus("success");
      setError("");
    } catch (updateError) {
      setError(updateError.message || "Unable to update task.");
      setStatus("error");

      if (previousStatus) {
        setTasks((prev) =>
          prev.map((task) =>
            task.id === taskId
              ? {
                  ...task,
                  status: previousStatus,
                }
              : task,
          ),
        );
      }
    }
  }

  async function handleUpdateTaskPriority(taskId, nextPriority) {
    const previousTask = tasks.find((task) => task.id === taskId);
    const previousPriority = previousTask?.priority;

    setTasks((prev) =>
      prev.map((task) =>
        task.id === taskId
          ? {
              ...task,
              priority: nextPriority,
            }
          : task,
      ),
    );

    try {
      const response = await fetch(`${API_BASE_URL}/api/tasks/${taskId}`, {
        method: "PUT",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ priority: nextPriority }),
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.error || `Request failed with status ${response.status}`);
      }

      setTasks((prev) => prev.map((task) => (task.id === taskId ? data : task)));
      setSelectedTaskId((current) => (current === taskId ? data.id : current));
      setStatus("success");
      setError("");
    } catch (updateError) {
      setError(updateError.message || "Unable to update task priority.");
      setStatus("error");

      if (previousPriority) {
        setTasks((prev) =>
          prev.map((task) =>
            task.id === taskId
              ? {
                  ...task,
                  priority: previousPriority,
                }
              : task,
          ),
        );
      }
    }
  }

  const selectedTask = tasks.find((task) => task.id === selectedTaskId) || null;

  return (
    <main className="page-shell">
      <section className="board-card">
        <div className="board-header">
          <div>
            <p className="eyebrow">Task Board</p>
            <h1>TASK BOARD.</h1>
          </div>
          <div className="board-header__controls">
            <label className="field sort-field">
              <span>Sort by priority</span>
              <select value={sortOrder} onChange={(event) => setSortOrder(event.target.value)}>
                <option value="high_to_low">High to low</option>
                <option value="low_to_high">Low to high</option>
              </select>
            </label>
            <span className={`connection-pill connection-pill--${status}`}>{status}</span>
          </div>
        </div>

        {error ? <p className="error-banner">{error}</p> : null}

        <TaskForm onSubmit={handleCreateTask} />
        <TaskList
          tasks={tasks}
          onMoveTask={handleMoveTask}
          onSelectTask={setSelectedTaskId}
          sortOrder={sortOrder}
          selectedTaskId={selectedTaskId}
        />
        <TaskDetail
          task={selectedTask}
          onClose={() => setSelectedTaskId(null)}
          onUpdateTaskPriority={handleUpdateTaskPriority}
          onUpdateTaskStatus={handleMoveTask}
        />
      </section>
    </main>
  );
}
