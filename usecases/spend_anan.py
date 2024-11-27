# use_cases/spend_anan.py
class SpendAnanUseCase:
    def __init__(self, user_repo):
        self.user_repo = user_repo

    def execute(self, username: str, amount: int):
        user = self.user_repo.get(username)
        if user and user.spend_anan(amount):
            self.user_repo.update(user)
            return True
        return False
