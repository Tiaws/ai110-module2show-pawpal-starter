from datetime import date

import pytest

from pawpal_system import Owner, Pet, Scheduler, Task


def test_task_mark_completed_changes_status() -> None:
    task = Task(
        task_id=1,
        description="Feed pet",
        duration=10,
        priority="High",
    )

    assert task.is_completed is False

    task.mark_completed()

    assert task.is_completed is True


def test_adding_task_increases_pet_task_count() -> None:
    pet = Pet(name="Mochi", species="dog")
    task = Task(
        task_id=1,
        description="Morning walk",
        duration=30,
        priority="High",
    )
    initial_task_count = len(pet.tasks)

    pet.add_task(task)

    assert len(pet.tasks) == initial_task_count + 1
    assert pet.tasks[-1] is task


def test_scheduler_sort_by_time_orders_tasks_by_time_slot() -> None:
    pet = Pet(name="Mochi", species="dog")
    late_task = Task(
        task_id=1,
        description="Evening walk",
        duration=30,
        priority="Low",
        time_slot="17:30",
    )
    early_task = Task(
        task_id=2,
        description="Breakfast",
        duration=10,
        priority="High",
        time_slot="08:00",
    )
    pet.add_task(late_task)
    pet.add_task(early_task)
    scheduler = Scheduler(owner=Owner(name="Jordan", pets=[pet]))

    sorted_tasks = scheduler.sort_by_time()

    assert sorted_tasks == [early_task, late_task]
    assert pet.tasks == [late_task, early_task]


@pytest.mark.parametrize(
    ("frequency", "expected_due_date"),
    [
        ("Daily", date(2026, 10, 20)),
        ("Weekly", date(2026, 10, 26)),
    ],
)
def test_completing_recurring_task_schedules_next_occurrence(
    frequency: str, expected_due_date: date
) -> None:
    pet = Pet(name="Mochi", species="dog")
    task = Task(
        task_id=1,
        description="Give medication",
        duration=5,
        priority="High",
        time_slot="08:00",
        frequency=frequency,
    )
    pet.add_task(task)
    scheduler = Scheduler(owner=Owner(name="Jordan", pets=[pet]))

    next_task = scheduler.mark_task_completed(
        task, completed_on=date(2026, 10, 19)
    )

    assert task.is_completed is True
    assert next_task is not None
    assert next_task.due_date == expected_due_date
    assert next_task.is_completed is False
    assert next_task.task_id == 2
    assert next_task in pet.tasks


def test_completing_non_recurring_task_does_not_create_another_task() -> None:
    pet = Pet(name="Mochi", species="dog")
    task = Task(
        task_id=1,
        description="Trim nails",
        duration=15,
        priority="Medium",
    )
    pet.add_task(task)
    scheduler = Scheduler(owner=Owner(name="Jordan", pets=[pet]))

    next_task = scheduler.mark_task_completed(
        task, completed_on=date(2026, 10, 19)
    )

    assert task.is_completed is True
    assert next_task is None
    assert pet.tasks == [task]


@pytest.mark.parametrize("same_pet", [True, False])
def test_scheduler_reports_conflicts_for_tasks_at_same_time(
    same_pet: bool,
) -> None:
    first_pet = Pet(name="Mochi", species="dog")
    second_pet = first_pet if same_pet else Pet(name="Luna", species="cat")
    first_pet.add_task(
        Task(
            task_id=1,
            description="Morning walk",
            duration=30,
            priority="High",
            time_slot="08:00",
        )
    )
    second_pet.add_task(
        Task(
            task_id=2,
            description="Breakfast",
            duration=10,
            priority="High",
            time_slot="08:00",
        )
    )
    owner = Owner(name="Jordan", pets=[first_pet])
    if not same_pet:
        owner.add_pet(second_pet)
    scheduler = Scheduler(owner=owner)

    warnings = scheduler.detect_time_conflicts()

    assert len(warnings) == 1
    assert "WARNING" in warnings[0]
    assert "08:00" in warnings[0]
    assert "Morning walk" in warnings[0]
    assert "Breakfast" in warnings[0]


def test_scheduler_does_not_report_tasks_at_different_times_as_conflicts() -> None:
    pet = Pet(name="Mochi", species="dog")
    pet.add_task(
        Task(
            task_id=1,
            description="Morning walk",
            duration=30,
            priority="High",
            time_slot="08:00",
        )
    )
    pet.add_task(
        Task(
            task_id=2,
            description="Breakfast",
            duration=10,
            priority="High",
            time_slot="08:15",
        )
    )
    scheduler = Scheduler(owner=Owner(name="Jordan", pets=[pet]))

    assert scheduler.detect_time_conflicts() == []


def test_scheduler_filters_tasks_by_pet_and_completion_status() -> None:
    dog = Pet(name="Mochi", species="dog")
    cat = Pet(name="Luna", species="cat")
    completed_task = Task(
        task_id=1,
        description="Breakfast",
        duration=10,
        priority="High",
        is_completed=True,
    )
    pending_task = Task(
        task_id=2,
        description="Evening walk",
        duration=30,
        priority="Medium",
    )
    dog.add_task(completed_task)
    cat.add_task(pending_task)
    scheduler = Scheduler(owner=Owner(name="Jordan", pets=[dog, cat]))

    assert scheduler.filter_tasks(pet=dog) == [completed_task]
    assert scheduler.filter_tasks(is_completed=False) == [pending_task]
    assert scheduler.filter_tasks(pet=dog, is_completed=True) == [completed_task]
    assert scheduler.filter_tasks(pet=dog, is_completed=False) == []