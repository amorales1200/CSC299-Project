import json
import os
import sys


DATA_FILE = 'tasks.json'


def load_tasks():
    if not os.path.exists(DATA_FILE):
        return []
    try:
        with open(DATA_FILE, 'r') as f:
            return json.load(f)
    except json.JSONDecodeError:
        print(f"Error: Could not decode JSON from {DATA_FILE}. Starting with an empty list.")
        return []
    except Exception as e:
        print(f"An error occurred while loading tasks: {e}")
        return []

def save_tasks(tasks):
    try:
        with open(DATA_FILE, 'w') as f:
            json.dump(tasks, f, indent=4)
    except Exception as e:
        print(f"An error occurred while saving tasks: {e}")

def get_next_id(tasks):
    if not tasks:
        return 1
    return max(task['id'] for task in tasks) + 1

def find_task_by_id(tasks, task_id_str):
    try:
        task_id = int(task_id_str)
    except ValueError:
        return None 
        
    for task in tasks:
        if task['id'] == task_id:
            return task
    return None



def add_task(description):
    tasks = load_tasks()
    new_task = {
        'id': get_next_id(tasks),
        'description': description,
        'done': False
    }
    tasks.append(new_task)
    save_tasks(tasks)
    print(f"Task #{new_task['id']} added: '{description}'")

def list_tasks():
    """Lists all stored tasks (Read)."""
    tasks = load_tasks()
    if not tasks:
        print("No tasks found.")
        return

    print("\n--- Current Tasks ---")
    for task in tasks:
        status = "[DONE]" if task['done'] else "[TODO]"
        print(f"ID: {task['id']:<4} {status} - {task['description']}")
    print("---------------------\n")

def search_tasks(keyword):
    """Searches tasks by keyword in their description (Read)."""
    tasks = load_tasks()
    results = [
        task for task in tasks
        if keyword.lower() in task['description'].lower()
    ]

    if not results:
        print(f"No tasks found containing '{keyword}'.")
        return

    print(f"\n--- Search Results for '{keyword}' ---")
    for task in results:
        status = "[DONE]" if task['done'] else "[TODO]"
        print(f"ID: {task['id']:<4} {status} - {task['description']}")
    print("--------------------------------------\n")

def mark_done(task_id_str):
    tasks = load_tasks()
    task = find_task_by_id(tasks, task_id_str)

    if task:
        if task['done']:
            print(f"Task #{task_id_str} is already marked as DONE.")
        else:
            task['done'] = True
            save_tasks(tasks)
            print(f"Task #{task_id_str} marked as DONE: '{task['description']}'")
    else:
        print(f"Error: Task with ID {task_id_str} not found.")

def delete_task(task_id_str):
    tasks = load_tasks()
    
    try:
        task_id = int(task_id_str)
    except ValueError:
        print(f"Error: Invalid task ID '{task_id_str}'. ID must be an integer.")
        return

    tasks_before_delete = len(tasks)
    tasks = [task for task in tasks if task['id'] != task_id]
    
    if len(tasks) < tasks_before_delete:
        save_tasks(tasks)
        print(f"Task #{task_id_str} deleted.")
    else:
        print(f"Error: Task with ID {task_id_str} not found.")


def display_help():
    print("Usage: python tasks.py <command> [arguments]")
    print("\nCommands:")
    print("  add <description>     - Adds a new task with the given description.")
    print("  list                  - Lists all stored tasks.")
    print("  search <keyword>      - Searches tasks for a specific keyword.")
    print("  done <id>             - Marks the task with the given ID as complete.")
    print("  delete <id>           - Deletes the task with the given ID.")
    print("  help                  - Displays this help message.")
    print("\nExample:")
    print("  python tasks.py add 'Finish the CLI project'")
    print("  python tasks.py done 3")

def main():
    if len(sys.argv) < 2:
        display_help()
        return

    command = sys.argv[1].lower()

    if command == 'add':
        if len(sys.argv) < 3:
            print("Error: The 'add' command requires a description.")
            display_help()
            return
        description = " ".join(sys.argv[2:])
        add_task(description)
    elif command == 'list':
        list_tasks()
    elif command == 'search':
        if len(sys.argv) < 3:
            print("Error: The 'search' command requires a keyword.")
            display_help()
            return
        keyword = sys.argv[2]
        search_tasks(keyword)
    elif command == 'done':
        if len(sys.argv) < 3:
            print("Error: The 'done' command requires a task ID.")
            display_help()
            return
        task_id_str = sys.argv[2]
        mark_done(task_id_str)
    elif command == 'delete':
        if len(sys.argv) < 3:
            print("Error: The 'delete' command requires a task ID.")
            display_help()
            return
        task_id_str = sys.argv[2]
        delete_task(task_id_str)
    elif command == 'help':
        display_help()
    else:
        print(f"Error: Unknown command '{command}'.")
        display_help()

if __name__ == "__main__":
    main()