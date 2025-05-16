# MathStro Scheduler

A heuristic teacher-instructor scheduler optimization tool that efficiently matches sessions with available instructors based on time constraints and preferences.

![Scheduler Diagram](./media/scheduler.png)

## Overview

MathStro Scheduler uses a heuristic approach to solve the optimality problem of matching class sessions with instructor availability. The algorithm aims to create an optimal configuration where:

1. All session slots are filled with qualified instructors
2. Instructors are assigned to consecutive sessions on the same day when possible
3. Instructor preferences and availability constraints are respected

## Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/mathstro_scheduler.git
cd mathstro_scheduler

# Install the package
pip install -e .
```

## Input Data Format

The scheduler expects two tab-delimited text files as input:

### Sessions File

Contains information about available class sessions:

```
Day	Time Slot
Monday	09:00 AM - 10:00 AM
Monday	10:00 AM - 11:00 AM
Tuesday	09:00 AM - 10:00 AM
...
```

### Instructor Preferences File

Contains information about instructor availability:

```
ID	Name	Day	Time Slot
gacu001	Uriel Garcilazo	Monday	09:00 AM - 10:00 AM
gacu001	Uriel Garcilazo	Monday	10:00 AM - 11:00 AM
jdoe002	John Doe	Monday	10:00 AM - 11:00 AM
...
```

## Usage

### Basic Usage

```python
from mathstro_scheduler import scheduler

# Run the scheduler with default parameters
scheduler(
    epochs=100,
    replicates=5,
    max_attempts=10,
    session_file="path/to/sessions.txt",
    instructor_pref_file="path/to/instructors_prefs.txt",
    output_path="./output",
    verbose=True
)
```

### Parameters

- `epochs`: Number of epochs to run the algorithm (int)
- `replicates`: Number of replicates to run per epoch (int)
- `max_attempts`: Maximum number of attempts to assign a session to an instructor (int)
- `session_file`: Path to the input file containing session data (str)
- `instructor_pref_file`: Path to the input file containing instructor preference data (str)
- `output_path`: Directory to save the output file (str, default="./")
- `verbose`: Whether to print progress information (bool, default=True)

## Algorithm

The scheduling algorithm works as follows:

1. For a specified number of epochs:
   - For each session in the list of sessions:
     - Randomly sample from the list of instructor preferences
     - Try to assign an instructor to the session based on availability
     - If successful, break and move to the next session
     - If unsuccessful after max_attempts, move to the next session

2. Score assignments based on:
   - Penalty of -5 for each unfilled session
   - Reward of +2 if adjacent sessions have the same instructor on the same day

3. Keep track of the best session assignments and scores across all epochs

4. Output the final assignments as a tab-delimited text file

## Output Format

The scheduler produces a tab-delimited text file with the following format:

```
Session.week_day	Session.start_time_code - Session.end_time_code	InstructorPref.instructor_uid	InstructorPref.name
Monday	09:00 AM - 10:00 AM	gacu001	Uriel Garcilazo
Monday	10:00 AM - 11:00 AM	gacu001	Uriel Garcilazo
...
```

## Example

```python
from mathstro_scheduler import scheduler

# Run the scheduler with the provided example data
scheduler(
    epochs=50,
    replicates=3,
    max_attempts=5,
    session_file="examples/sessions.txt",
    instructor_pref_file="examples/instructors_prefs.txt",
    output_path="./results"
)
```

"# mathstroScheduler" 
