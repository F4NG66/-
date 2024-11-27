# main.py
import tkinter as tk
from tkinter import messagebox, simpledialog
from interface.user_repository import UserRepository
from interface.task_repository import TaskRepository
from usecases.TransferAnanUseCase import TransferAnanUseCase
from usecases.publish_task import PublishTaskUseCase
from usecases.complete_task import CompleteTaskUseCase
from usecases.user_login import UserLoginUseCase
from usecases.user_register import UserRegisterUseCase
from usecases.spend_anan import SpendAnanUseCase
from interface.notification_service import NotificationService
from interface.json_storage import JSONStorage
from entities.User import User
from entities.Task import Task

class Application:
    def __init__(self, root):
        self.root = root
        self.root.title("任务管理系统")
        self.current_user = None

        user_storage = JSONStorage('users.json')
        task_storage = JSONStorage('tasks.json')

        self.user_repo = UserRepository(user_storage)
        self.task_repo = TaskRepository(task_storage)
        self.notification_service = NotificationService()

        self.login_uc = UserLoginUseCase(self.user_repo)
        self.register_uc = UserRegisterUseCase(self.user_repo)
        self.publish_task_uc = PublishTaskUseCase(self.task_repo)
        self.complete_task_uc = CompleteTaskUseCase(self.task_repo, self.user_repo)
        self.spend_anan_uc = SpendAnanUseCase(self.user_repo)

        self.create_login_ui()

    def create_login_ui(self):
        self.clear_window()

        tk.Label(self.root, text="任务管理系统", font=("Arial", 16)).pack(pady=20)
        tk.Button(self.root, text="注册", command=self.register_ui, width=15).pack(pady=5)
        tk.Button(self.root, text="登录", command=self.login_ui, width=15).pack(pady=5)

    def register_ui(self):
        username = simpledialog.askstring("注册", "请输入用户名：")
        if not username:
            return
        password = simpledialog.askstring("注册", "请输入密码：", show='*')
        if not password:
            return
        role = simpledialog.askstring("注册", "请输入角色（user/admin），默认user：") or 'user'
        user = self.register_uc.execute(username, password, role)
        if user:
            messagebox.showinfo("注册", "注册成功！")
        else:
            messagebox.showerror("注册", "用户已存在。")

    def login_ui(self):
        username = simpledialog.askstring("登录", "请输入用户名：")
        if not username:
            return
        password = simpledialog.askstring("登录", "请输入密码：", show='*')
        if not password:
            return
        user = self.login_uc.execute(username, password)
        if user:
            self.current_user = user
            messagebox.showinfo("登录", f"登录成功！欢迎，{user.username}（角色：{user.role}）")
            self.create_main_ui()
        else:
            messagebox.showerror("登录", "用户名或密码错误。")

    def create_main_ui(self):
        self.clear_window()
        tk.Label(self.root, text=f"欢迎，{self.current_user.username}", font=("Arial", 16)).pack(pady=10)

        if self.current_user.role == 'admin':
            tk.Button(self.root, text="发布任务", command=self.publish_task_ui, width=20).pack(pady=5)
            tk.Button(self.root, text="查看任务列表", command=self.view_tasks_ui, width=20).pack(pady=5)
            tk.Button(self.root, text="查看用户排行榜", command=self.view_leaderboard_ui, width=20).pack(pady=5)
        else:
            tk.Button(self.root, text="查看任务列表", command=self.view_tasks_ui, width=20).pack(pady=5)
            tk.Button(self.root, text="完成任务", command=self.complete_task_ui, width=20).pack(pady=5)
            tk.Button(self.root, text="查看个人信息", command=self.view_user_info_ui, width=20).pack(pady=5)
            tk.Button(self.root, text="消费Anan", command=self.spend_anan_ui, width=20).pack(pady=5)
            tk.Button(self.root, text="转移 Anan", command=self.transfer_anan_ui, width=20).pack(pady=5)
            tk.Button(self.root, text="查看用户排行榜", command=self.view_leaderboard_ui, width=20).pack(pady=5)
        tk.Button(self.root, text="注销", command=self.logout, width=20).pack(pady=20)

    def publish_task_ui(self):
        if self.current_user.role != 'admin':
            messagebox.showerror("错误", "只有管理员可以发布任务。")
            return

        task_data = {}
        try:
            task_data['id'] = int(simpledialog.askstring("发布任务", "任务ID："))
            task_data['title'] = simpledialog.askstring("发布任务", "任务标题：")
            task_data['description'] = simpledialog.askstring("发布任务", "任务描述：")
            task_data['difficulty'] = int(simpledialog.askstring("发布任务", "任务难度（整数）："))
            task_data['reward'] = int(simpledialog.askstring("发布任务", "任务奖励Anan："))
            task_data['deadline'] = simpledialog.askstring("发布任务", "任务截止日期（YYYY-MM-DD）：")
            assigned_users = simpledialog.askstring("发布任务", "指定用户（用逗号分隔）：")
            task_data['assigned_users'] = [u.strip() for u in assigned_users.split(',')]
            task = self.publish_task_uc.execute(task_data, self.current_user)
            messagebox.showinfo("发布任务", "任务发布成功！")
            for u in task.assigned_users:
                self.notification_service.notify(u, f"新任务发布：{task.title}")
        except Exception as e:
            messagebox.showerror("错误", str(e))

    def view_tasks_ui(self):
        tasks = self.task_repo.list_all()[::-1]
        task_window = tk.Toplevel(self.root)
        task_window.title("任务列表")

    # 添加过滤选项
        filter_var = tk.StringVar(value="所有任务")
        filter_options = ["所有任务", "未完成任务", "已完成任务"]
        tk.Label(task_window, text="过滤条件：").pack(anchor='w')
        filter_menu = tk.OptionMenu(task_window, filter_var, *filter_options)
        filter_menu.pack(anchor='w')

        search_var = tk.StringVar()
        tk.Label(task_window, text="搜索关键词：").pack(anchor='w')
        search_entry = tk.Entry(task_window, textvariable=search_var)
        search_entry.pack(anchor='w')

    # 分页参数
        page_size = 5
        current_page = [0]
        filtered_tasks = []

        def apply_filters():
            nonlocal filtered_tasks, current_page
            selected_filter = filter_var.get()
            keyword = search_var.get().lower()
            filtered_tasks = []
            for task in tasks:
                if self.current_user.role != 'admin' and self.current_user.username not in task.assigned_users:
                    continue
                if selected_filter == "未完成任务" and task.is_completed:
                    continue
                if selected_filter == "已完成任务" and not task.is_completed:
                    continue
                if keyword and keyword not in task.title.lower() and keyword not in task.description.lower():
                    continue
                filtered_tasks.append(task)
            current_page[0] = 0  # 重置为第一页
            update_list()



        def update_list():
            listbox.delete(0, tk.END)
            if not filtered_tasks:
                listbox.insert(tk.END, "没有符合条件的任务。")
                page_label.config(text="")
                return
            start = current_page[0] * page_size
            end = start + page_size
            paginated_tasks = filtered_tasks[start:end]
            for task in paginated_tasks:
                status = "已完成" if task.is_completed else "未完成"
                assigned_users = ', '.join(task.assigned_users)
                task_info = (f"ID: {task.id}, 标题: {task.title}, 状态: {status}, "
                         f"截止日期: {task.deadline}, 指派给{assigned_users},已完成的用户{', '.join(task.completed_by)}")
                listbox.insert(tk.END, task_info)
            total_pages = (len(filtered_tasks) - 1) // page_size + 1
            page_label.config(text=f"第 {current_page[0]+1} 页，共 {total_pages} 页")

        def next_page():
            total_pages = (len(filtered_tasks) - 1) // page_size + 1
            if current_page[0] + 1 < total_pages:
                current_page[0] += 1
            update_list()

        def prev_page():
            if current_page[0] > 0:
                current_page[0] -= 1
                update_list()

        tk.Button(task_window, text="应用过滤", command=apply_filters).pack()

        listbox = tk.Listbox(task_window, width=80, height=20)
        listbox.pack()

        navigation_frame = tk.Frame(task_window)
        navigation_frame.pack()

        tk.Button(navigation_frame, text="上一页", command=prev_page).pack(side=tk.LEFT)
        page_label = tk.Label(navigation_frame, text="")
        page_label.pack(side=tk.LEFT)
        tk.Button(navigation_frame, text="下一页", command=next_page).pack(side=tk.LEFT)

        filtered_tasks = tasks.copy()
        update_list()


    def complete_task_ui(self):
        task_id = simpledialog.askinteger("完成任务", "请输入要完成的任务ID：")
        if not task_id:
            return
        success = self.complete_task_uc.execute(task_id, self.current_user.username)
        if success:
            task = self.task_repo.get(task_id)
            messagebox.showinfo("完成任务", "任务完成！")
            self.notification_service.notify(self.current_user.username, f"任务已完成：{task.title}")
        else:
            messagebox.showerror("错误", "无法完成任务，请检查任务ID或您是否被指派。")

    def view_user_info_ui(self):
        user = self.current_user
        info = (f"用户名：{user.username}\n"
                f"角色：{user.role}\n"
                f"等级：{user.level}\n"
                f"经验值：{user.experience}\n"
                f"Anan余额：{user.anan_balance}")
        messagebox.showinfo("个人信息", info)

    def spend_anan_ui(self):
        amount = simpledialog.askinteger("消费Anan", "请输入要消费的Anan数量：")
        if not amount:
            return
        if self.spend_anan_uc.execute(self.current_user.username, amount):
            messagebox.showinfo("消费Anan", f"消费成功！剩余Anan余额：{self.current_user.anan_balance}")
        else:
            messagebox.showerror("错误", "消费失败，余额不足。")

    def transfer_anan_ui(self):
        """用户转移 Anan 的界面逻辑"""
        to_username = simpledialog.askstring("转移 Anan", "请输入接收方用户名：")
        if not to_username:
            return
        try:
            amount = simpledialog.askinteger("转移 Anan", "请输入转移的 Anan 数量：", minvalue=1)
            if not amount:
                return
        except ValueError:
            messagebox.showerror("错误", "输入的金额无效。")
            return

    # 调用转移用例
        transfer_anan_uc = TransferAnanUseCase(self.user_repo)
        success, message = transfer_anan_uc.execute(self.current_user.username, to_username, amount)
        if success:
            messagebox.showinfo("成功", message)
        else:
            messagebox.showerror("失败", message)

    def view_leaderboard_ui(self):
        users = self.user_repo.users.values()
        leaderboard = sorted(users, key=lambda u: u.experience, reverse=True)
        leaderboard_text = ""
        for user in leaderboard:
            leaderboard_text += (f"{user.username}: 等级 {user.level}, 经验值 {user.experience}, "
                                 f"Anan {user.anan_balance}\n")
        messagebox.showinfo("用户排行榜", leaderboard_text)

    def logout(self):
        self.current_user = None
        self.create_login_ui()

    def clear_window(self):
        for widget in self.root.winfo_children():
            widget.destroy()

def main():
    root = tk.Tk()
    app = Application(root)
    root.mainloop()

if __name__ == "__main__":
    main()
