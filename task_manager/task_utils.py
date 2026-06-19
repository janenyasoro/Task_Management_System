# task_manager/task_utils.py
# Task management functions

from datetime import datetime
from typing import List, Dict, Tuple, Optional


def create_progress_bar(percentage: int, width: int = 20) -> str:
    """Create a visual progress bar."""
    filled = int(width * percentage / 100)
    empty = width - filled
    return "█" * filled + "░" * empty


def get_priority_icon(priority: str) -> str:
    """Get emoji icon for priority level."""
    icons = {
        "High": "🔴",
        "Medium": "🟡",
        "Low": "🟢"
    }
    return icons.get(priority, "⚪")


def add_task(tasks: List[Dict], title: str, description: str = "", 
             due_date: str = "", priority: str = "Medium") -> Tuple[List[Dict], bool, str]:
    """
    Add a new task to the task list.
    """
    # Validate and clean title
    if not title or title.strip() == "":
        return tasks, False, "❌ Task title cannot be empty!"
    
    title = title.strip()
    
    # Normalize priority
    priority_map = {
        "H": "High", "HIGH": "High", "1": "High",
        "M": "Medium", "MEDIUM": "Medium", "2": "Medium",
        "L": "Low", "LOW": "Low", "3": "Low"
    }
    priority = priority_map.get(priority.upper(), "Medium")
    
    # Generate new ID
    new_id = max([task.get("id", 0) for task in tasks], default=0) + 1
    
    # Create task
    task = {
        "id": new_id,
        "title": title,
        "description": description.strip() if description else "",
        "due_date": due_date if due_date else "No due date",
        "priority": priority,
        "completed": False,
        "progress": 0,
        "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "completed_at": None
    }
    
    tasks.append(task)
    return tasks, True, f"✅ Task '{title}' added successfully! (ID: {new_id})"


def mark_task_as_complete(tasks: List[Dict], task_num: str) -> Tuple[List[Dict], bool, str]:
    """Mark a task as complete."""
    if not tasks:
        return tasks, False, "❌ No tasks available!"
    
    try:
        index = int(task_num) - 1
        if 0 <= index < len(tasks):
            if tasks[index]["completed"]:
                return tasks, False, f"⚠️ Task '{tasks[index]['title']}' is already complete!"
            
            tasks[index]["completed"] = True
            tasks[index]["progress"] = 100
            tasks[index]["completed_at"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            return tasks, True, f"✅ Task '{tasks[index]['title']}' marked as complete!"
        else:
            return tasks, False, "❌ Invalid task number!"
    except (ValueError, TypeError):
        return tasks, False, "❌ Please enter a valid number!"


def view_pending_tasks(tasks: List[Dict]) -> List[Dict]:
    """Display pending tasks."""
    pending = [task for task in tasks if not task["completed"]]
    
    if not pending:
        print("\n🎉 NO PENDING TASKS! All tasks are complete!")
        return pending
    
    print("\n" + "=" * 60)
    print(f"📋 PENDING TASKS ({len(pending)} tasks remaining)")
    print("=" * 60)
    
    for i, task in enumerate(pending, 1):
        progress_bar = create_progress_bar(task.get("progress", 0))
        priority_icon = get_priority_icon(task.get("priority", "Medium"))
        
        print(f"\n{i}. {priority_icon} [{task.get('id', i)}] {task.get('title', 'Untitled')}")
        if task.get("description"):
            print(f"   📝 {task['description'][:80]}")
        print(f"   📊 {progress_bar} {task.get('progress', 0)}%")
        print(f"   📅 Due: {task.get('due_date', 'No due date')}")
        print(f"   🏷️  Priority: {task.get('priority', 'Medium')}")
    
    print("\n" + "=" * 60)
    return pending


def view_all_tasks(tasks: List[Dict]) -> None:
    """Display all tasks."""
    if not tasks:
        print("\n📭 No tasks found!")
        return
    
    print("\n" + "=" * 60)
    print(f"📋 ALL TASKS ({len(tasks)} total)")
    print("=" * 60)
    
    for i, task in enumerate(tasks, 1):
        status = "✅" if task.get("completed", False) else "⏳"
        priority_icon = get_priority_icon(task.get("priority", "Medium"))
        progress_bar = create_progress_bar(task.get("progress", 0))
        
        print(f"\n{i}. {status} {priority_icon} [{task.get('id', i)}] {task.get('title', 'Untitled')}")
        if task.get("description"):
            print(f"   📝 {task['description'][:80]}")
        print(f"   📊 {progress_bar} {task.get('progress', 0)}%")
        print(f"   📅 Due: {task.get('due_date', 'No due date')}")
        print(f"   🏷️  Priority: {task.get('priority', 'Medium')}")
        
        if task.get("completed") and task.get("completed_at"):
            print(f"   🎉 Completed: {task['completed_at']}")
    
    print("\n" + "=" * 60)


def update_task_progress(tasks: List[Dict], task_num: str, progress: int) -> Tuple[List[Dict], bool, str]:
    """Update task progress."""
    if not tasks:
        return tasks, False, "❌ No tasks available!"
    
    try:
        index = int(task_num) - 1
        if 0 <= index < len(tasks):
            if 0 <= progress <= 100:
                tasks[index]["progress"] = progress
                if progress == 100:
                    tasks[index]["completed"] = True
                    tasks[index]["completed_at"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    return tasks, True, f"🎉 Task '{tasks[index]['title']}' completed! (100%)"
                else:
                    tasks[index]["completed"] = False
                    tasks[index]["completed_at"] = None
                    return tasks, True, f"📈 Task '{tasks[index]['title']}' progress updated to {progress}%"
            else:
                return tasks, False, "❌ Progress must be between 0 and 100!"
        else:
            return tasks, False, "❌ Invalid task number!"
    except (ValueError, TypeError):
        return tasks, False, "❌ Please enter valid numbers!"


def calculate_progress(tasks: List[Dict]) -> float:
    """
    Calculate overall progress percentage.
    
    Args:
        tasks: List of task dictionaries
    
    Returns:
        float: Overall progress percentage (0-100)
    """
    if not tasks:
        return 0.0
    
    # Handle tasks without 'progress' key (for testing)
    total_progress = 0
    for task in tasks:
        # If 'progress' doesn't exist, check if 'completed' exists
        if "progress" in task:
            total_progress += task["progress"]
        elif "completed" in task and task["completed"]:
            total_progress += 100
        else:
            total_progress += 0
    
    total_tasks = len(tasks)
    overall_progress = total_progress / total_tasks
    
    # Display progress (for main program)
    print(f"\n📊 Overall Progress: {overall_progress:.1f}%")
    
    return overall_progress


def remove_task(tasks: List[Dict], task_num: str) -> Tuple[List[Dict], bool, str]:
    """Remove a task."""
    if not tasks:
        return tasks, False, "❌ No tasks available!"
    
    try:
        index = int(task_num) - 1
        if 0 <= index < len(tasks):
            removed = tasks.pop(index)
            return tasks, True, f"🗑️ Task '{removed['title']}' removed!"
        else:
            return tasks, False, "❌ Invalid task number!"
    except (ValueError, TypeError):
        return tasks, False, "❌ Please enter a valid number!"