import json
from ai_service import AIService
class Task:

    def __init__(self, id, description, completed=False):
        self.id = id
        self.description = description
        self.completed = completed

    def __str__(self):
        status = "✓" if self.completed else " "
        return f"[{status}] #{self.id}: #{self.description}"

class TaskManager:

    filename = "tasks.json"

    def __init__(self):
        self._tasks = []
        self.next_id = 1
        self.load_tasks()


    def add_task(self, description):
        task = Task(self.next_id, description)
        self._tasks.append(task)
        self.next_id += 1
        self.save_tasks()
        print (f"Task added: {task}")
        return task
    
    def add_complex_task(self, description):
        ai_service = AIService()
        subtasks = ai_service.create_simple_task_from_complex(description)
        if  subtasks[0].startswith("Error"):
            print(subtasks[0])
        else:
            for subtask in subtasks:
                self.add_task(subtask)
            print(f"Complex task added with {len(subtasks)} subtasks.")
        

    def list_tasks(self):
        if not self._tasks:
            print("No tasks available.")
        else:
            for task in self._tasks:
                print(task)

    def complete_task(self, task_id):
        for task in self._tasks:
            if task.id == task_id:
                task.completed = True
                self.save_tasks()
                print(f"Task completed: {task}")
                return task
        print(f"Task with ID {task_id} not found.")

    def eliminate_task(self, task_id):
        for task in self._tasks:
            if task.id == task_id:
                self._tasks.remove(task)
                self.save_tasks()
                print(f"Task eliminated: {task}")
                return task
        print(f"Task with ID {task_id} not found.")

    def load_tasks(self):
         try:
             with open(self.filename, "r") as file  :
                 data = json.load(file)
                 self._tasks = [Task(item['id'], item['description'], item['completed']) for item in data]
                 if self._tasks:
                     self.next_id = max(task.id for task in self._tasks) + 1
                 else:
                     self.next_id = 1
                        
         except FileNotFoundError:
             self._tasks = []
             self.next_id = 1

    def save_tasks(self):
         with open(self.filename, "w") as f:
             json.dump([{'id': task.id, 'description': task.description, 'completed': task.completed, } for task in self._tasks], f, indent=4)   