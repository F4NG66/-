# entities/user.py
from dataclasses import dataclass, field

@dataclass
class User:
    username: str
    password: str  # 为简单起见，直接存储明文密码
    role: str = 'user'  # 'user' 或 'admin'
    anan_balance: int = 0
    experience: int = 0
    level: int = 1

    def add_experience(self, amount: int):
        self.experience += amount
        self.level = self.experience // 100 + 1

    def spend_anan(self, amount: int):
        if self.anan_balance >= amount:
            self.anan_balance -= amount
            return True
        return False

    def earn_anan(self, amount: int):
        self.anan_balance += amount
