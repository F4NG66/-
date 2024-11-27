# use_cases/publish_task.py
from entities.Task import Task
from entities.User import User

class PublishTaskUseCase:
    def __init__(self, task_repo):
        self.task_repo = task_repo

    def execute(self, task_data: dict, user: User):
        if user.role != 'admin':
            raise PermissionError("Only admin can publish tasks.")
        task = Task(**task_data)
        self.task_repo.add(task)
        return task
