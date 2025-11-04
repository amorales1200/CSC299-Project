# File: tasks3/src/tasks3/__init__.py

import json
import os
import sys

# --- REQUIRED FUNCTION ---
def inc(n: int) -> int:
    return n + 1
# -------------------------

DATA_FILE = 'tasks.json'


# --- CORE TASK MANAGEMENT FUNCTIONS ---

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
    return new_task

def list_tasks():
    return load_tasks()

def mark_done(task_id_str):
    tasks = load_tasks()
    task = find_task_by_id(tasks, task_id_str)

    if task and not task['done']:
        task['done'] = True
        save_tasks(tasks)
        return True
    return False

def delete_task(task_id_str):
    tasks = load_tasks()
    try:
        task_id = int(task_id_str)
    except ValueError:
        return False

    tasks_before_delete = len(tasks)
    tasks_list = [task for task in tasks if task['id'] != task_id]
    
    if len(tasks_list) < tasks_before_delete:
        save_tasks(tasks_list)
        return True
    return False

# --- MAIN ENTRY POINT ---

def display_help():
    print("Usage: uv run tasks3 <command> [arguments]...")
    print("\nCommands:")
    print("  add <description>     - Adds a new task.")
    print("  list                  - Lists all stored tasks.")
    # Add more help content here

def main():
    # This function is called by `uv run tasks3`
    if len(sys.argv) < 2:
        display_help()
        return

    command = sys.argv[1].lower()

    if command == 'add':
        if len(sys.argv) < 3:
            print("Error: The 'add' command requires a description.")
            return
        description = " ".join(sys.argv[2:])
        add_task(description)
        print(f"Task added: '{description}'")

    elif command == 'list':
        tasks = list_tasks()
        if not tasks:
            print("No tasks found.")
            return
        print("\n--- Current Tasks ---")
        for task in tasks:
            status = "[DONE]" if task['done'] else "[TODO]"
            print(f"ID: {task['id']:<4} {status} - {task['description']}")
        print("---------------------\n")
    
    elif command == 'done':
        if len(sys.argv) < 3:
            print("Error: The 'done' command requires a task ID.")
            return
        task_id_str = sys.argv[2]
        if mark_done(task_id_str):
            print(f"Task #{task_id_str} marked as DONE.")
        else:
            print(f"Error: Could not mark Task #{task_id_str} as done (not found or invalid ID).")

  
    
if __name__ == "__main__":
    main()