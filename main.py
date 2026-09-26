from task_manager import TaskManager


def print_menu():
    print("\n --- Smart task manager --- ")
    print("1 - Add task")
    print("2 - List tasks")
    print("3 - Complete task")
    print("4 - Delete task")
    print("5 - Exit")


def main():

    manager = TaskManager()

    while True:
        print_menu()

        choice = input("Choose an option: ")
        match choice:
            case "1":
                description = input("Enter task description: ")
                manager.add_task(description)
            case "2":
                manager.list_tasks()
            case "3":
                task_id = int(input("Enter task ID to complete: "))
                manager.complete_task(task_id)
            case "4":
                task_id = int(input("Enter task ID to delete: "))
                manager.eliminate_task(task_id)
            case "5":
                print("Exiting...")
                break
            case _:
                print("Invalid option. Please try again.")

if __name__ == "__main__":
    main()
