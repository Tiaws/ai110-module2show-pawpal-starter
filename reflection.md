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

- What behaviors did you test?
- Why were these tests important?

**b. Confidence**

- How confident are you that your scheduler works correctly?
- What edge cases would you test next if you had more time?

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?
