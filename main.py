"""Create and display a sample PawPal+ schedule."""

from pawpal_system import Owner, Pet, Scheduler, Task


def main() -> None:
    owner = Owner(name="Jordan")

    dog = Pet(name="Mochi", species="dog")
    cat = Pet(name="Luna", species="cat")
    owner.add_pet(dog)
    owner.add_pet(cat)

    dog.add_task(
        Task(
            task_id=1,
            description="Morning walk",
            duration=30,
            priority="High",
            time_slot="08:00",
        )
    )
    dog.add_task(
        Task(
            task_id=2,
            description="Breakfast",
            duration=10,
            priority="High",
            time_slot="08:45",
        )
    )
    cat.add_task(
        Task(
            task_id=3,
            description="Medication",
            duration=5,
            priority="High",
            time_slot="08:00",
        )
    )
    cat.add_task(
        Task(
            task_id=4,
            description="Playtime",
            duration=15,
            priority="Medium",
            time_slot="17:30",
        )
    )

    scheduler = Scheduler(owner=owner)
    for warning in scheduler.detect_time_conflicts():
        print(warning)

    plan = sorted(
        scheduler.generate_daily_plan(),
        key=lambda task: task.time_slot,
    )
    pet_names = {
        task.task_id: pet.name
        for pet in owner.pets
        for task in pet.tasks
    }

    print("Today's Schedule")
    for task in plan:
        print(
            f"{task.time_slot} - {task.description} "
            f"for {pet_names[task.task_id]} "
            f"({task.duration} min, priority: {task.priority})"
        )


if __name__ == "__main__":
    main()