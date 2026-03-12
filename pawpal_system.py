from typing import List


class Owner:
    """Represents a pet owner with time constraints and multiple pets."""
    
    def __init__(self, name: str, email: str, time_available: float, start_time: str, end_time:str ):
        self._name = name
        self._email = email
        self._time_available = time_available
        self._pets = []
        
    def get_name(self) -> str:
        """Returns the owner's name."""
        return self._name
    
    def get_email(self) -> str:
        """Returns the owner's email."""
        return self._email
    
    def set_email(self, email: str) -> None:
        """Updates the owner's email."""
        self._email = email
    
    def get_pets(self) -> List['Pet']:
        """Returns list of owner's pets."""
        return self._pets.copy()
    
    def get_time_available(self) -> float:
        """Returns owner's available time for pet care tasks."""
        if self._time_available < 0:
            raise ValueError("Available time cannot be negative.")
        return self._time_available
    
    def add_pet(self, pet: 'Pet') -> None:
        """Adds a pet to the owner's collection."""
        if pet not in self._pets:
            self._pets.append(pet)
        else:
            print(f"{pet._name} is already in the owner's collection.")
    
    def remove_pet(self, pet: 'Pet') -> None:
        """Removes a pet from the owner's collection."""
        if pet in self._pets:
            self._pets.remove(pet)
        else:
            raise ValueError(f"{pet._name} is not in the owner's collection.") 


class Pet:
    """Represents a pet with associated care tasks."""
    
    def __init__(self, name: str, species: str, breed: str, age: float):
        self._name = name
        self._species = species
        self._breed = breed
        self._age = age
        self._tasks = []
    
    def get_name(self) -> str:
        """Returns the pet's name."""
        return self._name
    
    def get_species(self) -> str:
        """Returns the pet's species."""
        return self._species
    
    def get_breed(self) -> str:
        """Returns the pet's breed."""
        return self._breed
    def get_age(self) -> float: 
        """Returns the pet's age."""
        return self._age
    
    def get_tasks(self) -> List['Task']:
        """Returns list of care tasks for this pet."""
        return self._tasks.copy()
    
    def add_task(self, task: 'Task') -> None:
        """Adds a care task for this pet."""
        if task not in self._tasks:
            self._tasks.append(task)
        else:
            print(f"Task '{task._name}' is already assigned to {self._name}.")
    
    def remove_task(self, task: 'Task') -> None:
        """Removes a care task for this pet."""
        self._tasks.remove(task)


class Task:
    """Represents a single pet care task with duration and priority."""
    
    def __init__(self, name: str, duration: float, priority: int, category: str, description: str = ""):
        self._name = name
        self._duration = duration
        self._priority = priority
        self._category = category
        self._description = description
        self._completed = False
        
        
        
    def get_name(self) -> str:
        """Returns the task's name."""
        return self._name
    def get_duration(self) -> float:
        """Returns the task's duration in hours."""
        return self._duration
    def get_priority(self) -> int:
        """Returns the task's priority level."""
        return self._priority
    def get_category(self) -> str:
        """Returns the task's category (e.g., feeding, grooming)."""
        return self._category
    def get_description(self) -> str:
        """Returns the task's description."""
        return self._description
    
    def mark_complete(self) -> None:
        """Marks the task as completed."""
        self._completed = True
        
    def is_completed(self) -> bool:
        """Returns whether the task is completed."""
        return self._completed
    
    def update_priority(self, priority: int) -> None:
        """Updates the task's priority level."""
        self._priority = priority
    
    def __str__(self) -> str:
        """Returns a readable string representation of the task."""
        return f"{self._name} (Priority: {self._priority}, Duration: {self._duration}h, Category: {self._category})"


class Scheduler:
    """Generates optimized daily schedules considering owner time and task priorities."""
    
    def __init__(self, owner: Owner):
        self._owner = owner
        self._pets = owner.get_pets() if owner else []
        self._daily_plan = []
    
    def get_all_tasks(self) -> List[Task]:
        """Returns a list of all tasks across all pets."""
        all_tasks = []
        for pet in self._pets:
            all_tasks.extend(pet.get_tasks())
        return all_tasks
    
    def generate_plan(self, date: str) -> List[Task]:
        """Generates a daily plan of tasks for the given date."""
        all_tasks = self.get_all_tasks()
        time_available = self._owner.get_time_available()
        
        # # Sort tasks by priority (higher priority first)
        # sorted_tasks = sorted(all_tasks, key=lambda task: task.get_priority(), reverse=True)
        
         # Sort tasks by duration (shortest first)
        sorted_tasks = sorted(all_tasks, key=lambda task: task.get_duration())
    
        
        # Greedily add tasks until time runs out
        self._daily_plan = []
        total_time = 0.0
        
        for task in sorted_tasks:
            if total_time + task.get_duration() <= time_available:
                self._daily_plan.append(task)
                total_time += task.get_duration()
        
        return self._daily_plan
    
    def optimize_plan(self) -> List[Task]:
        """Optimizes the current daily plan based on priorities and constraints."""
        if not self._daily_plan:
            return self._daily_plan
        
        # Re-sort the daily plan by priority to ensure optimization
        self._daily_plan.sort(key=lambda task: task.get_priority(), reverse=True)
        
        # Validate time constraints
        if self.check_time_constraints(self._daily_plan):
            return self._daily_plan
        else:
            # If constraints violated, remove lowest priority tasks
            while self._daily_plan and not self.check_time_constraints(self._daily_plan):
                self._daily_plan.pop()  # Remove last (lowest priority) task
            return self._daily_plan
    
    def check_time_constraints(self, tasks: List[Task]) -> bool:
        """Validates that total task duration fits within owner's available time."""
        total_duration = sum(task._duration for task in tasks)
        return total_duration <= self._owner.get_time_available()
    
    def get_daily_plan(self) -> List[Task]:
        """Returns the current daily plan."""
        return self._daily_plan.copy()
    
    def get_plan_explanation(self) -> str:
        """Returns explanation of why tasks were scheduled as they are."""
        if not self._daily_plan:
            return "No tasks scheduled. Either no tasks available or insufficient time."
        
        explanation = f"Daily Plan for {self._owner.get_name()}:\n"
        explanation += f"Available time: {self._owner.get_time_available()} hours\n"
        explanation += f"Scheduled tasks ({len(self._daily_plan)} total):\n"
        
        total_time = 0.0
        for i, task in enumerate(self._daily_plan, 1):
            explanation += f"{i}. {task.get_name()} (Priority: {task.get_priority()}, Duration: {task.get_duration()}h)\n"
            total_time += task.get_duration()
        
        explanation += f"\nTotal scheduled time: {total_time} hours\n"
        explanation += f"Remaining time: {self._owner.get_time_available() - total_time} hours"
        
        return explanation