#!/bin/bash
# Complete setup script for Task Management System

echo "Setting up Task Management System..."

# Create directory structure
mkdir -p task_manager

# Create __init__.py if it doesn't exist
if [ ! -f "task_manager/__init__.py" ]; then
    cat > task_manager/__init__.py << 'EOF'
# task_manager/__init__.py
from task_manager.task_utils import *
from task_manager.validation import *

__all__ = [
    "add_task",
    "mark_task_as_complete",
    "view_pending_tasks",
    "view_all_tasks",
    "update_task_progress",
    "calculate_progress",
    "remove_task"
]
EOF
    echo "Created task_manager/__init__.py"
fi

# Create validation.py if it doesn't exist
if [ ! -f "task_manager/validation.py" ]; then
    echo "Creating validation.py..."
    cat > task_manager/validation.py << 'EOF'
# task_manager/validation.py
# Input validation functions

from datetime import datetime
from typing import Tuple, Optional

def validate_task_title(title: str) -> Tuple[bool, str]:
    """Validate task title."""
    if not title or title.strip() == "":
        return False, "Task title cannot be empty!"
    cleaned = title.strip()
    if len(cleaned) < 3:
        return False, "Task title must be at least 3 characters!"
    if len(cleaned) > 100:
        return False, "Task title too long! Max 100 characters."
    return True, cleaned

def validate_task_description(description: str) -> Tuple[bool, str]:
    """Validate task description."""
    if not description or description.strip() == "":
        return True, ""
    cleaned = description.strip()
    if len(cleaned) > 500:
        return False, "Description too long! Max 500 characters."
    return True, cleaned

def validate_due_date(due_date: str) -> Tuple[bool, str, Optional[str]]:
    """Validate due date."""
    if not due_date or due_date.strip() == "":
        return True, "No due date provided", None
    due_date = due_date.strip()
    formats = ["%Y-%m-%d", "%d/%m/%Y", "%m/%d/%Y", "%Y/%m/%d"]
    for fmt in formats:
        try:
            parsed = datetime.strptime(due_date, fmt)
            today = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
            if parsed < today:
                return False, "Date cannot be in the past!", None
            return True, "Valid", parsed.strftime("%Y-%m-%d")
        except ValueError:
            continue
    return False, "Invalid date format! Use YYYY-MM-DD", None

def validate_priority(priority: str) -> Tuple[bool, Optional[str], str]:
    """Validate priority."""
    valid = {"High": ["High","high","H","1"], "Medium": ["Medium","medium","M","2"], "Low": ["Low","low","L","3"]}
    if not priority or priority.strip() == "":
        return False, None, "Priority cannot be empty!"
    priority = priority.strip()
    for standard, variations in valid.items():
        if priority in variations:
            return True, standard, "Valid"
    return False, None, "Invalid priority! Use High/Medium/Low"

def validate_menu_choice(choice: str, max_choice: int) -> Tuple[bool, Optional[int], str]:
    """Validate menu choice."""
    try:
        num = int(choice)
        if 1 <= num <= max_choice:
            return True, num, "Valid"
        return False, None, f"Enter a number between 1 and {max_choice}"
    except ValueError:
        return False, None, "Invalid input!"

def validate_task_number(task_num: str, total: int) -> Tuple[bool, Optional[int], str]:
    """Validate task number."""
    if total == 0:
        return False, None, "No tasks available!"
    try:
        num = int(task_num)
        if 1 <= num <= total:
            return True, num - 1, "Valid"
        return False, None, f"Enter a number between 1 and {total}"
    except ValueError:
        return False, None, "Invalid input!"

def validate_progress(progress: str) -> Tuple[bool, Optional[int], str]:
    """Validate progress."""
    if not progress or progress.strip() == "":
        return False, None, "Progress cannot be empty!"
    try:
        num = int(progress)
        if 0 <= num <= 100:
            return True, num, "Valid"
        return False, None, "Progress must be 0-100!"
    except ValueError:
        return False, None, "Invalid input!"
EOF
    echo "Created task_manager/validation.py"
fi

