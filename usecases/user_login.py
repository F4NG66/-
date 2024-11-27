# use_cases/user_login.py
class UserLoginUseCase:
    def __init__(self, user_repo):
        self.user_repo = user_repo

    def execute(self, username, password):
        user = self.user_repo.authenticate(username, password)
        if user:
            return user
        else:
            return None
