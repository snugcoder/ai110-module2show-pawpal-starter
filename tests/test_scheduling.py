import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pytest
from pawpal_system import Owner, Pet, Task, Scheduler
from main import filter_tasks_by_completion


# --- helpers ---

def make_owner(hours=4.0):
    return Owner(name="Test", email="test@test.com", time_available=hours,
                 start_time="08:00", end_time="16:00")

def make_pet(owner, name="Buddy"):
    pet = Pet(name=name, species="dog", breed="Mixed", age=2)
    owner.add_pet(pet)
    return pet


# ---------------------------------------------------------------
# Sorting: generate_plan sorts by duration (shortest first)
# ---------------------------------------------------------------

class TestGeneratePlanSorting:

    def test_shorter_task_appears_before_longer_task(self):
        owner = make_owner(10.0)
        pet = make_pet(owner)
        long_task = Task("Long", 3.0, 1, "exercise")
        short_task = Task("Short", 0.5, 1, "feeding")
        pet.add_task(long_task)
        pet.add_task(short_task)

        plan = Scheduler(owner).generate_plan("today")

        assert plan[0] == short_task
        assert plan[1] == long_task

    def test_plan_durations_are_in_ascending_order(self):
        owner = make_owner(10.0)
        pet = make_pet(owner)
        pet.add_task(Task("Long",   3.0, 1, "exercise"))
        pet.add_task(Task("Short",  0.5, 1, "feeding"))
        pet.add_task(Task("Medium", 1.5, 2, "grooming"))

        plan = Scheduler(owner).generate_plan("today")
        durations = [t.get_duration() for t in plan]

        assert durations == sorted(durations)

    def test_high_priority_long_task_comes_after_low_priority_short_task(self):
        """Priority does not affect order — duration is the sort key."""
        owner = make_owner(10.0)
        pet = make_pet(owner)
        high_pri_long = Task("ImportantLong", 3.0, 10, "exercise")
        low_pri_short = Task("MinorShort",    0.5,  1, "feeding")
        pet.add_task(high_pri_long)
        pet.add_task(low_pri_short)

        plan = Scheduler(owner).generate_plan("today")

        assert plan[0] == low_pri_short
        assert plan[1] == high_pri_long


# ---------------------------------------------------------------
# Filtering: generate_plan excludes tasks that overflow time budget
# ---------------------------------------------------------------

class TestGeneratePlanFiltering:

    def test_task_exceeding_budget_is_excluded(self):
        owner = make_owner(1.0)
        pet = make_pet(owner)
        fits = Task("Short", 0.5, 1, "feeding")
        too_long = Task("Long", 2.0, 1, "exercise")
        pet.add_task(fits)
        pet.add_task(too_long)

        plan = Scheduler(owner).generate_plan("today")

        assert fits in plan
        assert too_long not in plan

    def test_task_exactly_filling_budget_is_included(self):
        owner = make_owner(1.0)
        pet = make_pet(owner)
        exact = Task("Exact", 1.0, 1, "feeding")
        pet.add_task(exact)

        plan = Scheduler(owner).generate_plan("today")

        assert exact in plan

    def test_all_tasks_exceed_budget_returns_empty(self):
        owner = make_owner(0.1)
        pet = make_pet(owner)
        pet.add_task(Task("Big1", 1.0, 1, "feeding"))
        pet.add_task(Task("Big2", 2.0, 2, "exercise"))

        plan = Scheduler(owner).generate_plan("today")

        assert plan == []

    def test_all_tasks_fit_all_are_included(self):
        owner = make_owner(10.0)
        pet = make_pet(owner)
        tasks = [
            Task("Feed",  0.5, 1, "feeding"),
            Task("Walk",  1.0, 2, "exercise"),
            Task("Groom", 0.5, 3, "grooming"),
        ]
        for t in tasks:
            pet.add_task(t)

        plan = Scheduler(owner).generate_plan("today")

        assert len(plan) == 3

    def test_no_tasks_returns_empty_plan(self):
        owner = make_owner(4.0)
        make_pet(owner)

        plan = Scheduler(owner).generate_plan("today")

        assert plan == []

    def test_greedy_packs_shorter_tasks_over_one_longer_task(self):
        """Two short tasks that fit together are preferred over one long task
        because sorting by duration puts the short ones first."""
        owner = make_owner(1.5)
        pet = make_pet(owner)
        long_task = Task("Long",   1.2, 5, "exercise")  # fits alone, but appears last
        short1    = Task("Short1", 0.5, 1, "feeding")
        short2    = Task("Short2", 0.5, 1, "feeding")
        short3    = Task("Short3", 0.7, 1, "feeding")   # would overflow after short1+short2
        pet.add_task(long_task)
        pet.add_task(short1)
        pet.add_task(short2)
        pet.add_task(short3)

        plan = Scheduler(owner).generate_plan("today")

        # Sorted order: short1(0.5), short2(0.5), short3(0.7), long(1.2)
        # Greedy: 0.5 -> 1.0 -> 1.0+0.7=1.7 exceeds 1.5, skip -> 1.0+1.2=2.2 exceeds, skip
        assert short1 in plan
        assert short2 in plan
        assert short3 not in plan
        assert long_task not in plan


