import { useState } from "react";
import TaskItem from "./TaskItem";

const STATUS_COLUMNS = [
  { value: "todo", label: "To Do" },
  { value: "in_progress", label: "In Progress" },
  { value: "done", label: "Done" },
];

const PRIORITY_RANK = {
  low: 1,
  medium: 2,
  high: 3,
};

function sortTasksByPriority(tasks, sortOrder) {
  const direction = sortOrder === "low_to_high" ? 1 : -1;

  return [...tasks].sort((left, right) => {
    const priorityDifference =
      (PRIORITY_RANK[left.priority] || 0) - (PRIORITY_RANK[right.priority] || 0);

    if (priorityDifference !== 0) {
      return priorityDifference * direction;
    }

    return new Date(left.created_at || 0) - new Date(right.created_at || 0);
  });
}

function TaskList({ tasks, onMoveTask, onSelectTask, sortOrder, selectedTaskId }) {
  const [draggedTaskId, setDraggedTaskId] = useState(null);
  const [activeColumn, setActiveColumn] = useState(null);

  function handleDragStart(taskId) {
    setDraggedTaskId(taskId);
  }

  function handleDragEnd() {
    setDraggedTaskId(null);
    setActiveColumn(null);
  }

  function handleDrop(nextStatus) {
    if (draggedTaskId == null) {
      return;
    }

    const draggedTask = tasks.find((task) => task.id === draggedTaskId);

    if (draggedTask && draggedTask.status !== nextStatus) {
      onMoveTask(draggedTaskId, nextStatus);
    }

    setDraggedTaskId(null);
    setActiveColumn(null);
  }

  return (
    <section className="board-columns">
      {STATUS_COLUMNS.map((column) => {
        const columnTasks = sortTasksByPriority(
          tasks.filter((task) => task.status === column.value),
          sortOrder,
        );
        const isActiveDropZone = activeColumn === column.value;

        return (
          <div
            key={column.value}
            className={`status-column${isActiveDropZone ? " status-column--active" : ""}`}
            onDragOver={(event) => {
              event.preventDefault();
              if (draggedTaskId != null) {
                setActiveColumn(column.value);
              }
            }}
            onDragEnter={(event) => {
              event.preventDefault();
              if (draggedTaskId != null) {
                setActiveColumn(column.value);
              }
            }}
            onDragLeave={(event) => {
              if (!event.currentTarget.contains(event.relatedTarget)) {
                setActiveColumn((current) => (current === column.value ? null : current));
              }
            }}
            onDrop={(event) => {
              event.preventDefault();
              handleDrop(column.value);
            }}
          >
            <div className="status-column__header">
              <h2>{column.label}</h2>
              <span>{columnTasks.length}</span>
            </div>

            <div className="task-list">
              {columnTasks.length > 0 ? (
                columnTasks.map((task) => (
                  <TaskItem
                    key={task.id}
                    task={task}
                    isDragging={draggedTaskId === task.id}
                    isSelected={selectedTaskId === task.id}
                    onDragStart={handleDragStart}
                    onDragEnd={handleDragEnd}
                    onSelectTask={onSelectTask}
                  />
                ))
              ) : (
                <p className="empty-column">Drop a task here.</p>
              )}
            </div>
          </div>
        );
      })}
    </section>
  );
}

export default TaskList;