# Create task_utils.py if it doesn't exist
if [ ! -f "task_manager/task_utils.py" ]; then
    echo "Creating task_utils.py..."
    cat > task_manager/task_utils.py << 'EOF'
# task_manager/task_utils.py
# Task management functions

from datetime import datetime
from typing import List, Dict, Tuple

def add_task(tasks: List[Dict], title: str, description: str = "", 
             due_date: str = "", priority: str = "Medium") -> Tuple[List[Dict], bool, str]:
    """Add a new task."""
    if not title or title.strip() == "":
        return tasks, False, "❌ Task title cannot be empty!"
    title = title.strip()
    priority_map = {"H":"High","HIGH":"High","1":"High","M":"Medium","MEDIUM":"Medium","2":"Medium","L":"Low","LOW":"Low","3":"Low"}
    priority = priority_map.get(priority.upper(), "Medium")
    new_id = max([t.get("id", 0) for t in tasks], default=0) + 1
    task = {
        "id": new_id, "title": title, "description": description.strip() if description else "",
        "due_date": due_date if due_date else "No due date", "priority": priority,
        "completed": False, "progress": 0,
        "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "completed_at": None
    }
    tasks.append(task)
    return tasks, True, f"✅ Task '{title}' added successfully!"

def calculate_progress(tasks: List[Dict]) -> float:
    """Calculate overall progress."""
    if not tasks:
        return 0.0
    total_progress = 0
    for task in tasks:
        if "progress" in task:
            total_progress += task["progress"]
        elif "completed" in task and task["completed"]:
            total_progress += 100
    return total_progress / len(tasks)

def view_pending_tasks(tasks: List[Dict]) -> List[Dict]:
    """Display pending tasks."""
    pending = [t for t in tasks if not t["completed"]]
    if not pending:
        print("\n🎉 No pending tasks!")
        return pending
    print(f"\n📋 Pending Tasks ({len(pending)}):")
    for i, task in enumerate(pending, 1):
        print(f"{i}. {task.get('title', 'Untitled')}")
    return pending

def view_all_tasks(tasks: List[Dict]) -> None:
    """Display all tasks."""
    if not tasks:
        print("\n📭 No tasks found!")
        return
    print(f"\n📋 All Tasks ({len(tasks)}):")
    for i, task in enumerate(tasks, 1):
        status = "✅" if task.get("completed", False) else "⏳"
        print(f"{i}. {status} {task.get('title', 'Untitled')}")

def mark_task_as_complete(tasks: List[Dict], task_num: str) -> Tuple[List[Dict], bool, str]:
    """Mark task as complete."""
    try:
        idx = int(task_num) - 1
        if 0 <= idx < len(tasks):
            tasks[idx]["completed"] = True
            tasks[idx]["progress"] = 100
            return tasks, True, f"✅ Task '{tasks[idx]['title']}' completed!"
        return tasks, False, "❌ Invalid task number!"
    except ValueError:
        return tasks, False, "❌ Invalid input!"

def remove_task(tasks: List[Dict], task_num: str) -> Tuple[List[Dict], bool, str]:
    """Remove a task."""
    try:
        idx = int(task_num) - 1
        if 0 <= idx < len(tasks):
            removed = tasks.pop(idx)
            return tasks, True, f"🗑️ Task '{removed['title']}' removed!"
        return tasks, False, "❌ Invalid task number!"
    except ValueError:
        return tasks, False, "❌ Invalid input!"

def update_task_progress(tasks: List[Dict], task_num: str, progress: int) -> Tuple[List[Dict], bool, str]:
    """Update task progress."""
    try:
        idx = int(task_num) - 1
        if 0 <= idx < len(tasks):
            if 0 <= progress <= 100:
                tasks[idx]["progress"] = progress
                if progress == 100:
                    tasks[idx]["completed"] = True
                return tasks, True, f"📈 Task '{tasks[idx]['title']}' at {progress}%"
            return tasks, False, "❌ Progress must be 0-100!"
        return tasks, False, "❌ Invalid task number!"
    except ValueError:
        return tasks, False, "❌ Invalid input!"
EOF
    echo "Created task_manager/task_utils.py"
fi

echo ""
echo "✅ Setup complete!"
echo "Directory structure:"
ls -la task_manager/