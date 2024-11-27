# repositories/task_repository.py
from entities.Task import Task

class TaskRepository:
    def __init__(self, storage):
        self.storage = storage
        self.tasks = self.load_tasks()

    def load_tasks(self):
        data = self.storage.load()
        tasks = {}
        for task_id, task_data in data.items():
            task_data['id'] = int(task_data['id'])
            tasks[task_data['id']] = Task(**task_data)
        return tasks

    def add(self, task):
        self.tasks[task.id] = task
        self.save_tasks()

    def get(self, task_id):
        return self.tasks.get(task_id)

    def update(self, task):
        self.tasks[task.id] = task
        self.save_tasks()

    def list_all(self):
        return list(self.tasks.values())

    def save_tasks(self):
        data = {task_id: vars(task) for task_id, task in self.tasks.items()}
        self.storage.save(data)
