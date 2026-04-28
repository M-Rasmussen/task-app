function TaskItem({ task, isDragging, isSelected, onDragStart, onDragEnd, onSelectTask }) {
  return (
    <article
      className={`task-card${isDragging ? " task-card--dragging" : ""}${isSelected ? " task-card--selected" : ""}`}
      draggable
      onClick={() => onSelectTask(task.id)}
      onDragStart={(event) => {
        event.dataTransfer.effectAllowed = "move";
        event.dataTransfer.setData("text/plain", String(task.id));
        onDragStart(task.id);
      }}
      onDragEnd={onDragEnd}
    >
      <div className="task-card__top">
        <h3>{task.title}</h3>
        <span className={`priority-badge priority-badge--${task.priority}`}>{task.priority}</span>
      </div>
    </article>
  );
}

export default TaskItem;
