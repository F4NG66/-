# use_cases/transfer_anan.py
class TransferAnanUseCase:
    def __init__(self, user_repo):
        self.user_repo = user_repo

    def execute(self, from_username, to_username, amount):
        """执行 Anan 转移"""
        # 检查用户是否存在
        from_user = self.user_repo.get(from_username)
        to_user = self.user_repo.get(to_username)
        if not from_user:
            return False, f"用户 {from_username} 不存在。"
        if not to_user:
            return False, f"用户 {to_username} 不存在。"

        # 检查余额是否足够
        if from_user.anan_balance < amount:
            return False, "余额不足，无法完成转移。"

        # 转移 Anan
        from_user.anan_balance -= amount
        to_user.anan_balance += amount

        # 更新用户数据
        self.user_repo.update(from_user)
        self.user_repo.update(to_user)

        return True, f"成功转移 {amount} Anan 给 {to_user.username}。"
