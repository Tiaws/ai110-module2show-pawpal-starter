"""Core data models and scheduler skeleton for PawPal+."""

from dataclasses import dataclass, field
from datetime import date


@dataclass
class Task:
    task_id: int
    description: str
    duration: int
    priority: str
    time_slot: str = ""
    is_completed: bool = False

    def mark_completed(self) -> None:
        raise NotImplementedError

    def edit_details(self, new_details: dict[str, object]) -> None:
        raise NotImplementedError


@dataclass
class Pet:
    name: str
    species: str
    tasks: list[Task] = field(default_factory=list)

    def add_task(self, task: Task) -> None:
        raise NotImplementedError


@dataclass
class Owner:
    name: str
    pets: list[Pet] = field(default_factory=list)

    def add_pet(self, pet: Pet) -> None:
        raise NotImplementedError


@dataclass
class Scheduler:
    owner: Owner

    def get_available_time(self, date: date) -> int:
        raise NotImplementedError

    def generate_daily_plan(self) -> list[Task]:
        raise NotImplementedError