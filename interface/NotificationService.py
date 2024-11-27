class NotificationService:
    def notify_new_task(self, task):
        for user in task.assigned_users:
            print(f"通知：{user.username}，你有一个新任务：{task.title}")

    def notify_task_completion(self, user, task):
        print(f"通知：{user.username}，你已完成任务：{task.title}")
