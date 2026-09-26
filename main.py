from task_manager import TaskManager


def print_menu():
    print("\n --- Smart task manager --- ")
    print("1 - Add task")
    print("2 - Add complex task with AI")
    print("3 - List tasks")
    print("4 - Complete task")
    print("5 - Delete task")
    print("6 - Exit")


def main():

    manager = TaskManager()

    while True:
        print_menu()

        try:
            choice = int(input("Choose an option: "))
            match choice:
                case 1:
                    description = input("Enter task description: ")
                    manager.add_task(description)
                case 2:
                    description = input("Enter complex task description: ")
                    manager.add_complex_task(description)
                case 3:
                    manager.list_tasks()
                case 4:
                    task_id = int(input("Enter task ID to complete: "))
                    manager.complete_task(task_id)
                case 5:
                    task_id = int(input("Enter task ID to delete: "))
                    manager.eliminate_task(task_id)
                case 6:
                    print("Exiting...")
                    break
                case _:
                    print("Invalid option. Please try again.")
        except ValueError:
            print("Invalid input. Please enter a number.")


if __name__ == "__main__":
    main()
