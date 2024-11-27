# repositories/user_repository.py
from entities.User import User

class UserRepository:
    def __init__(self, storage):
        self.storage = storage
        self.users = self.load_users()

    def load_users(self):
        data = self.storage.load()
        users = {}
        for username, user_data in data.items():
            users[username] = User(**user_data)
        return users

    def add(self, user):
        self.users[user.username] = user
        self.save_users()

    def get(self, username):
        return self.users.get(username)

    def update(self, user):
        self.users[user.username] = user
        self.save_users()

    def authenticate(self, username, password):
        user = self.get(username)
        if user and user.password == password:
            return user
        return None

    def save_users(self):
        data = {username: vars(user) for username, user in self.users.items()}
        self.storage.save(data)
