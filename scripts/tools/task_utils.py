import os
import json
import shutil

def get_task(task_id: int, base_path: str):
    """Loads a task from its JSON file."""
    task_file = os.path.join(base_path, str(task_id), 'task.json')
    if os.path.exists(task_file):
        with open(task_file, 'r', encoding='utf-8') as f:
            return json.load(f)
    return None

def get_all_tasks(base_path: str):
    """Loads all tasks from the tasks directory, sorted by ID."""
    tasks = []
    if not os.path.exists(base_path):
        return tasks
    for task_dir in sorted(os.listdir(base_path), key=int):
        task_path = os.path.join(base_path, task_dir)
        if os.path.isdir(task_path):
            task_file = os.path.join(task_path, 'task.json')
            if os.path.exists(task_file):
                with open(task_file, 'r', encoding='utf-8') as f:
                    try:
                        task_data = json.load(f)
                        if task_data.get('id') == int(task_dir):
                            tasks.append(task_data)
                    except (json.JSONDecodeError, ValueError):
                        continue
    return tasks

def move_task_logic(task_id_to_move: int, new_index_1_based: int, base_path: str):
    """
    Moves a task to a new position, re-numbering all tasks and updating dependencies.
    """
    all_tasks_original_order = get_all_tasks(base_path)
    if not all_tasks_original_order:
        return {"ok": False, "error": "No tasks found."}

    task_to_move = None
    original_index = -1
    for i, task in enumerate(all_tasks_original_order):
        if task['id'] == task_id_to_move:
            task_to_move = task
            original_index = i
            break
    
    if task_to_move is None:
        return {"ok": False, "error": f"Task with id {task_id_to_move} not found."}

    tasks_new_order = list(all_tasks_original_order)
    tasks_new_order.pop(original_index)
    tasks_new_order.insert(new_index_1_based - 1, task_to_move)

    old_to_new_id_map = {}
    new_id_to_old_id_map = {}
    for new_id, task_in_new_order in enumerate(tasks_new_order, 1):
        old_id = task_in_new_order['id']
        old_to_new_id_map[old_id] = new_id
        new_id_to_old_id_map[new_id] = old_id

    updated_tasks = []
    for task_data in tasks_new_order:
        old_id = task_data['id']
        new_id = old_to_new_id_map[old_id]
        task_data['id'] = new_id
        for feature in task_data.get('features', []):
            parts = feature['id'].split('.')
            feature['id'] = f"{new_id}.{parts[1]}"
            if 'dependencies' in feature and feature['dependencies']:
                new_deps = []
                for dep in feature['dependencies']:
                    dep_task_id_str, dep_feature_num = dep.split('.')
                    dep_task_id = int(dep_task_id_str)
                    new_dep_task_id = old_to_new_id_map.get(dep_task_id, dep_task_id)
                    new_deps.append(f"{new_dep_task_id}.{dep_feature_num}")
                feature['dependencies'] = new_deps
        updated_tasks.append(task_data)

    temp_dirs = {}
    try:
        for old_id in old_to_new_id_map.keys():
            old_dir = os.path.join(base_path, str(old_id))
            temp_dir = os.path.join(base_path, f"{old_id}_tmp")
            if os.path.exists(old_dir):
                shutil.move(old_dir, temp_dir)
                temp_dirs[old_id] = temp_dir

        for new_id, old_id in new_id_to_old_id_map.items():
            temp_dir = temp_dirs[old_id]
            new_dir = os.path.join(base_path, str(new_id))
            shutil.move(temp_dir, new_dir)
            
            task_to_write = None
            for t in updated_tasks:
                if t['id'] == new_id:
                    task_to_write = t
                    break
            
            if task_to_write:
                with open(os.path.join(new_dir, 'task.json'), 'w', encoding='utf-8') as f:
                    json.dump(task_to_write, f, indent=2)

    except Exception as e:
        for temp_dir in temp_dirs.values():
            if os.path.exists(temp_dir):
                original_id = os.path.basename(temp_dir).replace('_tmp','')
                original_path = os.path.join(base_path, original_id)
                shutil.move(temp_dir, original_path)
        return {"ok": False, "error": f"An error occurred during file operations: {e}"}

    return {"ok": True, "message": f"Task {task_id_to_move} moved to position {new_index_1_based}. Tasks renumbered."}
