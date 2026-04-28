import sqlite3
from contextlib import contextmanager
from pathlib import Path

from TestAPP.backend.models.task import Task


class TaskService:
    def __init__(self, db_path=None):
        default_path = Path(__file__).resolve().parent.parent / "tasks.db"
        self.db_path = Path(db_path) if db_path else default_path
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self._initialize_database()

    @contextmanager
    def _get_connection(self):
        connection = sqlite3.connect(self.db_path)
        connection.row_factory = sqlite3.Row
        try:
            yield connection
            connection.commit()
        finally:
            connection.close()

    def _initialize_database(self):
        with self._get_connection() as connection:
            connection.execute(
                """
                CREATE TABLE IF NOT EXISTS tasks (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    title TEXT NOT NULL,
                    description TEXT NOT NULL DEFAULT '',
                    status TEXT NOT NULL,
                    priority TEXT NOT NULL,
                    created_at TEXT NOT NULL
                )
                """
            )

    def _row_to_task(self, row):
        if row is None:
            raise ValueError("Task not found")

        return Task.from_dict(
            {
                "id": row["id"],
                "title": row["title"],
                "description": row["description"],
                "status": row["status"],
                "priority": row["priority"],
                "created_at": row["created_at"],
            }
        )

    def get_all_tasks(self, filters=None):
        filters = filters or {}
        query = """
            SELECT id, title, description, status, priority, created_at
            FROM tasks
            WHERE 1 = 1
        """
        parameters = []

        status = filters.get("status")
        priority = filters.get("priority")
        search = filters.get("search")

        if status:
            query += " AND status = ?"
            parameters.append(status)

        if priority:
            query += " AND priority = ?"
            parameters.append(priority)

        if search:
            query += " AND (LOWER(title) LIKE ? OR LOWER(description) LIKE ?)"
            search_value = f"%{search.lower()}%"
            parameters.extend([search_value, search_value])

        query += " ORDER BY datetime(created_at) ASC, id ASC"

        with self._get_connection() as connection:
            rows = connection.execute(query, parameters).fetchall()

        return [self._row_to_task(row).to_dict() for row in rows]

    def get_task_by_id(self, task_id):
        with self._get_connection() as connection:
            row = connection.execute(
                """
                SELECT id, title, description, status, priority, created_at
                FROM tasks
                WHERE id = ?
                """,
                (task_id,),
            ).fetchone()

        return self._row_to_task(row)

    def create_task(self, data):
        task = Task(
            id=None,
            title=data.get("title", ""),
            description=data.get("description", ""),
            status=data.get("status", "todo"),
            priority=data.get("priority", "medium"),
        )

        with self._get_connection() as connection:
            cursor = connection.execute(
                """
                INSERT INTO tasks (title, description, status, priority, created_at)
                VALUES (?, ?, ?, ?, ?)
                """,
                (
                    task.title,
                    task.description,
                    task.status,
                    task.priority,
                    task.created_at.isoformat(),
                ),
            )
            task_id = cursor.lastrowid

        return self.get_task_by_id(task_id)

    def update_task(self, task_id, data):
        task = self.get_task_by_id(task_id)
        task.update(data)

        with self._get_connection() as connection:
            connection.execute(
                """
                UPDATE tasks
                SET title = ?, description = ?, status = ?, priority = ?
                WHERE id = ?
                """,
                (
                    task.title,
                    task.description,
                    task.status,
                    task.priority,
                    task_id,
                ),
            )

        return self.get_task_by_id(task_id)

    def delete_task(self, task_id):
        task = self.get_task_by_id(task_id)

        with self._get_connection() as connection:
            connection.execute("DELETE FROM tasks WHERE id = ?", (task_id,))

        return task

    def get_stats(self):
        with self._get_connection() as connection:
            row = connection.execute(
                """
                SELECT
                    COUNT(*) AS total,
                    SUM(CASE WHEN status = 'todo' THEN 1 ELSE 0 END) AS todo,
                    SUM(CASE WHEN status = 'in_progress' THEN 1 ELSE 0 END) AS in_progress,
                    SUM(CASE WHEN status = 'done' THEN 1 ELSE 0 END) AS done,
                    SUM(CASE WHEN priority = 'low' THEN 1 ELSE 0 END) AS low,
                    SUM(CASE WHEN priority = 'medium' THEN 1 ELSE 0 END) AS medium,
                    SUM(CASE WHEN priority = 'high' THEN 1 ELSE 0 END) AS high
                FROM tasks
                """
            ).fetchone()

        return {
            "total": row["total"] or 0,
            "todo": row["todo"] or 0,
            "in_progress": row["in_progress"] or 0,
            "done": row["done"] or 0,
            "low": row["low"] or 0,
            "medium": row["medium"] or 0,
            "high": row["high"] or 0,
        }
