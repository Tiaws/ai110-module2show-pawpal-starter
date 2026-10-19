"""PawPal+ core data models and scheduler meeting specific project requirements."""

from dataclasses import dataclass, field
from datetime import date


@dataclass
class Task:
    task_id: int
    description: str
    duration: int
    priority: str
    time_slot: str = ""
    frequency: str = "Once"  # Added per your requirement
    is_completed: bool = False

    def mark_completed(self) -> None:
        """Marks the task as completed."""
        self.is_completed = True

    def edit_details(self, new_details: dict[str, object]) -> None:
        """Updates task attributes using a dictionary."""
        for key, value in new_details.items():
            if hasattr(self, key):
                setattr(self, key, value)


@dataclass
class Pet:
    name: str
    species: str
    tasks: list[Task] = field(default_factory=list)

    def add_task(self, task: Task) -> None:
        """Assigns a new task to this pet."""
        self.tasks.append(task)


@dataclass
class Owner:
    name: str
    pets: list[Pet] = field(default_factory=list)

    def add_pet(self, pet: Pet) -> None:
        """Adds a pet to the household."""
        self.pets.append(pet)

    def get_all_tasks(self) -> list[Task]:
        """Aggregates and returns every pet's tasks together."""
        all_tasks = []
        for pet in self.pets:
            all_tasks.extend(pet.tasks)
        return all_tasks


@dataclass
class Scheduler:
    owner: Owner

    def get_available_time(self, date: date) -> int:
        """Calculates available free time by reading from Owner.get_all_tasks()."""
        total_active_minutes = 720  # e.g., 12-hour window
        used_minutes = sum(
            task.duration 
            for task in self.owner.get_all_tasks() 
            if not task.is_completed
        )
        return max(0, total_active_minutes - used_minutes)

    def generate_daily_plan(self) -> list[Task]:
        """Retrieves and organizes tasks across pets using Owner.get_all_tasks()."""
        # Pulls tasks directly from the Owner method to satisfy the multi-pet requirement
        all_tasks = self.owner.get_all_tasks()
        
        # Sort tasks by priority (High -> Medium -> Low)
        priority_map = {"High": 1, "Medium": 2, "Low": 3}
        all_tasks.sort(key=lambda t: priority_map.get(t.priority.capitalize(), 4))
        
        return all_tasks