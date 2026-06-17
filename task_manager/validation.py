# task_manager/validation.py
# Input validation functions

from typing import Tuple, Optional


def validate_menu_choice(choice: str, max_choice: int) -> Tuple[bool, Optional[int], str]:
    """Validate menu choice."""
    try:
        num = int(choice)
        if 1 <= num <= max_choice:
            return True, num, "Valid"
        else:
            return False, None, f"Enter a number between 1 and {max_choice}"
    except (ValueError, TypeError):
        return False, None, "Invalid input! Please enter a number."


def validate_task_number(task_num: str, total_tasks: int) -> Tuple[bool, Optional[int], str]:
    """Validate task number."""
    if total_tasks == 0:
        return False, None, "No tasks available!"
    
    try:
        num = int(task_num)
        if 1 <= num <= total_tasks:
            return True, num - 1, "Valid"
        else:
            return False, None, f"Enter a number between 1 and {total_tasks}"
    except (ValueError, TypeError):
        return False, None, "Invalid input! Please enter a number."


def validate_progress(progress: str) -> Tuple[bool, Optional[int], str]:
    """Validate progress percentage."""
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