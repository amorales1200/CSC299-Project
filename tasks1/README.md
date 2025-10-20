This is a prototype command-line application (CLI) for managing tasks. It allows users to store, list, and search for tasks, with all data persisted in a local JSON file, tasks.json.
Python 3: The application is written in Python and requires a Python 3 environment.
File Structure: This tasks.py file must be run from within its directory (tasks1/).
How to run it: 
Navigate to the tasks1 directory in your terminal to execute commands:
cd csc299-project/tasks1
Add a Task (Create)
Use the add command followed by the task description:
python tasks.py add "Design the database schema"
python tasks.py add Review pull request
List All Tasks (Read)
Use the list command to see all current tasks and their status:
python tasks.py list
Search for a Task (Read)
Use the search command followed by a keyword. The search is case-insensitive:
python tasks.py search design