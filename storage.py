"""The Storage class: the list of tasks, next_id, and the JSON file.

M3: in memory: get_all, get, add, update, delete (lesson 12)
M4: load() and save() with tasks.json (lessons 13 and 14)
"""

import json
import logging
import os

from pydantic import TypeAdapter

from errors import TaskNotFound
from models import Task
from schemas import TaskIn

logger = logging.getLogger(__name__)

_adapter = TypeAdapter(list[Task])


class Storage:
    def __init__(self, path: str = "tasks.json") -> None:
        self.path = path
        self.tasks: list[Task] = self.load()
        self.next_id = max((t.id for t in self.tasks), default=0) + 1

    def load(self) -> list[Task]:
        if not os.path.exists(self.path):
            return []
        with open(self.path, encoding="utf-8") as f:
            raw = json.load(f)
        # A bad record raises ValidationError naming the record and the field.
        return _adapter.validate_python(raw)

    def save(self) -> None:
        tmp = self.path + ".tmp"
        with open(tmp, "w", encoding="utf-8") as f:
            json.dump(_adapter.dump_python(self.tasks, mode="json"), f, ensure_ascii=False, indent=2)
        os.replace(tmp, self.path)

    def get_all(self) -> list[Task]:
        return self.tasks

    def get(self, task_id: int) -> Task:
        for task in self.tasks:
            if task.id == task_id:
                return task
        raise TaskNotFound(task_id)

    def add(self, data: TaskIn) -> Task:
        task = Task(id=self.next_id, title=data.title, done=data.done)
        self.next_id += 1
        self.tasks.append(task)
        self.save()
        logger.info("task %d added", task.id)
        return task

    def update(self, task_id: int, changes: dict) -> Task:
        task = self.get(task_id)
        for key, value in changes.items():
            setattr(task, key, value)
        self.save()
        logger.info("task %d changed: %s", task_id, ", ".join(changes) or "nothing")
        return task

    def delete(self, task_id: int) -> None:
        task = self.get(task_id)
        self.tasks.remove(task)
        self.save()
        logger.info("task %d deleted", task_id)
