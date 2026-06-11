import sys

# Import from task_manager package
from task_manager import (
    add_task,
    mark_task_as_complete,
    view_pending_tasks,
    view_all_tasks,
    update_task_progress,
    calculate_progress,
    remove_task
)
from task_manager.validation import validate_menu_choice


def display_menu():
    """Display the main menu options."""
    print("\n" + "=" * 60)
    print("🎯 TASK MANAGEMENT SYSTEM".center(60))
    print("=" * 60)
    print("""
   ┌────────────────────────────────────────────────────────┐
   │                    MAIN MENU                           │
   ├────────────────────────────────────────────────────────┤
   │  1. ➕ ADD NEW TASK                                     │
   │  2. ✅ MARK TASK AS COMPLETE                            │
   │  3. 📈 UPDATE TASK PROGRESS                             │
   │  4. 📋 VIEW PENDING TASKS                               │
   │  5. 👁️ VIEW ALL TASKS                                  │
   │  6. 📊 VIEW PROGRESS & STATISTICS                       │
   │  7. 🗑️ REMOVE TASK                                     │
   │  8. 🚪 EXIT                                             │
   └────────────────────────────────────────────────────────┘
""")
    print("=" * 60)


def add_task_interface(tasks):
    """Interface for adding a new task."""
    print("\n" + "─" * 50)
    print("📝 ADD NEW TASK")
    print("─" * 50)
    
    # Get task title
    while True:
        title = input("📌 Task title (required): ").strip()
        if title:
            break
        print("   ❌ Title cannot be empty! Please enter a title.")
    
    # Get description (optional)
    description = input("📝 Description (optional): ").strip()
    
    # Get due date (optional)
    due_date = input("📅 Due date (YYYY-MM-DD) or press Enter to skip: ").strip()
    
    # Get priority
    print("\n🎯 Priority options:")
    print("   H = High 🔴")
    print("   M = Medium 🟡")
    print("   L = Low 🟢")
    priority = input("Enter priority (H/M/L): ").strip()
    
    # Add the task
    tasks, success, message = add_task(tasks, title, description, due_date, priority)
    print(f"\n{message}")
    
    return tasks


def mark_complete_interface(tasks):
    """Interface for marking a task as complete."""
    if not tasks:
        print("\n❌ No tasks available! Please add some tasks first.")
        return tasks
    
    print("\n" + "─" * 50)
    print("✅ MARK TASK AS COMPLETE")
    print("─" * 50)
    
    # Show pending tasks only
    pending = view_pending_tasks(tasks)
    
    if not pending:
        return tasks
    
    task_num = input("\n📌 Enter task number to mark as complete: ").strip()
    
    if not task_num:
        print("❌ Operation cancelled")
        return tasks
    
    tasks, success, message = mark_task_as_complete(tasks, task_num)
    print(f"\n{message}")
    
    return tasks


def update_progress_interface(tasks):
    """Interface for updating task progress."""
    if not tasks:
        print("\n❌ No tasks available! Please add some tasks first.")
        return tasks
    
    print("\n" + "─" * 50)
    print("📈 UPDATE TASK PROGRESS")
    print("─" * 50)
    
    # Show all tasks
    view_all_tasks(tasks)
    
    task_num = input("\n📌 Enter task number to update: ").strip()
    
    if not task_num:
        print("❌ Operation cancelled")
        return tasks
    
    try:
        progress = int(input("📊 Enter progress percentage (0-100): ").strip())
        tasks, success, message = update_task_progress(tasks, task_num, progress)
        print(f"\n{message}")
    except ValueError:
        print("❌ Invalid input! Please enter a number between 0 and 100.")
    
    return tasks


def view_pending_interface(tasks):
    """Interface for viewing pending tasks."""
    print("\n" + "─" * 50)
    print("📋 PENDING TASKS")
    print("─" * 50)
    view_pending_tasks(tasks)


def view_all_interface(tasks):
    """Interface for viewing all tasks."""
    print("\n" + "─" * 50)
    print("👁️ ALL TASKS")
    print("─" * 50)
    view_all_tasks(tasks)


def progress_interface(tasks):
    """Interface for viewing progress statistics."""
    print("\n" + "─" * 50)
    print("📊 PROGRESS & STATISTICS")
    print("─" * 50)
    calculate_progress(tasks)


def remove_task_interface(tasks):
    """Interface for removing a task."""
    if not tasks:
        print("\n❌ No tasks available! Please add some tasks first.")
        return tasks
    
    print("\n" + "─" * 50)
    print("🗑️ REMOVE TASK")
    print("─" * 50)
    
    # Show all tasks
    view_all_tasks(tasks)
    
    task_num = input("\n📌 Enter task number to remove: ").strip()
    
    if not task_num:
        print("❌ Operation cancelled")
        return tasks
    
    # Confirm deletion
    confirm = input(f"⚠️ Are you sure you want to delete this task? (y/n): ").lower()
    
    if confirm == 'y' or confirm == 'yes':
        tasks, success, message = remove_task(tasks, task_num)
        print(f"\n{message}")
    else:
        print("\n❌ Deletion cancelled")
    
    return tasks


def main():
    """Main program loop."""
    tasks = []
    
    print("\n" + "🎯" * 30)
    print("WELCOME TO THE TASK MANAGEMENT SYSTEM!")
    print("🎯" * 30)
    print("\nManage your tasks efficiently, track progress, and stay organized!\n")
    
    while True:
        display_menu()
        
        choice = input("🔹 Enter your choice (1-8): ").strip()
        
        # Validate menu choice
        is_valid, validated_choice, message = validate_menu_choice(choice, 8)
        
        if not is_valid:
            print(f"\n❌ {message}")
            input("\n⏎ Press Enter to continue...")
            continue
        
        # Process user choice
        if validated_choice == 1:
            tasks = add_task_interface(tasks)
        
        elif validated_choice == 2:
            tasks = mark_complete_interface(tasks)
        
        elif validated_choice == 3:
            tasks = update_progress_interface(tasks)
        
        elif validated_choice == 4:
            view_pending_interface(tasks)
        
        elif validated_choice == 5:
            view_all_interface(tasks)
        
        elif validated_choice == 6:
            progress_interface(tasks)
        
        elif validated_choice == 7:
            tasks = remove_task_interface(tasks)
        
        elif validated_choice == 8:
            # Exit the program
            print("\n" + "=" * 60)
            print("👋 THANK YOU FOR USING TASK MANAGEMENT SYSTEM!")
            print("=" * 60)
            
            if tasks:
                print("\n📊 Final Progress Summary:")
                calculate_progress(tasks)
            
            print("\n✨ Stay productive and keep achieving your goals! ✨")
            print("=" * 60 + "\n")
            sys.exit(0)
        
        # Pause before showing menu again (except for exit)
        if validated_choice != 8:
            input("\n⏎ Press Enter to continue...")


# Entry point of the application
if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 Goodbye! Thanks for using Task Management System!\n")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ An unexpected error occurred: {e}")
        print("Please restart the application.")
        sys.exit(1)