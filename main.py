# main.py
# Main script for the Task Management System

import sys

# Import functions from task_manager package
try:
    from task_manager.task_utils import (
        add_task,
        mark_task_as_complete,
        view_pending_tasks,
        calculate_progress,
        view_all_tasks,
        update_task_progress,
        remove_task
    )
    from task_manager.validation import validate_menu_choice
except ImportError:
    # Fallback if task_manager package doesn't exist
    print("Error: Cannot find task_manager package!")
    print("Make sure the task_manager folder is in the same directory.")
    sys.exit(1)


def main():
    """Main function to run the Task Management System."""
    tasks = []  # List to store all tasks
    
    print("\n" + "=" * 50)
    print("WELCOME TO TASK MANAGEMENT SYSTEM")
    print("=" * 50)
    
    while True:
        # Display menu
        print("\nTask Management System")
        print("1. Add Task")
        print("2. Mark Task as Complete")
        print("3. View Pending Tasks")
        print("4. View Progress")
        print("5. View All Tasks")
        print("6. Update Task Progress")
        print("7. Remove Task")
        print("8. Exit")
        
        choice = input("\nEnter your choice (1-8): ").strip()
        
        # Add Task
        if choice == "1":
            print("\n--- ADD NEW TASK ---")
            
            # Get task details
            title = input("Enter task title: ").strip()
            if not title:
                print("❌ Task title cannot be empty!")
                continue
            
            description = input("Enter description (optional): ").strip()
            due_date = input("Enter due date (YYYY-MM-DD) or press Enter to skip: ").strip()
            
            # Get priority
            print("\nPriority options: H=High, M=Medium, L=Low")
            priority = input("Enter priority (H/M/L): ").strip()
            
            # Add the task
            tasks, success, message = add_task(tasks, title, description, due_date, priority)
            print(message)
        
        # Mark Task as Complete
        elif choice == "2":
            if not tasks:
                print("\n❌ No tasks available! Please add some tasks first.")
                continue
            
            print("\n--- MARK TASK AS COMPLETE ---")
            
            # Show pending tasks
            view_pending_tasks(tasks)
            
            task_num = input("\nEnter task number to mark as complete: ").strip()
            if not task_num:
                print("❌ Operation cancelled.")
                continue
            
            tasks, success, message = mark_task_as_complete(tasks, task_num)
            print(message)
        
        # View Pending Tasks
        elif choice == "3":
            print("\n--- PENDING TASKS ---")
            view_pending_tasks(tasks)
        
        # View Progress
        elif choice == "4":
            print("\n--- PROGRESS TRACKING ---")
            calculate_progress(tasks)
        
        # View All Tasks
        elif choice == "5":
            print("\n--- ALL TASKS ---")
            view_all_tasks(tasks)
        
        # Update Task Progress
        elif choice == "6":
            if not tasks:
                print("\n❌ No tasks available! Please add some tasks first.")
                continue
            
            print("\n--- UPDATE TASK PROGRESS ---")
            
            # Show all tasks
            view_all_tasks(tasks)
            
            task_num = input("\nEnter task number to update: ").strip()
            if not task_num:
                print("❌ Operation cancelled.")
                continue
            
            try:
                progress = int(input("Enter progress percentage (0-100): ").strip())
                tasks, success, message = update_task_progress(tasks, task_num, progress)
                print(message)
            except ValueError:
                print("❌ Invalid input! Please enter a number between 0 and 100.")
        
        # Remove Task
        elif choice == "7":
            if not tasks:
                print("\n❌ No tasks available! Please add some tasks first.")
                continue
            
            print("\n--- REMOVE TASK ---")
            
            # Show all tasks
            view_all_tasks(tasks)
            
            task_num = input("\nEnter task number to remove: ").strip()
            if not task_num:
                print("❌ Operation cancelled.")
                continue
            
            # Confirm deletion
            confirm = input("Are you sure you want to delete this task? (y/n): ").lower()
            if confirm in ['y', 'yes']:
                tasks, success, message = remove_task(tasks, task_num)
                print(message)
            else:
                print("❌ Deletion cancelled.")
        
        # Exit
        elif choice == "8":
            print("\n" + "=" * 50)
            print("👋 Thank you for using Task Management System!")
            if tasks:
                print("\nFinal Progress Summary:")
                calculate_progress(tasks)
            print("\nGoodbye!")
            break
        
        # Invalid choice
        else:
            print("❌ Invalid choice. Please enter a number between 1 and 8.")
        
        # Pause before showing menu again (except when exiting)
        if choice != "8":
            input("\nPress Enter to continue...")


# Run the program
if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 Goodbye!")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ An unexpected error occurred: {e}")
        print("Please restart the application.")
        sys.exit(1)