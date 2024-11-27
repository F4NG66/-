# use_cases/complete_task.py
class CompleteTaskUseCase:
    def __init__(self, task_repo, user_repo):
        self.task_repo = task_repo
        self.user_repo = user_repo

    def execute(self, task_id: int, username: str):
        task = self.task_repo.get(task_id)
        user = self.user_repo.get(username)
        if task and user and username in task.assigned_users:
            task.mark_completed(username)
            user.add_experience(task.difficulty * 10)
            user.earn_anan(task.reward)
            self.task_repo.update(task)
            self.user_repo.update(user)
            return True
        return False
