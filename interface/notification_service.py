# services/notification_service.py
class NotificationService:
    def notify(self, username, message):
        # 在GUI中，这个方法可以被修改为在界面上显示通知
        print(f"【通知】用户 {username}：{message}")
