# Smart Task Manager

A simple command-line task manager written in Python. Add, list, complete, and delete tasks through an interactive menu. Tasks are persisted to a local `tasks.json` file, so they are kept between runs. It also includes an AI-powered feature to break down a complex task into smaller subtasks using the Gemini API.

## Features

- Add a task with a text description
- Add a complex task and let AI (Gemini) split it into 3-5 simpler subtasks automatically
- List all tasks, showing a checkmark (`✓`) for completed ones
- Mark a task as completed by its ID
- Delete a task by its ID
- Tasks are automatically saved to `tasks.json` (pretty-printed with indentation) after every change and reloaded on startup
- Simple interactive menu loop with numeric input validation

## Requirements

- Python 3.10+ (uses the `match` statement)
- A [Gemini API key](https://aistudio.google.com/apikey) (free tier available) to use the AI subtask feature

## Project structure

```
main.py                # Entry point: menu loop and user interaction
task_manager.py         # Task and TaskManager classes (core logic + JSON persistence)
ai_service.py            # AIService: wraps Gemini API calls (OpenAI-compatible endpoint)
test_task_manager.py    # pytest test suite for Task and TaskManager
tasks.json               # Auto-generated data file (ignored by git, created on first run)
.env                     # Local secrets (GEMINI_API_KEY), ignored by git
requirements.txt         # Python dependencies
```

## Configuration

The AI subtask feature needs a Gemini API key. Create a `.env` file in the project root (already excluded from git):

```
GEMINI_API_KEY=your-api-key-here
```

Without this variable, `AIService` raises a `RuntimeError` when instantiated, but the rest of the app (add/list/complete/delete tasks) works normally without it.

## Usage

1. Create and activate a virtual environment:
   ```bash
   python -m venv .venv
   source .venv/bin/activate   # Linux/macOS/WSL
   .venv\Scripts\Activate.ps1  # Windows PowerShell
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the app:
   ```bash
   python main.py
   ```
4. Follow the on-screen menu (enter a number):
   ```
   --- Smart task manager ---
   1 - Add task
   2 - Add complex task with AI
   3 - List tasks
   4 - Complete task
   5 - Delete task
   6 - Exit
   ```

## Testing

Unit tests are written with `pytest` and cover `Task` and `TaskManager` (including a mocked `AIService`, so no real API calls or key are needed to run them):

```bash
pytest test_task_manager.py -v
```

## Notes

- Task data is stored in `tasks.json` in the project root, created automatically the first time you add a task. This file is excluded from version control via `.gitignore`.
- Task IDs are assigned incrementally starting at `1`, and continue from the highest existing ID after reloading from `tasks.json`.
- Non-numeric menu input is handled gracefully with a validation message instead of crashing.
- The AI subtask feature (`AIService.create_simple_task_from_complex`) calls the Gemini API via its OpenAI-compatible endpoint and requires network access and a valid `GEMINI_API_KEY`.

