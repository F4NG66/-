from usecases.CompleteTaskUseCase import CompleteTaskUseCase
from usecases.LeaderboardUseCase import LeaderboardUseCase
from usecases.PublishTaskUseCase import PublishTaskUseCase
from usecases.SpendAnanUseCase import SpendAnanUseCase


class Controller:
    def __init__(self, user_repo, task_repo, notification_service):
        self.user_repo = user_repo
        self.task_repo = task_repo
        self.notification_service = notification_service
        self.publish_task_uc = PublishTaskUseCase(task_repo, notification_service)
        self.complete_task_uc = CompleteTaskUseCase(task_repo, user_repo, notification_service)
        self.spend_anan_uc = SpendAnanUseCase(user_repo)
        self.leaderboard_uc = LeaderboardUseCase(user_repo)
