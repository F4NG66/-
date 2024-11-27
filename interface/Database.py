import sqlite3

class Database:
    def __init__(self, db_name='app.db'):
        self.connection = sqlite3.connect(db_name)
        self.create_tables()

    def create_tables(self):
        cursor = self.connection.cursor()
        # 创建用户表
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                username TEXT PRIMARY KEY,
                anan INTEGER,
                total_anan INTEGER
            )
        ''')
        # 创建任务表
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT,
                description TEXT,
                difficulty INTEGER,
                deadline TEXT
            )
        ''')
        # 创建任务分配表
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS task_assignments (
                task_id INTEGER,
                username TEXT,
                completed INTEGER,
                FOREIGN KEY(task_id) REFERENCES tasks(id),
                FOREIGN KEY(username) REFERENCES users(username)
            )
        ''')
        self.connection.commit()
