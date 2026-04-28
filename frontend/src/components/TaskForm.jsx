import { useState } from "react";

const STATUS_OPTIONS = ["todo", "in_progress", "done"];
const PRIORITY_OPTIONS = ["low", "medium", "high"];

const INITIAL_FORM = {
  title: "",
  description: "",
  status: "todo",
  priority: "medium",
};

function formatLabel(value) {
  return value.replace("_", " ");
}

export default function TaskForm({ onSubmit }) {
  const [form, setForm] = useState(INITIAL_FORM);
  const [errors, setErrors] = useState({});

  function handleChange(event) {
    const { name, value } = event.target;
    setForm((prev) => ({
      ...prev,
      [name]: value,
    }));
  }

  function validate() {
    const nextErrors = {};

    if (!form.title.trim()) {
      nextErrors.title = "Title is required";
    }

    if (!STATUS_OPTIONS.includes(form.status)) {
      nextErrors.status = "Invalid status";
    }

    if (!PRIORITY_OPTIONS.includes(form.priority)) {
      nextErrors.priority = "Invalid priority";
    }

    return nextErrors;
  }

  async function handleSubmit(event) {
    event.preventDefault();

    const validationErrors = validate();
    if (Object.keys(validationErrors).length > 0) {
      setErrors(validationErrors);
      return;
    }

    setErrors({});

    const result = await onSubmit(form);
    if (result?.ok) {
      setForm(INITIAL_FORM);
    }
  }

  return (
    <form className="task-form" onSubmit={handleSubmit}>
      <label className="field">
        <span>Title</span>
        <input type="text" name="title" value={form.title} onChange={handleChange} />
        {errors.title ? <p className="field-error">{errors.title}</p> : null}
      </label>

      <label className="field field--message">
        <span>Description</span>
        <textarea name="description" value={form.description} onChange={handleChange} />
      </label>

      <label className="field">
        <span>Status</span>
        <select name="status" value={form.status} onChange={handleChange}>
          {STATUS_OPTIONS.map((status) => (
            <option key={status} value={status}>
              {formatLabel(status)}
            </option>
          ))}
        </select>
        {errors.status ? <p className="field-error">{errors.status}</p> : null}
      </label>

      <label className="field">
        <span>Priority</span>
        <select name="priority" value={form.priority} onChange={handleChange}>
          {PRIORITY_OPTIONS.map((priority) => (
            <option key={priority} value={priority}>
              {priority}
            </option>
          ))}
        </select>
        {errors.priority ? <p className="field-error">{errors.priority}</p> : null}
      </label>

      <button type="submit">Create Task</button>
    </form>
  );
}
