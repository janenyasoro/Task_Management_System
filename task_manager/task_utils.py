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
    """Add a new task."""
    # Validate and clean title
    if not title or title.strip() == "":
        title = "Untitled Task"
    else:
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
        progress_bar = create_progress_bar(task["progress"])
        priority_icon = get_priority_icon(task["priority"])
        
        print(f"\n{i}. {priority_icon} [{task['id']}] {task['title']}")
        if task["description"]:
            print(f"   📝 {task['description'][:80]}")
        print(f"   📊 {progress_bar} {task['progress']}%")
        print(f"   📅 Due: {task['due_date']}")
        print(f"   🏷️  Priority: {task['priority']}")
    
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
        status = "✅" if task["completed"] else "⏳"
        priority_icon = get_priority_icon(task["priority"])
        progress_bar = create_progress_bar(task["progress"])
        
        print(f"\n{i}. {status} {priority_icon} [{task['id']}] {task['title']}")
        if task["description"]:
            print(f"   📝 {task['description'][:80]}")
        print(f"   📊 {progress_bar} {task['progress']}%")
        print(f"   📅 Due: {task['due_date']}")
        print(f"   🏷️  Priority: {task['priority']}")
        
        if task["completed"] and task["completed_at"]:
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


def calculate_progress(tasks: List[Dict]) -> Dict:
    """Calculate progress statistics."""
    if not tasks:
        print("\n📭 No tasks to track!")
        return {
            "total_tasks": 0,
            "completed_tasks": 0,
            "pending_tasks": 0,
            "overall_progress": 0.0
        }
    
    total_tasks = len(tasks)
    completed_tasks = sum(1 for task in tasks if task["completed"])
    total_progress = sum(task["progress"] for task in tasks) / total_tasks
    
    print("\n" + "=" * 60)
    print("📊 PROGRESS REPORT")
    print("=" * 60)
    print(f"\n📌 Total Tasks: {total_tasks}")
    print(f"✅ Completed: {completed_tasks} ({completed_tasks/total_tasks*100:.1f}%)")
    print(f"⏳ Pending: {total_tasks - completed_tasks}")
    print(f"📈 Overall Progress: {total_progress:.1f}%")
    
    progress_bar = create_progress_bar(int(total_progress), 40)
    print(f"   {progress_bar}")
    
    # Priority breakdown
    priority_stats = {"High": {"total": 0, "completed": 0},
                     "Medium": {"total": 0, "completed": 0},
                     "Low": {"total": 0, "completed": 0}}
    
    for task in tasks:
        priority = task["priority"]
        priority_stats[priority]["total"] += 1
        if task["completed"]:
            priority_stats[priority]["completed"] += 1
    
    print(f"\n🎯 By Priority:")
    for priority, stats in priority_stats.items():
        if stats["total"] > 0:
            pct = (stats["completed"] / stats["total"]) * 100
            icon = {"High": "🔴", "Medium": "🟡", "Low": "🟢"}[priority]
            print(f"   {icon} {priority}: {stats['completed']}/{stats['total']} ({pct:.1f}%)")
    
    print("=" * 60)
    
    return {
        "total_tasks": total_tasks,
        "completed_tasks": completed_tasks,
        "pending_tasks": total_tasks - completed_tasks,
        "overall_progress": total_progress
    }


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