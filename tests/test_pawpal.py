from pawpal_system import Pet, Task


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