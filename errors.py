"""What can go wrong, in the words of the task list: TaskNotFound. (M3, lesson 15)"""


class TaskNotFound(Exception):
    def __init__(self, task_id: int) -> None:
        super().__init__(f"Task {task_id} not found")
        self.task_id = task_id
