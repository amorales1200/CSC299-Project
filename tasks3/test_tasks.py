
import os
import pytest
import json
import tasks3 


@pytest.fixture(autouse=True)
def clean_data_file(tmp_path):
    """Fixture to ensure a clean, temporary tasks.json for every test."""
    
    original_data_file = tasks3.DATA_FILE
    
   
    temp_data_file = tmp_path / "tasks.json"
    tasks3.DATA_FILE = str(temp_data_file)
    
 
    with open(tasks3.DATA_FILE, 'w') as f:
        json.dump([], f)
    
    yield 
    
    tasks3.DATA_FILE = original_data_file


from tasks3 import inc, load_tasks, get_next_id, add_task, mark_done 


def test_inc():
    assert inc(5) == 6


def test_get_next_id():
    tasks = [{'id': 5, 'description': 'a', 'done': False},
             {'id': 1, 'description': 'b', 'done': False}]
    assert get_next_id(tasks) == 6


def test_add_task_success(tmp_path):
    description = "Submit assignment"
    add_task(description)
    
    tasks = load_tasks()
    assert len(tasks) == 1

def test_mark_done_success(tmp_path):
    added_task = add_task("Task to complete")
    task_id = str(added_task['id'])
    
    mark_done(task_id)
    
    tasks = load_tasks()
    assert tasks[0]['done'] == True