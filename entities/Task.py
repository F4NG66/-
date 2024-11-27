# entities/task.py
from dataclasses import dataclass, field
from datetime import datetime
from typing import List

@dataclass
class Task:
    id: int
    title: str
    description: str
    difficulty: int
    reward: int
    deadline: str  # 可以转换为 datetime 对象
    assigned_users: List[str]
    completed_by: List[str] = field(default_factory=list)
    is_completed: bool = False

    def mark_completed(self, username: str):
        if username not in self.completed_by:
            self.completed_by.append(username)
        if set(self.assigned_users) == set(self.completed_by):
            self.is_completed = True
