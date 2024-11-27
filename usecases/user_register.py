# use_cases/user_register.py
from entities.User import User

class UserRegisterUseCase:
    def __init__(self, user_repo):
        self.user_repo = user_repo

    def execute(self, username, password, role='user'):
        if self.user_repo.get(username):
            return None  # 用户已存在
        user = User(username=username, password=password, role=role)
        self.user_repo.add(user)
        return user
