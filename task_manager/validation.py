from typing import Tuple, Optional


def validate_menu_choice(choice: str, max_choice: int) -> Tuple[bool, Optional[int], str]:
    """
    Validate menu choice input.
    
    Args:
        choice: User's input string
        max_choice: Maximum valid choice number
    
    Returns:
        Tuple of (is_valid, choice_number, error_message)
    """
    try:
        num = int(choice)
        if 1 <= num <= max_choice:
            return True, num, "Valid"
        else:
            return False, None, f"Please enter a number between 1 and {max_choice}"
    except ValueError:
        return False, None, "Invalid input! Please enter a number."


def validate_task_number(task_num: str, total_tasks: int) -> Tuple[bool, Optional[int], str]:
    """
    Validate task number input.
    
    Args:
        task_num: User's task number input
        total_tasks: Total number of tasks
    
    Returns:
        Tuple of (is_valid, task_index, error_message)
    """
    if total_tasks == 0:
        return False, None, "No tasks available!"
    
    try:
        num = int(task_num)
        if 1 <= num <= total_tasks:
            return True, num - 1, "Valid"  # Return 0-based index
        else:
            return False, None, f"Please enter a number between 1 and {total_tasks}"
    except ValueError:
        return False, None, "Invalid input! Please enter a number."


def validate_progress(progress: str) -> Tuple[bool, Optional[int], str]:
    """
    Validate progress percentage input.
    
    Args:
        progress: User's progress input
    
    Returns:
        Tuple of (is_valid, progress_value, error_message)
    """
    if not progress or progress.strip() == "":
        return False, None, "Progress cannot be empty!"
    
    try:
        num = int(progress)
        if 0 <= num <= 100:
            return True, num, "Valid"
        else:
            return False, None, "Progress must be between 0 and 100!"
    except ValueError:
        return False, None, "Invalid input! Please enter a number."


def validate_priority(priority: str) -> Tuple[bool, str, str]:
    """
    Validate priority input.
    
    Args:
        priority: User's priority input
    
    Returns:
        Tuple of (is_valid, validated_priority, error_message)
    """
    if not priority or priority.strip() == "":
        return False, "Medium", "Priority cannot be empty! Using Medium."
    
    priority = priority.strip().upper()
    
    if priority in ['H', 'HIGH', '1']:
        return True, "High", "Valid"
    elif priority in ['M', 'MEDIUM', '2']:
        return True, "Medium", "Valid"
    elif priority in ['L', 'LOW', '3']:
        return True, "Low", "Valid"
    else:
        return False, "Medium", f"Invalid priority '{priority}'. Using Medium."


def validate_yes_no(prompt: str) -> bool:
    """
    Validate yes/no input.
    
    Args:
        prompt: Message to display to user
    
    Returns:
        True for yes, False for no
    """
    while True:
        response = input(prompt + " (y/n): ").lower().strip()
        if response in ['y', 'yes']:
            return True
        elif response in ['n', 'no']:
            return False
        else:
            print("❌ Please enter 'y' or 'n'")