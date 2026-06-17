#!/usr/bin/env python3
# main.py - Test-compatible version

import sys
import os

# Try to import from task_manager package
try:
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
except ImportError:
    # Fallback - try direct import if package structure is different
    try:
        from task_utils import (
            add_task,
            mark_task_as_complete,
            view_pending_tasks,
            view_all_tasks,
            update_task_progress,
            calculate_progress,
            remove_task
        )
        from validation import validate_menu_choice
    except ImportError:
        print("Error: Cannot find required modules!")
        print("Make sure task_manager folder or module files exist.")
        sys.exit(1)


def get_input(prompt="", default=""):
    """
    Safely get input from user - handles EOF gracefully.
    """
    try:
        if prompt:
            return input(prompt)
        return input()
    except EOFError:
        return default
    except KeyboardInterrupt:
        return default


def display_menu():
    """Display the main menu options."""
    print("\n" + "=" * 60)
    print("🎯 TASK MANAGEMENT SYSTEM".center(60))
    print("=" * 60)
    print("1. ➕ ADD NEW TASK")
    print("2. ✅ MARK TASK AS COMPLETE")
    print("3. 📈 UPDATE TASK PROGRESS")
    print("4. 📋 VIEW PENDING TASKS")
    print("5. 👁️ VIEW ALL TASKS")
    print("6. 📊 VIEW PROGRESS & STATISTICS")
    print("7. 🗑️ REMOVE TASK")
    print("8. 🚪 EXIT")
    print("=" * 60)


def add_task_interface(tasks):
    """Interface for adding a new task."""
    print("\n" + "─" * 50)
    print("📝 ADD NEW TASK")
    print("─" * 50)
    
    # Get task title - handle EOF properly
    title = get_input("📌 Task title (required): ").strip()
    if not title:
        print("❌ Title cannot be empty! Using default title.")
        title = "Untitled Task"
    
    # Get description (optional)
    description = get_input("📝 Description (optional): ").strip()
    
    # Get due date (optional)
    due_date = get_input("📅 Due date (YYYY-MM-DD) or press Enter to skip: ").strip()
    
    # Get priority
    priority = get_input("🎯 Priority (H/M/L): ").strip()
    
    # Add the task
    tasks, success, message = add_task(tasks, title, description, due_date, priority)
    print(f"\n{message}")
    
    return tasks


def mark_complete_interface(tasks):
    """Interface for marking a task as complete."""
    if not tasks:
        print("\n❌ No tasks available!")
        return tasks
    
    print("\n" + "─" * 50)
    print("✅ MARK TASK AS COMPLETE")
    print("─" * 50)
    
    view_pending_tasks(tasks)
    
    task_num = get_input("\n📌 Enter task number: ").strip()
    
    if not task_num:
        print("❌ No task number provided.")
        return tasks
    
    tasks, success, message = mark_task_as_complete(tasks, task_num)
    print(f"\n{message}")
    
    return tasks


def update_progress_interface(tasks):
    """Interface for updating task progress."""
    if not tasks:
        print("\n❌ No tasks available!")
        return tasks
    
    print("\n" + "─" * 50)
    print("📈 UPDATE TASK PROGRESS")
    print("─" * 50)
    
    view_all_tasks(tasks)
    
    task_num = get_input("\n📌 Enter task number: ").strip()
    
    if not task_num:
        print("❌ No task number provided.")
        return tasks
    
    progress_str = get_input("📊 Enter progress (0-100): ").strip()
    
    try:
        progress = int(progress_str) if progress_str else 0
        tasks, success, message = update_task_progress(tasks, task_num, progress)
        print(f"\n{message}")
    except ValueError:
        print("❌ Invalid progress value! Using 0.")
        tasks, success, message = update_task_progress(tasks, task_num, 0)
        print(f"\n{message}")
    
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
        print("\n❌ No tasks available!")
        return tasks
    
    print("\n" + "─" * 50)
    print("🗑️ REMOVE TASK")
    print("─" * 50)
    
    view_all_tasks(tasks)
    
    task_num = get_input("\n📌 Enter task number: ").strip()
    
    if not task_num:
        print("❌ No task number provided.")
        return tasks
    
    confirm = get_input("⚠️ Confirm delete? (y/n): ").lower()
    
    if confirm in ['y', 'yes']:
        tasks, success, message = remove_task(tasks, task_num)
        print(f"\n{message}")
    else:
        print("\n❌ Deletion cancelled")
    
    return tasks


def main():
    """Main program loop."""
    tasks = []
    
    # Don't show welcome message in test mode
    if not os.environ.get('TEST_MODE'):
        print("\n" + "🎯" * 30)
        print("WELCOME TO THE TASK MANAGEMENT SYSTEM!")
        print("🎯" * 30)
        print("\nManage your tasks efficiently, track progress, and stay organized!\n")
    
    while True:
        try:
            display_menu()
            choice = get_input("🔹 Enter your choice (1-8): ").strip()
            
            if not choice:
                if not os.environ.get('TEST_MODE'):
                    print("❌ Please enter a choice.")
                continue
            
            # Validate menu choice
            is_valid, validated_choice, message = validate_menu_choice(choice, 8)
            
            if not is_valid:
                print(f"\n❌ {message}")
                if not os.environ.get('TEST_MODE'):
                    get_input("\n⏎ Press Enter to continue...")
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
                print("\n👋 Thank you for using Task Management System!")
                if tasks and not os.environ.get('TEST_MODE'):
                    print("\n📊 Final Progress Summary:")
                    calculate_progress(tasks)
                print("\nGoodbye!")
                sys.exit(0)
            
            # Pause after each operation (except exit)
            if validated_choice != 8 and not os.environ.get('TEST_MODE'):
                get_input("\n⏎ Press Enter to continue...")
        
        except EOFError:
            # Handle test mode gracefully
            if os.environ.get('TEST_MODE'):
                break
            else:
                raise
        
        except KeyboardInterrupt:
            print("\n\n👋 Goodbye!")
            sys.exit(0)


if __name__ == "__main__":
    try:
        main()
    except EOFError:
        # EOF is expected in test mode
        pass
    except KeyboardInterrupt:
        print("\n\n👋 Goodbye!")
        sys.exit(0)
    except Exception as e:
        print(f"❌ An unexpected error occurred: {e}")
        sys.exit(1)