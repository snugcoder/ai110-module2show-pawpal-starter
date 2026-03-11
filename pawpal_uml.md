# PawPal+ UML Class Diagram

```mermaid
classDiagram
    class Owner {
        -name: str
        -email: str
        -timeAvailable: float
        +getPets() List~Pet~
        +getTimeAvailable() float
        +addPet(pet: Pet) void
        +removePet(pet: Pet) void
    }

    class Pet {
        -name: str
        -species: str
        -breed: str
        -age: float
        -tasks: List~Task~
        +getTasks() List~Task~
        +addTask(task: Task) void
        +removeTask(task: Task) void
    }

    class Task {
        -name: str
        -duration: float
        -priority: int
        -category: str
        -completed: bool
        +markComplete() void
        +updatePriority(priority: int) void
    }

    class Scheduler {
        -owner: Owner
        -pets: List~Pet~
        -dailyPlan: List~Task~
        +generatePlan(date: str) List~Task~
        +optimizePlan() List~Task~
        +checkTimeConstraints(tasks: List~Task~) bool
        +getPlanExplanation() str
    }

    Owner --> Pet: owns *
    Pet --> Task: has *
    Scheduler --> Owner: schedules for, respects timeAvailable
    Scheduler --> Pet: considers
```

## Class Relationships

- **Owner → Pet** (owns *): One owner can have multiple pets
- **Pet → Task** (has *): Each pet can have multiple care tasks
- **Scheduler → Owner** (schedules for, respects timeAvailable): The scheduler coordinates with the owner and respects their time constraints
- **Scheduler → Pet** (considers): The scheduler considers all pets when generating plans
