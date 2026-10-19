"""PawPal+ core data models and scheduler meeting specific project requirements."""

from dataclasses import dataclass, field
from datetime import date, timedelta


@dataclass
class Task:
    task_id: int
    description: str
    duration: int
    priority: str
    time_slot: str = ""
    frequency: str = "Once"  # Added per your requirement
    is_completed: bool = False
    due_date: date | None = None

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

    def mark_task_completed(
        self, task: Task, completed_on: date | None = None
    ) -> Task | None:
        """Complete an owned task and create its next daily or weekly occurrence.

        Recurrence is calculated from ``completed_on`` or today's date. Return the
        new task for recurring tasks, or ``None`` when no next task is created.
        """
        pet = next(
            (
                pet
                for pet in self.owner.pets
                if any(owned_task is task for owned_task in pet.tasks)
            ),
            None,
        )
        if pet is None:
            raise ValueError("Cannot complete a task that is not assigned to this owner.")
        if task.is_completed:
            return None

        task.mark_completed()
        recurrence_days = {"daily": 1, "weekly": 7}.get(
            task.frequency.strip().casefold()
        )
        if recurrence_days is None:
            return None

        next_due_date = (completed_on or date.today()) + timedelta(
            days=recurrence_days
        )
        next_task = Task(
            task_id=max(
                (
                    owned_task.task_id
                    for owned_pet in self.owner.pets
                    for owned_task in owned_pet.tasks
                ),
                default=0,
            )
            + 1,
            description=task.description,
            duration=task.duration,
            priority=task.priority,
            time_slot=task.time_slot,
            frequency=task.frequency,
            due_date=next_due_date,
        )
        pet.add_task(next_task)
        return next_task

    def get_available_time(self, date: date) -> int:
        """Calculates available free time by reading from Owner.get_all_tasks()."""
        total_active_minutes = 720  # e.g., 12-hour window
        used_minutes = sum(
            task.duration 
            for task in self.owner.get_all_tasks() 
            if not task.is_completed
        )
        return max(0, total_active_minutes - used_minutes)

    def sort_by_time(self) -> list[Task]:
        """Return every owner's task sorted chronologically by its zero-padded HH:MM slot.

        Tasks with identical time slots retain their original order. The owner's
        stored task lists are not modified.
        """
        return sorted(
            self.owner.get_all_tasks(),
            key=lambda task: task.time_slot,
        )

    def filter_tasks(
        self, pet: Pet | None = None, is_completed: bool | None = None
    ) -> list[Task]:
        """Return tasks optionally filtered by pet and completion status.

        Omitting either argument leaves that attribute unrestricted. A pet must
        be the same pet object registered with this scheduler's owner.
        """
        pets = self.owner.pets if pet is None else [
            owned_pet for owned_pet in self.owner.pets if owned_pet is pet
        ]
        tasks = [task for owned_pet in pets for task in owned_pet.tasks]
        if is_completed is not None:
            tasks = [
                task for task in tasks if task.is_completed is is_completed
            ]
        return tasks

    def detect_time_conflicts(self) -> list[str]:
        """Return warnings for active tasks sharing an exact date and time slot.

        Tasks without a time slot and completed tasks are ignored. Tasks without
        an explicit due date are treated as scheduled for today; task durations
        are not used to detect partial overlaps.
        """
        tasks_by_time: dict[tuple[date, str], list[tuple[Pet, Task]]] = {}
        today = date.today()
        for pet in self.owner.pets:
            for task in pet.tasks:
                if task.is_completed or not task.time_slot:
                    continue
                scheduled_date = task.due_date or today
                tasks_by_time.setdefault(
                    (scheduled_date, task.time_slot), []
                ).append((pet, task))

        warnings = []
        for (scheduled_date, time_slot), scheduled_tasks in tasks_by_time.items():
            if len(scheduled_tasks) < 2:
                continue
            task_descriptions = ", ".join(
                f"{pet.name}: {task.description}" for pet, task in scheduled_tasks
            )
            warnings.append(
                f"WARNING: Schedule conflict on {scheduled_date} at {time_slot}: "
                f"{task_descriptions}"
            )
        return warnings

    def generate_daily_plan(self) -> list[Task]:
        """Return all pets' tasks sorted from high to low priority.

        Unknown priorities sort after High, Medium, and Low. This method does
        not filter by date, completion status, or available time.
        """
        # Pulls tasks directly from the Owner method to satisfy the multi-pet requirement
        all_tasks = self.owner.get_all_tasks()
        
        # Sort tasks by priority (High -> Medium -> Low)
        priority_map = {"High": 1, "Medium": 2, "Low": 3}
        all_tasks.sort(key=lambda t: priority_map.get(t.priority.capitalize(), 4))
        
        return all_tasks