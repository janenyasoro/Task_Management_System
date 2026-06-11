# task_manager/task_utils.py
# Task management functions

from datetime import datetime
from typing import List, Dict, Tuple, Optional


def create_progress_bar(percentage: int, width: int = 20) -> str:
    """
    Create a visual progress bar.
    
    Args:
        percentage: Progress percentage (0-100)
        width: Width of the progress bar in characters
    
    Returns:
        String representation of a progress bar
    """
    filled = int(width * percentage / 100)
    empty = width - filled
    return "█" * filled + "░" * empty


def get_priority_icon(priority: str) -> str:
    """
    Get emoji icon for priority level.
    
    Args:
        priority: Priority level (High, Medium, Low)
    
    Returns:
        Emoji string
    """
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
    
    Args:
        tasks: List of task dictionaries
        title: Task title (required)
        description: Task description (optional)
        due_date: Due date (optional)
        priority: Priority level (High, Medium, Low)
    
    Returns:
        Tuple of (updated_tasks, success, message)
    """
    # Validate title
    if not title or title.strip() == "":
        return tasks, False, "❌ Task title cannot be empty!"
    
    title = title.strip()
    
    # Validate and normalize priority
    from task_manager.validation import validate_priority
    is_valid, validated_priority, _ = validate_priority(priority)
    if not is_valid:
        validated_priority = "Medium"
    
    # Generate new ID
    if tasks:
        new_id = max(task.get("id", 0) for task in tasks) + 1
    else:
        new_id = 1
    
    # Create task dictionary
    task = {
        "id": new_id,
        "title": title,
        "description": description.strip() if description else "",
        "due_date": due_date if due_date else "No due date",
        "priority": validated_priority,
        "completed": False,
        "progress": 0,
        "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "completed_at": None
    }
    
    tasks.append(task)
    return tasks, True, f"✅ Task '{title}' added successfully! (ID: {new_id})"


def mark_task_as_complete(tasks: List[Dict], task_identifier: str) -> Tuple[List[Dict], bool, str]:
    """
    Mark a task as complete (100% progress).
    
    Args:
        tasks: List of task dictionaries
        task_identifier: Task number (1-based as shown to user)
    
    Returns:
        Tuple of (updated_tasks, success, message)
    """
    if not tasks:
        return tasks, False, "❌ No tasks available!"
    
    from task_manager.validation import validate_task_number
    is_valid, task_index, message = validate_task_number(task_identifier, len(tasks))
    
    if not is_valid:
        return tasks, False, message
    
    if tasks[task_index]["completed"]:
        return tasks, False, f"⚠️ Task '{tasks[task_index]['title']}' is already complete!"
    
    tasks[task_index]["completed"] = True
    tasks[task_index]["progress"] = 100
    tasks[task_index]["completed_at"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    return tasks, True, f"✅ Task '{tasks[task_index]['title']}' marked as complete! Great job!"


def update_task_progress(tasks: List[Dict], task_identifier: str, progress: int) -> Tuple[List[Dict], bool, str]:
    """
    Update the progress percentage of a task.
    
    Args:
        tasks: List of task dictionaries
        task_identifier: Task number (1-based as shown to user)
        progress: Progress percentage (0-100)
    
    Returns:
        Tuple of (updated_tasks, success, message)
    """
    if not tasks:
        return tasks, False, "❌ No tasks available!"
    
    from task_manager.validation import validate_task_number, validate_progress
    is_valid, task_index, message = validate_task_number(task_identifier, len(tasks))
    
    if not is_valid:
        return tasks, False, message
    
    is_valid, progress_value, message = validate_progress(str(progress))
    
    if not is_valid:
        return tasks, False, message
    
    tasks[task_index]["progress"] = progress_value
    
    if progress_value == 100:
        tasks[task_index]["completed"] = True
        tasks[task_index]["completed_at"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        return tasks, True, f"🎉 Task '{tasks[task_index]['title']}' completed! (100%)"
    else:
        tasks[task_index]["completed"] = False
        tasks[task_index]["completed_at"] = None
        return tasks, True, f"📈 Task '{tasks[task_index]['title']}' progress updated to {progress_value}%"


def view_pending_tasks(tasks: List[Dict]) -> List[Dict]:
    """
    Display all pending (incomplete) tasks.
    
    Args:
        tasks: List of task dictionaries
    
    Returns:
        List of pending tasks
    """
    pending = [task for task in tasks if not task["completed"]]
    
    if not pending:
        print("\n" + "=" * 60)
        print("🎉 NO PENDING TASKS!")
        print("=" * 60)
        print("All tasks are complete! You're doing great! 🎯")
        print("=" * 60)
        return pending
    
    print("\n" + "=" * 60)
    print(f"📋 PENDING TASKS ({len(pending)} tasks remaining)")
    print("=" * 60)
    
    for i, task in enumerate(pending, 1):
        progress_bar = create_progress_bar(task["progress"])
        priority_icon = get_priority_icon(task["priority"])
        
        print(f"\n{i}. {priority_icon} [{task['id']}] {task['title'].upper()}")
        if task["description"]:
            print(f"   📝 Description: {task['description'][:80]}")
        print(f"   📊 Progress: {progress_bar} {task['progress']}%")
        print(f"   📅 Due: {task['due_date']}")
        print(f"   🏷️  Priority: {task['priority']}")
    
    print("\n" + "=" * 60)
    return pending


def view_all_tasks(tasks: List[Dict]) -> None:
    """
    Display all tasks (both complete and incomplete).
    
    Args:
        tasks: List of task dictionaries
    """
    if not tasks:
        print("\n📭 No tasks found. Add some tasks first!")
        return
    
    print("\n" + "=" * 60)
    print(f"📋 ALL TASKS ({len(tasks)} total)")
    print("=" * 60)
    
    # Sort tasks: pending first, then by priority
    def sort_key(task):
        priority_order = {"High": 0, "Medium": 1, "Low": 2}
        return (task["completed"], priority_order[task["priority"]])
    
    sorted_tasks = sorted(tasks, key=sort_key)
    
    for i, task in enumerate(sorted_tasks, 1):
        status = "✅" if task["completed"] else "⏳"
        priority_icon = get_priority_icon(task["priority"])
        progress_bar = create_progress_bar(task["progress"])
        
        print(f"\n{i}. {status} {priority_icon} [{task['id']}] {task['title'].upper()}")
        if task["description"]:
            print(f"   📝 Description: {task['description'][:80]}")
        print(f"   📊 Progress: {progress_bar} {task['progress']}%")
        print(f"   📅 Due: {task['due_date']}")
        print(f"   🏷️  Priority: {task['priority']}")
        
        if task["completed"] and task["completed_at"]:
            print(f"   🎉 Completed: {task['completed_at']}")
    
    print("\n" + "=" * 60)


def calculate_progress(tasks: List[Dict]) -> Dict:
    """
    Calculate and display overall progress statistics.
    
    Args:
        tasks: List of task dictionaries
    
    Returns:
        Dictionary containing progress statistics
    """
    if not tasks:
        print("\n📭 No tasks to track. Add some tasks first!")
        return {
            "total_tasks": 0,
            "completed_tasks": 0,
            "pending_tasks": 0,
            "overall_progress": 0.0
        }
    
    total_tasks = len(tasks)
    completed_tasks = sum(1 for task in tasks if task["completed"])
    total_progress = sum(task["progress"] for task in tasks) / total_tasks
    
    # Priority breakdown
    priority_stats = {
        "High": {"total": 0, "completed": 0},
        "Medium": {"total": 0, "completed": 0},
        "Low": {"total": 0, "completed": 0}
    }
    
    for task in tasks:
        priority = task["priority"]
        priority_stats[priority]["total"] += 1
        if task["completed"]:
            priority_stats[priority]["completed"] += 1
    
    # Count overdue tasks
    overdue_tasks = 0
    today = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
    
    for task in tasks:
        if not task["completed"] and task["due_date"] != "No due date":
            try:
                due = datetime.strptime(task["due_date"], "%Y-%m-%d")
                if due < today:
                    overdue_tasks += 1
            except:
                pass
    
    # Display report
    print("\n" + "=" * 60)
    print("📊 PROGRESS REPORT")
    print("=" * 60)
    
    print(f"\n📌 OVERALL STATISTICS:")
    print(f"   • Total Tasks: {total_tasks}")
    print(f"   • Completed: {completed_tasks} ({completed_tasks/total_tasks*100:.1f}%)")
    print(f"   • Pending: {total_tasks - completed_tasks}")
    print(f"   • Overdue: {overdue_tasks}")
    
    print(f"\n📈 OVERALL PROGRESS: {total_progress:.1f}%")
    progress_bar = create_progress_bar(int(total_progress), width=40)
    print(f"   {progress_bar}")
    
    print(f"\n⚠️ BREAKDOWN BY PRIORITY:")
    for priority, stats in priority_stats.items():
        if stats["total"] > 0:
            pct = (stats["completed"] / stats["total"]) * 100
            icon = {"High": "🔴", "Medium": "🟡", "Low": "🟢"}[priority]
            print(f"   {icon} {priority}: {stats['completed']}/{stats['total']} completed ({pct:.1f}%)")
    
    # Recent completions (last 7 days)
    recent_completions = 0
    for task in tasks:
        if task["completed"] and task["completed_at"]:
            try:
                completed_date = datetime.strptime(task["completed_at"], "%Y-%m-%d %H:%M:%S")
                days_ago = (datetime.now() - completed_date).days
                if days_ago <= 7:
                    recent_completions += 1
            except:
                pass
    
    if recent_completions > 0:
        print(f"\n🏆 RECENT ACHIEVEMENTS:")
        print(f"   • Completed {recent_completions} task(s) in the last 7 days!")
    
    print("\n" + "=" * 60)
    
    return {
        "total_tasks": total_tasks,
        "completed_tasks": completed_tasks,
        "pending_tasks": total_tasks - completed_tasks,
        "overall_progress": total_progress,
        "overdue_tasks": overdue_tasks,
        "recent_completions": recent_completions
    }


def remove_task(tasks: List[Dict], task_identifier: str) -> Tuple[List[Dict], bool, str]:
    """
    Remove a task from the list.
    
    Args:
        tasks: List of task dictionaries
        task_identifier: Task number (1-based as shown to user)
    
    Returns:
        Tuple of (updated_tasks, success, message)
    """
    if not tasks:
        return tasks, False, "❌ No tasks available to remove!"
    
    from task_manager.validation import validate_task_number
    is_valid, task_index, message = validate_task_number(task_identifier, len(tasks))
    
    if not is_valid:
        return tasks, False, message
    
    removed_task = tasks.pop(task_index)
    return tasks, True, f"🗑️ Task '{removed_task['title']}' removed successfully!"