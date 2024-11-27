class LeaderboardUseCase:
    def __init__(self, user_repository):
        self.user_repository = user_repository

    def execute(self):
        users = list(self.user_repository.users.values())
        # 根据等级和anan排序
        users.sort(key=lambda x: (x.level, x.total_anan), reverse=True)
        return users
