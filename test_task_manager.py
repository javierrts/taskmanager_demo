import json
from unittest.mock import MagicMock, patch

import pytest

from task_manager import Task, TaskManager


@pytest.fixture
def manager(tmp_path, monkeypatch):
    # Use an isolated temp file for each test so tests don't touch real tasks.json
    test_file = tmp_path / "tasks.json"
    monkeypatch.setattr(TaskManager, "filename", str(test_file))
    return TaskManager()


class TestTask:
    def test_task_str_not_completed(self):
        task = Task(1, "Buy milk")
        assert str(task) == "[ ] #1: #Buy milk"

    def test_task_str_completed(self):
        task = Task(1, "Buy milk", completed=True)
        assert str(task) == "[✓] #1: #Buy milk"

    def test_task_default_completed_false(self):
        task = Task(2, "Clean house")
        assert task.completed is False


class TestTaskManagerInit:
    def test_init_empty_when_no_file(self, manager):
        assert manager._tasks == []
        assert manager.next_id == 1

    def test_init_loads_existing_tasks(self, tmp_path, monkeypatch):
        test_file = tmp_path / "tasks.json"
        test_file.write_text(
            json.dumps(
                [{"id": 1, "description": "Existing task", "completed": False}]
            )
        )
        monkeypatch.setattr(TaskManager, "filename", str(test_file))
        tm = TaskManager()
        assert len(tm._tasks) == 1
        assert tm._tasks[0].description == "Existing task"
        assert tm.next_id == 2


class TestAddTask:
    def test_add_task_appends_task(self, manager):
        task = manager.add_task("Write report")
        assert task in manager._tasks
        assert task.description == "Write report"
        assert task.id == 1

    def test_add_task_increments_next_id(self, manager):
        manager.add_task("Task A")
        manager.add_task("Task B")
        assert manager.next_id == 3
        assert manager._tasks[0].id == 1
        assert manager._tasks[1].id == 2

    def test_add_task_persists_to_file(self, manager):
        manager.add_task("Persisted task")
        with open(manager.filename, "r") as f:
            data = json.load(f)
        assert len(data) == 1
        assert data[0]["description"] == "Persisted task"
        assert data[0]["completed"] is False


class TestAddComplexTask:
    @patch("task_manager.AIService")
    def test_add_complex_task_creates_subtasks(self, mock_ai_service_cls, manager):
        mock_instance = MagicMock()
        mock_instance.create_simple_task_from_complex.return_value = [
            "Subtask 1",
            "Subtask 2",
        ]
        mock_ai_service_cls.return_value = mock_instance

        manager.add_complex_task("Complex task description")

        assert len(manager._tasks) == 2
        assert manager._tasks[0].description == "Subtask 1"
        assert manager._tasks[1].description == "Subtask 2"

    @patch("task_manager.AIService")
    def test_add_complex_task_handles_error(self, mock_ai_service_cls, manager, capsys):
        mock_instance = MagicMock()
        mock_instance.create_simple_task_from_complex.return_value = [
            "Error: something went wrong"
        ]
        mock_ai_service_cls.return_value = mock_instance

        manager.add_complex_task("Bad description")

        assert manager._tasks == []
        captured = capsys.readouterr()
        assert "Error: something went wrong" in captured.out


class TestListTasks:
    def test_list_tasks_empty(self, manager, capsys):
        manager.list_tasks()
        captured = capsys.readouterr()
        assert "No tasks available." in captured.out

    def test_list_tasks_with_items(self, manager, capsys):
        manager.add_task("Task 1")
        capsys.readouterr()  # clear previous output
        manager.list_tasks()
        captured = capsys.readouterr()
        assert "Task 1" in captured.out


class TestCompleteTask:
    def test_complete_task_marks_completed(self, manager):
        task = manager.add_task("Task to complete")
        result = manager.complete_task(task.id)
        assert result.completed is True
        assert manager._tasks[0].completed is True

    def test_complete_task_persists_change(self, manager):
        task = manager.add_task("Task to complete")
        manager.complete_task(task.id)
        with open(manager.filename, "r") as f:
            data = json.load(f)
        assert data[0]["completed"] is True

    def test_complete_task_not_found(self, manager, capsys):
        result = manager.complete_task(999)
        assert result is None
        captured = capsys.readouterr()
        assert "Task with ID 999 not found." in captured.out


class TestEliminateTask:
    def test_eliminate_task_removes_task(self, manager):
        task = manager.add_task("Task to remove")
        manager.eliminate_task(task.id)
        assert manager._tasks == []

    def test_eliminate_task_persists_change(self, manager):
        task = manager.add_task("Task to remove")
        manager.eliminate_task(task.id)
        with open(manager.filename, "r") as f:
            data = json.load(f)
        assert data == []

    def test_eliminate_task_not_found(self, manager, capsys):
        result = manager.eliminate_task(999)
        assert result is None
        captured = capsys.readouterr()
        assert "Task with ID 999 not found." in captured.out

    def test_eliminate_task_keeps_other_tasks(self, manager):
        task1 = manager.add_task("Keep me")
        task2 = manager.add_task("Remove me")
        manager.eliminate_task(task2.id)
        assert len(manager._tasks) == 1
        assert manager._tasks[0].id == task1.id


class TestSaveLoadTasks:
    def test_save_tasks_writes_json(self, manager):
        manager.add_task("A")
        manager.add_task("B")
        with open(manager.filename, "r") as f:
            data = json.load(f)
        assert len(data) == 2
        assert {d["description"] for d in data} == {"A", "B"}

    def test_load_tasks_recomputes_next_id(self, tmp_path, monkeypatch):
        test_file = tmp_path / "tasks.json"
        test_file.write_text(
            json.dumps(
                [
                    {"id": 5, "description": "Task five", "completed": False},
                    {"id": 3, "description": "Task three", "completed": True},
                ]
            )
        )
        monkeypatch.setattr(TaskManager, "filename", str(test_file))
        tm = TaskManager()
        assert tm.next_id == 6

    def test_load_tasks_missing_file_defaults(self, tmp_path, monkeypatch):
        test_file = tmp_path / "nonexistent.json"
        monkeypatch.setattr(TaskManager, "filename", str(test_file))
        tm = TaskManager()
        assert tm._tasks == []
        assert tm.next_id == 1
