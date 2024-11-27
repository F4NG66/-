import sqlite3

from entities.Task import Task
from entities.User import User


class SQLiteRepo:
    def __init__(self, db_path="tasks.db"):
        self.conn = sqlite3.connect(db_path)
        self.create_tables()

    def create_tables(self):
        with self.conn:
            # 创建用户表
            self.conn.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    username TEXT PRIMARY KEY,
                    exp INTEGER DEFAULT 0,
                    balance INTEGER DEFAULT 0,
                    level INTEGER DEFAULT 1
                )
            """)
            # 创建任务表
            self.conn.execute("""
                CREATE TABLE IF NOT EXISTS tasks (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    title TEXT,
                    description TEXT,
                    difficulty INTEGER,
                    reward INTEGER,
                    deadline TEXT,
                    is_completed INTEGER DEFAULT 0,
                    assignees TEXT
                )
            """)

    def add_user(self, user):
        with self.conn:
            self.conn.execute(
                "INSERT OR IGNORE INTO users (username, exp, balance, level) VALUES (?, ?, ?, ?)",
                (user.username, user.exp, user.balance, user.level),
            )

    def get_user(self, username):
        cursor = self.conn.execute("SELECT * FROM users WHERE username = ?", (username,))
        row = cursor.fetchone()
        if row:
            user = User(username=row[0])
            user.exp = row[1]
            user.balance = row[2]
            user.level = row[3]
            return user
        return None

    def update_user(self, user):
        with self.conn:
            self.conn.execute(
                "UPDATE users SET exp = ?, balance = ?, level = ? WHERE username = ?",
                (user.exp, user.balance, user.level, user.username),
            )

    def add_task(self, task):
        with self.conn:
            self.conn.execute(
                "INSERT INTO tasks (title, description, difficulty, reward, deadline, assignees) VALUES (?, ?, ?, ?, ?, ?)",
                (task.title, task.description, task.difficulty, task.reward, task.deadline, ",".join(task.assignees)),
            )

    def get_task(self, task_id):
        cursor = self.conn.execute("SELECT * FROM tasks WHERE id = ?", (task_id,))
        row = cursor.fetchone()
        if row:
            task = Task(
                title=row[1],
                description=row[2],
                difficulty=row[3],
                reward=row[4],
                deadline=row[5],
                assignees=row[7].split(","),
            )
            task.is_completed = bool(row[6])
            return task
        return None

    def update_task(self, task):
        with self.conn:
            self.conn.execute(
                "UPDATE tasks SET is_completed = ? WHERE id = ?",
                (1 if task.is_completed else 0, task.id),
            )

    def get_all_tasks(self):
        cursor = self.conn.execute("SELECT * FROM tasks")
        tasks = []
        for row in cursor.fetchall():
            task = Task(
                title=row[1],
                description=row[2],
                difficulty=row[3],
                reward=row[4],
                deadline=row[5],
                assignees=row[7].split(","),
            )
            task.is_completed = bool(row[6])
            tasks.append(task)

