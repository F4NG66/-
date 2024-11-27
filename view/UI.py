import tkinter as tk
from tkinter import messagebox
from datetime import datetime

from entities.Task import Task
from interface.SQLiteRepo import SQLiteRepo
from usecases.CompleteTaskUseCase import CompleteTaskUseCase
from usecases.PublishTaskUseCase import PublishTaskUseCase


class TaskUI:
    def __init__(self, root, publish_use_case, complete_use_case, user_repo):
        self.root = root
        self.publish_use_case = publish_use_case
        self.complete_use_case = complete_use_case
        self.user_repo = user_repo
        self.setup_ui()

    def setup_ui(self):
        self.root.title("任务管理系统")

        # 发布任务部分
        tk.Label(self.root, text="发布任务").grid(row=0, column=0, columnspan=2)

        tk.Label(self.root, text="任务标题:").grid(row=1, column=0)
        self.title_entry = tk.Entry(self.root)
        self.title_entry.grid(row=1, column=1)

        tk.Label(self.root, text="奖励（anan）:").grid(row=2, column=0)
        self.reward_entry = tk.Entry(self.root)
        self.reward_entry.grid(row=2, column=1)

        tk.Label(self.root, text="截止日期 (YYYY-MM-DD):").grid(row=3, column=0)
        self.deadline_entry = tk.Entry(self.root)
        self.deadline_entry.grid(row=3, column=1)

        tk.Label(self.root, text="分配给:").grid(row=4, column=0)
        self.assignee_entry = tk.Entry(self.root)
        self.assignee_entry.grid(row=4, column=1)

        tk.Button(self.root, text="发布任务", command=self.publish_task).grid(row=5, column=0, columnspan=2)

        # 完成任务部分
        tk.Label(self.root, text="完成任务").grid(row=6, column=0, columnspan=2)

        tk.Label(self.root, text="任务ID:").grid(row=7, column=0)
        self.task_id_entry = tk.Entry(self.root)
        self.task_id_entry.grid(row=7, column=1)

        tk.Label(self.root, text="用户名:").grid(row=8, column=0)
        self.username_entry = tk.Entry(self.root)
        self.username_entry.grid(row=8, column=1)

        tk.Button(self.root, text="完成任务", command=self.complete_task).grid(row=9, column=0, columnspan=2)

    def publish_task(self):
        title = self.title_entry.get()
        reward = int(self.reward_entry.get())
        deadline = self.deadline_entry.get()
        assignees = self.assignee_entry.get().split(",")

        try:
            deadline_date = datetime.strptime(deadline, "%Y-%m-%d")
            task = Task(title=title, description="描述", difficulty=1, reward=reward, deadline=deadline, assignees=assignees)
            self.publish_use_case.execute(task)
            messagebox.showinfo("成功", "任务已发布！")
        except ValueError:
            messagebox.showerror("错误", "截止日期格式错误，应为 YYYY-MM-DD。")

    def complete_task(self):
        task_id = int(self.task_id_entry.get())
        username = self.username_entry.get()

        message = self.complete_use_case.execute(task_id, username)
        messagebox.showinfo("任务完成", message)


if __name__ == "__main__":
    # 初始化数据库和存储
    db_repo = SQLiteRepo()

    # 初始化用例
    publish_task_use_case = PublishTaskUseCase(db_repo, db_repo)
    complete_task_use_case = CompleteTaskUseCase(db_repo, db_repo)

    # 初始化 UI
    root = tk.Tk()
    app = TaskUI(root, publish_task_use_case, complete_task_use_case, db_repo)
    root.mainloop()
