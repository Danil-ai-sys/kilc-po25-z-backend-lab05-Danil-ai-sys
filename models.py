"""What we keep: the Task dataclass. (M2, lesson 12)"""

from dataclasses import dataclass


@dataclass
class Task:
    id: int
    title: str
    done: bool = False
