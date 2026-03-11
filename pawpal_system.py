from typing import List


class Owner:
    """Represents a pet owner with time constraints and multiple pets."""
    
    def __init__(self, name: str, email: str, time_available: float):
        self._name = name
        self._email = email
        self._time_available = time_available
        self._pets = []
    
    def get_pets(self) -> List['Pet']:
        """Returns list of owner's pets."""
        pass
    
    def get_time_available(self) -> float:
        """Returns owner's available time for pet care tasks."""
        pass
    
    def add_pet(self, pet: 'Pet') -> None:
        """Adds a pet to the owner's collection."""
        pass
    
    def remove_pet(self, pet: 'Pet') -> None:
        """Removes a pet from the owner's collection."""
        pass


class Pet:
    """Represents a pet with associated care tasks."""
    
    def __init__(self, name: str, species: str, breed: str, age: float):
        self._name = name
        self._species = species
        self._breed = breed
        self._age = age
        self._tasks = []
    
    def get_tasks(self) -> List['Task']:
        """Returns list of care tasks for this pet."""
        pass
    
    def add_task(self, task: 'Task') -> None:
        """Adds a care task for this pet."""
        pass
    
    def remove_task(self, task: 'Task') -> None:
        """Removes a care task for this pet."""
        pass


class Task:
    """Represents a single pet care task with duration and priority."""
    
    def __init__(self, name: str, duration: float, priority: int, category: str):
        self._name = name
        self._duration = duration
        self._priority = priority
        self._category = category
        self._completed = False
    
    def mark_complete(self) -> None:
        """Marks the task as completed."""
        pass
    
    def update_priority(self, priority: int) -> None:
        """Updates the task's priority level."""
        pass


class Scheduler:
    """Generates optimized daily schedules considering owner time and task priorities."""
    
    def __init__(self, owner: Owner):
        self._owner = owner
        self._pets = owner.get_pets() if owner else []
        self._daily_plan = []
    
    def generate_plan(self, date: str) -> List[Task]:
        """Generates a daily plan of tasks for the given date."""
        pass
    
    def optimize_plan(self) -> List[Task]:
        """Optimizes the current daily plan based on priorities and constraints."""
        pass
    
    def check_time_constraints(self, tasks: List[Task]) -> bool:
        """Validates that total task duration fits within owner's available time."""
        pass
    
    def get_plan_explanation(self) -> str:
        """Returns explanation of why tasks were scheduled as they are."""
        pass
