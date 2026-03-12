from math import e
import streamlit as st
from pawpal_system import Owner, Pet, Task, Scheduler

# initializing pawpal objects
if "owner" not in st.session_state:
    st.session_state.owner = None
if "pet" not in st.session_state:
    st.session_state.pet = None
if "scheduler" not in st.session_state:
    st.session_state.scheduler = None
if "tasks" not in st.session_state:
    st.session_state.tasks = []

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")

st.title("🐾 PawPal+")

st.markdown(
    """
Welcome to the PawPal+ starter app.

This file is intentionally thin. It gives you a working Streamlit app so you can start quickly,
but **it does not implement the project logic**. Your job is to design the system and build it.

Use this app as your interactive demo once your backend classes/functions exist.
"""
)

with st.expander("Scenario", expanded=True):
    st.markdown(
        """
**PawPal+** is a pet care planning assistant. It helps a pet owner plan care tasks
for their pet(s) based on constraints like time, priority, and preferences.

You will design and implement the scheduling logic and connect it to this Streamlit UI.
"""
    )

with st.expander("What you need to build", expanded=True):
    st.markdown(
        """
At minimum, your system should:
- Represent pet care tasks (what needs to happen, how long it takes, priority)
- Represent the pet and the owner (basic info and preferences)
- Build a plan/schedule for a day that chooses and orders tasks based on constraints
- Explain the plan (why each task was chosen and when it happens)
"""
    )

st.divider()

st.subheader("Quick Demo Inputs (UI only)")
owner_name = st.text_input("Owner name", value="Jordan")
owner_email = st.text_input("Owner Email: ", value="jordan@email.com")
pet_name = st.text_input("Pet name", value="Mochi")
species = st.selectbox("Species", ["dog", "cat", "other"])
hours = st.number_input("Hours available today", value = 4.0)

if st.button("Save owner"):
    st.session_state.owner = Owner(name=owner_name, email=owner_email, time_available=hours)
    st.session_state.pet = Pet(name=pet_name, species=species, breed="Unknown", age=0, )
    st.session_state.owner.add_pet(st.session_state.pet)
    st.session_state.tasks = []
    st.success(f"Owner saved! Pet '{pet_name}' added.")

st.markdown("### Tasks")
st.caption("Add a few tasks. In your final version, these should feed into your scheduler.")

if "tasks" not in st.session_state:
    st.session_state.tasks = []

col1, col2, col3, col4 = st.columns(4)
with col1:
    task_title = st.text_input("Task title", value="Morning walk")
with col2:
    duration = st.number_input("Duration (minutes)", min_value=1, max_value=240, value=20)
with col3:
    priority = st.selectbox("Priority", ["low", "medium", "high"], index=2)
with col4:
    category = st.selectbox("Category", ["feeding", "exercise", "grooming", "medication", "other"])

priority_map = {"low":1, "medium":2, "high": 3}
if st.button("Add task"):
    if st.session_state.pet is None:
        st.warning("Save an owner and pet first")
    else:
        task = Task(
            name=task_title, 
            duration=duration/60.0, 
            priority=priority_map[priority], 
            category=category,
        )
        st.session_state.pet.add_task(task)
        st.session_state.tasks.append({
                 "title": task_title,
                 "duration (min)": int(duration),
                 "priority": priority,
                 "category": category,
             })

if st.session_state.tasks:
    st.write("Current tasks:")
    st.table(st.session_state.tasks)
else:
    st.info("No tasks yet. Add one above.")

st.divider()

st.subheader("Build Schedule")
st.caption("This button should call your scheduling logic once you implement it.")

if st.button("Generate schedule"):
    if st.session_state.owner is None:
        st.warning("Please create an owner first.")
    elif not st.session_state.tasks:
        st.warning("Save at least one task before generating a schedule")
    else:
        scheduler = Scheduler(st.session_state.owner)
        scheduled_tasks = scheduler.generate_plan(date="today")
        st.session_state.scheduler = scheduler
    st.markdown("### Schedule Explanation")
    st.text(scheduler.get_plan_explanation())
    
    if scheduled_tasks:
        st.markdown("### Scheduled Tasks")
        st.table([
            {
                "task": t.get_name(),
                "duration (hrs)": round(t.get_duration(), 2),
                "priority": t.get_priority(),
                "category": t.get_category(),
            }
            for t in scheduled_tasks
        ])
    else:
        st.info("No tasks fit within the available time. Try increasing hours or reducing durations.")
