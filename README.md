# Smart Task Manager

A simple command-line task manager written in Python. Add, list, complete, and delete tasks through an interactive menu. Tasks are stored in memory only (they are not saved to disk between runs).

## Features

- Add a task with a text description
- List all tasks, showing a checkmark (`✓`) for completed ones
- Mark a task as completed by its ID
- Delete a task by its ID
- Simple interactive menu loop

## Requirements

- Python 3.10+ (uses the `match` statement)

## Project structure

```
main.py           # Entry point: menu loop and user interaction
task_manager.py   # Task and TaskManager classes (core logic)
```

## Usage

1. (Optional) Create and activate a virtual environment:
   ```bash
   python -m venv .venv
   source .venv/bin/activate   # Linux/macOS/WSL
   .venv\Scripts\Activate.ps1  # Windows PowerShell
   ```
2. Run the app:
   ```bash
   python main.py
   ```
3. Follow the on-screen menu:
   ```
   --- Smart task manager ---
   1 - Add task
   2 - List tasks
   3 - Complete task
   4 - Delete task
   5 - Exit
   ```

## Notes

- Task data is kept only in memory (`TaskManager.tasks`) and is lost when the program exits.
- Task IDs are assigned incrementally starting at `1`.
