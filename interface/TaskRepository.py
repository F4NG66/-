from entities.Task import Task


class TaskRepository:
    def __init__(self, database, user_repository):
        self.database = database
        self.user_repository = user_repository

    def add_task(self, task):
        cursor = self.database.connection.cursor()
        cursor.execute('''
            INSERT INTO tasks (title, description, difficulty, deadline) VALUES (?, ?, ?, ?)
        ''', (task.title, task.description, task.difficulty, task.deadline.isoformat() if task.deadline else None))
        task_id = cursor.lastrowid
        # 分配任务给用户
        for user in task.assigned_users:
            cursor.execute('''
                INSERT INTO task_assignments (task_id, username, completed) VALUES (?, ?, 0)
            ''', (task_id, user.username))
        self.database.connection.commit()
        return task_id

    def get_task(self, task_id):
        cursor = self.database.connection.cursor()
        cursor.execute('SELECT id, title, description, difficulty, deadline FROM tasks WHERE id = ?', (task_id,))
        result = cursor.fetchone()
        if result:
            id, title, description, difficulty, deadline = result
            task = Task(title, description, difficulty, datetime.fromisoformat(deadline) if deadline else None)
            task.id = id
            # 获取分配的用户
            cursor.execute('SELECT username, completed FROM task_assignments WHERE task_id = ?', (task_id,))
            assignments = cursor.fetchall()
            for username, completed in assignments:
                user = self.user_repository.get_user(username)
                if user:
                    task.assigned_users.append(user)
                    if completed:
                        task.completed_users.append(user)
            return task
        return None

    def update_task_completion(self, task, user):
        cursor = self.database.connection.cursor()
        cursor.execute('''
            UPDATE task_assignments SET completed = 1 WHERE task_id = ? AND username = ?
        ''', (task.id, user.username))
        self.database.connection.commit()
