from pawpal_system import Owner, Pet, Task, Scheduler
# added filtering here
def filter_tasks_by_completion(tasks, completed: bool = True):
    """Return only tasks matching the completed flag."""
    return [task for task in tasks if task.is_completed() == completed]

if __name__ == "__main__":
    # Create an owner with time constraints
    owner = Owner(name="Alice", email="alice@example.com", time_available=8.0)
    print(f"Owner Name: {owner.get_name()}")
    print(f"Owner Email: {owner.get_email()}")
    
    pet = Pet(name="Buddy", species="Dog", breed="Golden Retriever", age=3)
    owner.add_pet(pet)
    pet2 = Pet(name="Mittens", species="Cat", breed="Siamese", age=2)
    owner.add_pet(pet2)
    
    task1 = Task(name="task1", category="Feeding", description="Feed Buddy", duration=0.5, priority=1)
    task2 = Task(name="task2", category="Exercise", description="Walk Buddy", duration=1.0, priority=2)
    task3 = Task(name="task3", category="Play", description="Play with Mittens", duration=0.5, priority=1)
    pet.add_task(task1)
    pet.add_task(task2)
    pet2.add_task(task3)
    
    owner_schedule = Scheduler(owner)
    owner_schedule.generate_plan(date="today")
    print(owner_schedule.get_plan_explanation())
    
    all_tasks = owner_schedule.get_all_tasks()  # or however you collect tasks
    completed_tasks = filter_tasks_by_completion(all_tasks, completed=True)
    incomplete_tasks = filter_tasks_by_completion(all_tasks, completed=False)

    print("Completed tasks:")
    for t in completed_tasks:
        print("-", t.get_name())

    print("Incomplete tasks:")
    for t in incomplete_tasks:
        print("-", t.get_name())