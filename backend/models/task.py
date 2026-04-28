from datetime import UTC, datetime


class Task:
    VALID_STATUS = {"todo", "in_progress", "done"}
    VALID_PRIORITY = {"low", "medium", "high"}

    def __init__(self, id, title, status="todo", priority="medium", description="", created_at=None):
        self.id = id
        self.title = title
        self.description = description
        self.status = status
        self.priority = priority
        self.created_at = created_at or datetime.now(UTC)

        self.validate()

    @classmethod
    def from_dict(cls, data):
        created_at = data.get("created_at")

        if isinstance(created_at, str):
            created_at = datetime.fromisoformat(created_at)

        return cls(
            id=data.get("id"),
            title=data.get("title", ""),
            description=data.get("description", ""),
            status=data.get("status", "todo"),
            priority=data.get("priority", "medium"),
            created_at=created_at,
        )

    def validate(self):
        if not self.title or not self.title.strip():
            raise ValueError("Title is required")

        if self.status not in self.VALID_STATUS:
            raise ValueError(f"Status must be one of: {', '.join(sorted(self.VALID_STATUS))}")

        if self.priority not in self.VALID_PRIORITY:
            raise ValueError(f"Priority must be one of: {', '.join(sorted(self.VALID_PRIORITY))}")

    def update(self, data):
        if "title" in data:
            self.title = data["title"]

        if "description" in data:
            self.description = data["description"]

        if "status" in data:
            self.status = data["status"]

        if "priority" in data:
            self.priority = data["priority"]

        self.validate()

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "status": self.status,
            "priority": self.priority,
            "created_at": self.created_at.isoformat(),
        }
