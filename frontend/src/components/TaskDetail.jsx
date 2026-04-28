const PRIORITY_OPTIONS = ["low", "medium", "high"];
const STATUS_OPTIONS = ["todo", "in_progress", "done"];

function formatLabel(value) {
  return value.replace("_", " ");
}

function formatLocalDate(value) {
  if (!value) {
    return "Unknown";
  }

  const date = new Date(value);

  if (Number.isNaN(date.getTime())) {
    return "Unknown";
  }

  return new Intl.DateTimeFormat(undefined, {
    dateStyle: "medium",
    timeStyle: "short",
  }).format(date);
}

function TaskDetail({ task, onClose, onUpdateTaskPriority, onUpdateTaskStatus }) {
  if (!task) {
    return null;
  }

  return (
    <section className="task-detail">
      <div className="task-detail__header">
        <div>
          <p className="eyebrow">Task Details</p>
          <h2>{task.title}</h2>
        </div>
        <button type="button" className="task-detail__close" onClick={onClose}>
          Close
        </button>
      </div>

      <div className="task-detail__grid">
        <div className="task-detail__section task-detail__section--wide">
          <h3>Description</h3>
          <p>{task.description || "No description yet."}</p>
        </div>

        <div className="task-detail__section">
          <h3>Created</h3>
          <p>{formatLocalDate(task.created_at)}</p>
        </div>

        <div className="task-detail__section">
          <h3>Priority</h3>
          <select
            value={task.priority}
            onChange={(event) => onUpdateTaskPriority(task.id, event.target.value)}
          >
            {PRIORITY_OPTIONS.map((priority) => (
              <option key={priority} value={priority}>
                {priority}
              </option>
            ))}
          </select>
        </div>

        <div className="task-detail__section">
          <h3>Status</h3>
          <select
            value={task.status}
            onChange={(event) => onUpdateTaskStatus(task.id, event.target.value)}
          >
            {STATUS_OPTIONS.map((status) => (
              <option key={status} value={status}>
                {formatLabel(status)}
              </option>
            ))}
          </select>
        </div>
      </div>
    </section>
  );
}

export default TaskDetail;
