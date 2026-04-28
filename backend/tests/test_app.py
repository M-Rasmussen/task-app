import tempfile
import unittest
from pathlib import Path

from TestAPP.backend.app import app
from TestAPP.backend.services.task_service import TaskService


class TaskApiTestCase(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.db_path = Path(self.temp_dir.name) / "test_tasks.db"
        self.client = app.test_client()
        app.config["TESTING"] = True

        self.original_task_service = app.view_functions["get_tasks"].__globals__["task_service"]
        self.test_task_service = TaskService(db_path=self.db_path)

        for view_function in app.view_functions.values():
            view_function.__globals__["task_service"] = self.test_task_service

    def tearDown(self):
        for view_function in app.view_functions.values():
            view_function.__globals__["task_service"] = self.original_task_service

        self.temp_dir.cleanup()

    def test_create_task_endpoint(self):
        response = self.client.post(
            "/api/tasks",
            json={
                "title": "API task",
                "description": "created through Flask",
                "status": "todo",
                "priority": "medium",
            },
        )

        self.assertEqual(response.status_code, 201)
        payload = response.get_json()
        self.assertEqual(payload["title"], "API task")
        self.assertEqual(payload["status"], "todo")

    def test_update_task_endpoint(self):
        created = self.test_task_service.create_task({"title": "Original title"})

        response = self.client.put(
            f"/api/tasks/{created.id}",
            json={"status": "done", "priority": "high"},
        )

        self.assertEqual(response.status_code, 200)
        payload = response.get_json()
        self.assertEqual(payload["status"], "done")
        self.assertEqual(payload["priority"], "high")

    def test_get_tasks_endpoint_returns_filtered_results(self):
        self.test_task_service.create_task({"title": "Todo item", "status": "todo"})
        self.test_task_service.create_task({"title": "Done item", "status": "done"})

        response = self.client.get("/api/tasks?status=done")

        self.assertEqual(response.status_code, 200)
        payload = response.get_json()
        self.assertEqual(len(payload), 1)
        self.assertEqual(payload[0]["title"], "Done item")

    def test_stats_endpoint_returns_database_counts(self):
        self.test_task_service.create_task({"title": "One", "status": "todo", "priority": "low"})
        self.test_task_service.create_task(
            {"title": "Two", "status": "in_progress", "priority": "high"}
        )

        response = self.client.get("/api/stats")

        self.assertEqual(response.status_code, 200)
        payload = response.get_json()
        self.assertEqual(payload["total"], 2)
        self.assertEqual(payload["todo"], 1)
        self.assertEqual(payload["in_progress"], 1)
        self.assertEqual(payload["high"], 1)


if __name__ == "__main__":
    unittest.main()
