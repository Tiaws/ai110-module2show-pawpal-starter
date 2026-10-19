# PawPal+ (Module 2 Project)

You are building **PawPal+**, a Streamlit app that helps a pet owner plan care tasks for their pet.

## Scenario

A busy pet owner needs help staying consistent with pet care. They want an assistant that can:

- Track pet care tasks (walks, feeding, meds, enrichment, grooming, etc.)
- Consider constraints (time available, priority, owner preferences)
- Produce a daily plan and explain why it chose that plan

Your job is to design the system first (UML), then implement the logic in Python, then connect it to the Streamlit UI.

## Sample Output
Today's Schedule
08:00 - Morning walk for Mochi (30 min, priority: High)
08:45 - Breakfast for Mochi (10 min, priority: High)
09:00 - Medication for Luna (5 min, priority: High)
17:30 - Playtime for Luna (15 min, priority: Medium)

## Implementation Summary

`Owner` keeps the household's pets, and each `Pet` stores its care `Task`s. Tasks hold details such as duration, priority, and time slot, and can be marked complete or edited. `Scheduler` gathers tasks across the owner's pets, estimates available time, and orders tasks by priority. The sample script in `main.py` prints those tasks by their assigned time slot.

## Testing PawPal+
Confidence Level: 2 stars
python -m pytest
============================= test session starts ==============================
platform win32 -- Python 3.13.15, pytest-9.1.1, pluggy-1.7.0
rootdir: C:\Users\jijot\OneDrive - The University of Texas at Dallas\Documents\Code pat\ai110-module2show-pawpal-starter
plugins: anyio-4.15.1
collected 10 items                                                              

tests\test_pawpal.py ..........                                           [100%]

============================== 10 passed in 0.06s ==============================
(.venv) PS C:\Users\jijot\OneDrive - The University of Texas at Dallas\Documents\Code pat\ai110-module2show-pawpal-starter> 

## What you will build

Your final app should:

- Let a user enter basic owner + pet info
- Let a user add/edit tasks (duration + priority at minimum)
- Generate a daily schedule/plan based on constraints and priorities
- Display the plan clearly (and ideally explain the reasoning)
- Include tests for the most important scheduling behaviors

## Getting started

### Setup

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### Suggested workflow

1. Read the scenario carefully and identify requirements and edge cases.
2. Draft a UML diagram (classes, attributes, methods, relationships).
3. Convert UML into Python class stubs (no logic yet).
4. Implement scheduling logic in small increments.
5. Add tests to verify key behaviors.
6. Connect your logic to the Streamlit UI in `app.py`.
7. Refine UML so it matches what you actually built.

## 🖥️ Sample Output

Paste a sample of your app's CLI or Streamlit output here so a reader can see what a generated plan looks like:

```
# e.g.:
# Daily plan for Biscuit (Golden Retriever):
#   08:00 — Morning walk (30 min) [priority: high]
#   09:00 — Feeding (10 min) [priority: high]
#   ...
```

## 🧪 Testing PawPal+

```bash
# Run the full test suite:
pytest

# Run with coverage:
pytest --cov
```

Sample test output:

```
# Paste your pytest output here
```

## 📐 Smarter Scheduling

The scheduler includes these lightweight scheduling helpers:

| Feature | Method(s) | Notes |
|---------|-----------|-------|
| Task sorting | `Scheduler.sort_by_time()`, `Scheduler.generate_daily_plan()` | `sort_by_time()` returns all tasks in zero-padded `HH:MM` order without changing the pets' stored task lists. `generate_daily_plan()` orders all tasks by priority: High, Medium, Low, then unrecognized priorities. |
| Filtering | `Scheduler.filter_tasks(pet=None, is_completed=None)` | Optionally select one of the owner's pets and/or tasks matching the completion status. Omitting a filter leaves that dimension unrestricted. |
| Conflict detection | `Scheduler.detect_time_conflicts()` | Returns warning strings when two or more incomplete tasks share the exact same time slot and date, including across different pets. Tasks without a time are skipped; a missing due date is treated as today. It detects matching start times, not duration overlaps. |
| Recurring tasks | `Scheduler.mark_task_completed(task, completed_on=None)` | Marks an owned task complete. `"Daily"` creates the next task one day later; `"Weekly"` creates one seven days later, calculated with `timedelta`. The new task is assigned to the same pet with a new task ID. One-time tasks do not create another occurrence. |

## 🚀 Demo Walkthrough

### 1. UI Features & User Actions
* **Owner & Pet Registration:** Easily add and manage multiple pets under a single owner profile.
* **Task Management:** Add custom care tasks including descriptions, specific time slots, durations, and priority levels (High/Medium/Low).
* **Smart Daily Plan:** View a structured, conflict-free schedule generated automatically by the backend scheduler.

### 2. Example Workflow
1. **Setup:** Launch the app and input the owner's name, then add two pets: *Max (Dog)* and *Luna (Cat)*.
2. **Add Tasks:** Schedule a High-Priority "Morning Walk" for Max at 08:00, a Medium-Priority "Feeding" at 08:30, and a "Medication" reminder.
3. **View Schedule:** Navigate to the daily schedule view to see your tasks organized chronologically with conflict warnings (if any overlap occurs).

### 3. Key Scheduler Behaviors
* **Sorting & Filtering:** Automatically organizes tasks chronologically using `Scheduler.sort_tasks_by_time()`.
* **Conflict Detection:** Flags overlapping time slots to alert the user of scheduling bottlenecks.
* **Recurring Tasks:** Automatically generates the next cycle's due date when a recurring daily/weekly task is completed.

### 4. Sample CLI Output (`main.py`)
```text
=== PawPal+ System Initialized ===
Owner: Sarah
Pets registered: Max (Dog), Luna (Cat)

--- Added Tasks ---
[Max] Morning Walk - 08:00 (Duration: 30 mins, Priority: High)
[Max] Feeding - 08:15 (Duration: 15 mins, Priority: Medium) -> ⚠️ CONFLICT DETECTED with Morning Walk!
[Luna] Vet Medication - 09:00 (Duration: 10 mins, Priority: High)

--- Today's Sorted Schedule ---
1. 08:00 | Max: Morning Walk (High)
2. 08:15 | Max: Feeding (Medium)
3. 09:00 | Luna: Vet Medication (High)

**Screenshot or video** *(optional)*: <!-- Insert a screenshot or link to a demo video here -->
