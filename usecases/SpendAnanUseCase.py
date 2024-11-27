class SpendAnanUseCase:
    def __init__(self, user_repository):
        self.user_repository = user_repository

    def execute(self, username, amount):
        user = self.user_repository.get_user(username)
        if user and user.spend_anan(amount):
            print(f"{user.username}消费了{amount}个anan，剩余{user.anan}个anan")
            return True
        else:
            print(f"{user.username}消费anan失败。")
            return False
