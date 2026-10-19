# PawPal+ Project Reflection

- Enter owner and pet information.
- Add or edit care tasks, including their duration and priority.
- Generate and view a daily care plan that accounts for available time and task priorities.

## 1. System Design

**a. Initial design**

- Owner: Manages the owner's personal details and their list of pets, with methods to add pets, view all tasks, and update information.

Pet: Holds individual animal details (name, species, age) and a list of tasks, with methods to add/remove tasks and update details.

Task: Highly detailed, tracking IDs, descriptions, durations, priorities, time slots, and advanced features like recurrence, snooze options, and completion status.

Scheduler: Acted as an advanced logic handler with multiple built-in utilities to check available time, sort tasks by priority or time, detect scheduling conflicts, and generate daily plans.

Relationships: Linked hierarchically from Owner to Pet (one-to-many), Pet to Task (one-to-many), with the Scheduler reading data from the Owner

**b. Design changes**

- Did your design change during implementation?
- Yes
- If yes, describe at least one change and why you made it.
- Removed features like task recurrence (is_recurring, frequency, recurrence_end) and the snooze() method.

---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

- What constraints does your scheduler consider (for example: time, priority, preferences)?
- How did you decide which constraints mattered most?

**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.
- Why is that tradeoff reasonable for this scenario?

---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
- I asked for the bare bones of the implmenation and edited it from there. Also AI for generating test cases for test completion and Task Addtion
- What kinds of prompts or questions were most helpful?
- The ones where I added more requirements 

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
- For the generating the uml logic, as it was more complicated than needed
- How did you evaluate or verify what the AI suggested?
- By reading the code and verifying it myself 

---

## 4. Testing and Verification

**a. What you tested**

- I tested marking a task complete, by adding a task to a pet, sorting tasks by time, and filtering by pet and completion status. I also tested daily and weekly recurrence, confirmed one-time tasks do not repeat, and checked that duplicate task times are reported for the same pet and across pets.


**b. Confidence**

- I am reasonably confident in the tested behavior because all 10 tests pass. 
- If I had more time, I would test invalid or missing time formats, tasks with the same time on different dates, completed tasks in conflict checks. I would also test empty schedules and recurrence when a task has no due date.

---

## 5. Reflection

**a. What went well**

- Building the UML logic and tests helped verify that these features work as intended.

**b. What you would improve**

- I would make daily plans to use the asked date and the owner's actual available hours.

**c. Key takeaway**

- I learned that the design should match what the code actually implemented. Tests are useful for checking individual behaviors. AI suggestions can help me get started, but I still need to read the code and verify that it meets the project requirements.
