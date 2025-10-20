

import json
import os
import sys

# --- Configuration ---
# The file where tasks will be stored
DATA_FILE = 'tasks.json'



def load_tasks():
    """Loads tasks from the JSON file. Returns an empty list if the file doesn't exist."""
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
    """Saves the current list of tasks back to the JSON file."""
    try:
        with open(DATA_FILE, 'w') as f:
            json.dump(tasks, f, indent=4)
    except Exception as e:
        print(f"An error occurred while saving tasks: {e}")

def get_next_id(tasks):
    """Generates a unique ID for a new task."""
    if not tasks:
        return 1
    return max(task['id'] for task in tasks) + 1



def add_task(description):
    """Adds a new task to the list."""
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
    """Lists all stored tasks."""
    tasks = load_tasks()
    if not tasks:
        print("No tasks found.")
        return

    print("\n--- Current Tasks ---")
    for task in tasks:
        status = "[DONE]" if task['done'] else "[TODO]"
        print(f"ID: {task['id']} {status} - {task['description']}")
    print("---------------------\n")

def search_tasks(keyword):
    """Searches tasks by keyword in their description."""
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
        print(f"ID: {task['id']} {status} - {task['description']}")
    print("--------------------------------------\n")

# --- Command-Line Interface (CLI) Handler ---

def display_help():
    """Displays the usage instructions."""
    print("Usage: python tasks.py <command> [arguments]")
    print("\nCommands:")
    print("  add <description> - Adds a new task with the given description.")
    print("  list              - Lists all stored tasks.")
    print("  search <keyword>  - Searches tasks for a specific keyword.")
    print("  help              - Displays this help message.")
    print("\nExample:")
    print("  python tasks.py add 'Finish the CLI project'")

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
        # Join all arguments after the command to allow for multi-word descriptions
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
    elif command == 'help':
        display_help()
    else:
        print(f"Error: Unknown command '{command}'.")
        display_help()

if __name__ == "__main__":
    main()