# ---------------------------------------------------------------
# check_time_constraints
# ---------------------------------------------------------------

class TestCheckTimeConstraints:

    def test_tasks_within_budget_returns_true(self):
        owner = make_owner(4.0)
        make_pet(owner)
        scheduler = Scheduler(owner)
        tasks = [Task("Feed", 1.0, 1, "feeding"), Task("Walk", 1.0, 2, "exercise")]

        assert scheduler.check_time_constraints(tasks) is True

    def test_tasks_exactly_at_budget_returns_true(self):
        owner = make_owner(2.0)
        make_pet(owner)
        scheduler = Scheduler(owner)
        tasks = [Task("Feed", 1.0, 1, "feeding"), Task("Walk", 1.0, 2, "exercise")]

        assert scheduler.check_time_constraints(tasks) is True

    def test_tasks_over_budget_returns_false(self):
        owner = make_owner(1.5)
        make_pet(owner)
        scheduler = Scheduler(owner)
        tasks = [Task("Feed", 1.0, 1, "feeding"), Task("Walk", 1.0, 2, "exercise")]

        assert scheduler.check_time_constraints(tasks) is False

    def test_empty_task_list_returns_true(self):
        owner = make_owner(4.0)
        make_pet(owner)
        scheduler = Scheduler(owner)

        assert scheduler.check_time_constraints([]) is True


# ---------------------------------------------------------------
# optimize_plan: re-sorts by priority, trims if over budget
# ---------------------------------------------------------------

class TestOptimizePlan:

    def test_optimize_sorts_by_priority_descending(self):
        owner = make_owner(10.0)
        pet = make_pet(owner)
        low = Task("Low", 0.5, 1, "feeding")
        med = Task("Med", 0.5, 2, "grooming")
        high = Task("High", 0.5, 3, "exercise")
        pet.add_task(low)
        pet.add_task(high)
        pet.add_task(med)

        scheduler = Scheduler(owner)
        scheduler.generate_plan("today")
        plan = scheduler.optimize_plan()

        assert plan[0] == high
        assert plan[1] == med
        assert plan[2] == low

    def test_optimize_trims_until_time_constraint_satisfied(self):
        """If the plan exceeds budget, lowest-priority tasks are removed until it fits."""
        owner = make_owner(1.5)
        pet = make_pet(owner)
        t_high = Task("HighPri", 1.0, 3, "feeding")
        t_low  = Task("LowPri",  0.5, 1, "exercise")
        pet.add_task(t_high)
        pet.add_task(t_low)

        scheduler = Scheduler(owner)
        scheduler.generate_plan("today")
        # Inject an extra task to force a constraint violation
        t_extra = Task("Extra", 0.5, 2, "grooming")
        scheduler._daily_plan.append(t_extra)  # total = 2.0 > 1.5

        plan = scheduler.optimize_plan()

        assert scheduler.check_time_constraints(plan) is True

    def test_optimize_empty_plan_returns_empty(self):
        owner = make_owner(4.0)
        make_pet(owner)
        scheduler = Scheduler(owner)

        assert scheduler.optimize_plan() == []


