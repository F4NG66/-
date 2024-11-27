class CompleteTaskUseCase:
    def __init__(self, task_repo, user_repo):
        self.task_repo = task_repo
        self.user_repo = user_repo

    def execute(self, task_id, username):
        task = self.task_repo.get(task_id)
        user = self.user_repo.get(username)

        if task and not task.is_completed and username in task.assignees:
            task.completed_by.append(username)
            user.add_exp(task.reward)
            task.is_completed = True
            return f"{username} 完成了任务 {task.title}，获得奖励 {task.reward} anan！"
        return "任务无法完成或未分配给此用户。"
