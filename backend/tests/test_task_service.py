import tempfile
import unittest
from pathlib import Path

from TestAPP.backend.services.task_service import TaskService


class TaskServiceTestCase(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.db_path = Path(self.temp_dir.name) / "test_tasks.db"
        self.service = TaskService(db_path=self.db_path)

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_create_and_get_task(self):
        created = self.service.create_task(
            {
                "title": "Write tests",
                "description": "Cover the SQLite service",
                "status": "todo",
                "priority": "high",
            }
        )

        fetched = self.service.get_task_by_id(created.id)

        self.assertEqual(fetched.title, "Write tests")
        self.assertEqual(fetched.description, "Cover the SQLite service")
        self.assertEqual(fetched.status, "todo")
        self.assertEqual(fetched.priority, "high")

    def test_get_all_tasks_applies_filters(self):
        self.service.create_task(
            {"title": "Alpha task", "description": "first", "status": "todo", "priority": "low"}
        )
        self.service.create_task(
            {
                "title": "Beta task",
                "description": "second item",
                "status": "done",
                "priority": "high",
            }
        )

        filtered = self.service.get_all_tasks({"status": "done", "search": "beta"})

        self.assertEqual(len(filtered), 1)
        self.assertEqual(filtered[0]["title"], "Beta task")

    def test_update_task_persists_changes(self):
        created = self.service.create_task(
            {"title": "Move card", "description": "drag me", "status": "todo", "priority": "medium"}
        )

        updated = self.service.update_task(
            created.id,
            {"status": "in_progress", "priority": "high", "description": "updated"},
        )

        self.assertEqual(updated.status, "in_progress")
        self.assertEqual(updated.priority, "high")
        self.assertEqual(updated.description, "updated")

    def test_delete_task_removes_it(self):
        created = self.service.create_task({"title": "Remove me"})

        self.service.delete_task(created.id)

        with self.assertRaises(ValueError):
            self.service.get_task_by_id(created.id)

    def test_get_stats_counts_statuses_and_priorities(self):
        self.service.create_task({"title": "Todo low", "status": "todo", "priority": "low"})
        self.service.create_task(
            {"title": "Doing medium", "status": "in_progress", "priority": "medium"}
        )
        self.service.create_task({"title": "Done high", "status": "done", "priority": "high"})

        stats = self.service.get_stats()

        self.assertEqual(
            stats,
            {
                "total": 3,
                "todo": 1,
                "in_progress": 1,
                "done": 1,
                "low": 1,
                "medium": 1,
                "high": 1,
            },
        )


if __name__ == "__main__":
    unittest.main()