# ---------------------------------------------------------------
# get_all_tasks: aggregates across multiple pets
# ---------------------------------------------------------------

class TestGetAllTasks:

    def test_aggregates_tasks_from_multiple_pets(self):
        owner = make_owner(10.0)
        pet1 = Pet("Buddy",   "dog", "Mixed",   2)
        pet2 = Pet("Mittens", "cat", "Persian", 3)
        owner.add_pet(pet1)
        owner.add_pet(pet2)
        t1 = Task("Walk Buddy",    1.0, 2, "exercise")
        t2 = Task("Feed Mittens",  0.5, 3, "feeding")
        pet1.add_task(t1)
        pet2.add_task(t2)

        all_tasks = Scheduler(owner).get_all_tasks()

        assert t1 in all_tasks
        assert t2 in all_tasks
        assert len(all_tasks) == 2

    def test_owner_with_no_pets_returns_empty(self):
        owner = make_owner(4.0)

        assert Scheduler(owner).get_all_tasks() == []

    def test_pet_with_no_tasks_contributes_nothing(self):
        owner = make_owner(4.0)
        make_pet(owner)

        assert Scheduler(owner).get_all_tasks() == []

    def test_task_count_matches_sum_across_all_pets(self):
        owner = make_owner(10.0)
        pet1 = make_pet(owner, "Dog")
        pet2 = make_pet(owner, "Cat")
        pet1.add_task(Task("Walk",  1.0, 2, "exercise"))
        pet1.add_task(Task("Feed",  0.5, 3, "feeding"))
        pet2.add_task(Task("Brush", 0.5, 1, "grooming"))

        all_tasks = Scheduler(owner).get_all_tasks()

        assert len(all_tasks) == 3


# ---------------------------------------------------------------
# filter_tasks_by_completion (main.py)
# NOTE: This function accesses `task.completed` but Task stores the
# attribute as `task._completed`. These tests will currently raise
# AttributeError, exposing that bug.
# ---------------------------------------------------------------

class TestFilterTasksByCompletion:

    def test_returns_only_completed_tasks(self):
        t1 = Task("Feed", 1.0, 1, "feeding")
        t2 = Task("Walk", 0.5, 2, "exercise")
        t1.mark_complete()

        result = filter_tasks_by_completion([t1, t2], completed=True)

        assert t1 in result
        assert t2 not in result

    def test_returns_only_incomplete_tasks(self):
        t1 = Task("Feed", 1.0, 1, "feeding")
        t2 = Task("Walk", 0.5, 2, "exercise")
        t1.mark_complete()

        result = filter_tasks_by_completion([t1, t2], completed=False)

        assert t2 in result
        assert t1 not in result

    def test_empty_list_returns_empty(self):
        assert filter_tasks_by_completion([], completed=True) == []

    def test_no_completed_tasks_filter_completed_returns_empty(self):
        tasks = [Task("Feed", 1.0, 1, "feeding"), Task("Walk", 0.5, 2, "exercise")]

        result = filter_tasks_by_completion(tasks, completed=True)

        assert result == []

    def test_default_parameter_filters_for_completed(self):
        t1 = Task("Feed", 1.0, 1, "feeding")
        t1.mark_complete()
        t2 = Task("Walk", 0.5, 2, "exercise")

        result = filter_tasks_by_completion([t1, t2])

        assert t1 in result
        assert t2 not in result
