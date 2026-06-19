# task_manager/validation.py
# Input validation functions

from datetime import datetime
from typing import Tuple, Optional


def validate_task_title(title: str) -> Tuple[bool, str]:
    """
    Validate task title input.
    """
    # Check if title is empty or just whitespace
    if not title or title.strip() == "":
        return False, "Task title cannot be empty!"
    
    # Clean the title
    cleaned_title = title.strip()
    
    # Check minimum length using len()
    if len(cleaned_title) < 3:
        return False, "Task title must be at least 3 characters long!"
    
    # Check maximum length using len()
    if len(cleaned_title) > 100:
        return False, "Task title is too long! Maximum 100 characters."
    
    # Check for invalid characters
    invalid_chars = ['|', '\\', '/', '*', '?', '<', '>', ':', '"']
    if any(char in cleaned_title for char in invalid_chars):
        return False, f"Task title contains invalid characters: {', '.join(invalid_chars)}"
    
    return True, cleaned_title


def validate_task_description(description: str) -> Tuple[bool, str]:
    """
    Validate task description input.
    """
    # Description is optional, so empty is allowed
    if not description or description.strip() == "":
        return True, ""
    
    cleaned_description = description.strip()
    
    # Check maximum length using len()
    if len(cleaned_description) > 500:
        return False, "Task description is too long! Maximum 500 characters."
    
    return True, cleaned_description


def validate_due_date(due_date: str) -> Tuple[bool, str, Optional[str]]:
    """
    Validate due date input.
    """
    # Check if date is provided (optional)
    if not due_date or due_date.strip() == "":
        return True, "No due date provided", None
    
    due_date = due_date.strip()
    
    # Try different date formats
    date_formats = [
        "%Y-%m-%d",  # 2024-12-25
        "%d/%m/%Y",  # 25/12/2024
        "%m/%d/%Y",  # 12/25/2024
        "%Y/%m/%d",  # 2024/12/25
        "%d-%m-%Y",  # 25-12-2024
        "%m-%d-%Y",  # 12-25-2024
    ]
    
    for date_format in date_formats:
        try:
            parsed_date = datetime.strptime(due_date, date_format)
            
            # Check if date is not in the past (allow today)
            today = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
            if parsed_date < today:
                return False, f"Due date {parsed_date.strftime('%Y-%m-%d')} is in the past!", None
            
            # Return standardized format
            standardized_date = parsed_date.strftime("%Y-%m-%d")
            return True, "Valid", standardized_date
            
        except ValueError:
            continue
    
    return False, "Invalid date format! Use YYYY-MM-DD, DD/MM/YYYY, or MM/DD/YYYY", None


def validate_priority(priority: str) -> Tuple[bool, Optional[str], str]:
    """
    Validate priority level input.
    """
    valid_priorities = {
        "High": ["High", "high", "H", "1", "HIGH"],
        "Medium": ["Medium", "medium", "M", "2", "MEDIUM"],
        "Low": ["Low", "low", "L", "3", "LOW"]
    }
    
    # Check if priority is empty
    if not priority or priority.strip() == "":
        return False, None, "Priority cannot be empty!"
    
    priority = priority.strip()
    
    # Check if priority is valid
    for standard_priority, variations in valid_priorities.items():
        if priority in variations:
            return True, standard_priority, "Valid"
    
    return False, None, "Invalid priority! Choose High, Medium, or Low (or H/M/L)"


def validate_task_number(task_number: str, total_tasks: int) -> Tuple[bool, Optional[int], str]:
    """
    Validate task number input - handles ValueError.
    """
    # Check if there are any tasks
    if total_tasks == 0:
        return False, None, "No tasks available!"
    
    try:
        # Convert to integer - this handles ValueError
        task_num = int(task_number)
        if 1 <= task_num <= total_tasks:
            return True, task_num - 1, "Valid"  # Return 0-based index
        else:
            return False, None, f"Invalid task number! Please enter a number between 1 and {total_tasks}"
    except ValueError:
        # This catches the ValueError when input is not a number
        return False, None, "Invalid input! Please enter a valid number."


def validate_progress(progress: str) -> Tuple[bool, Optional[int], str]:
    """
    Validate progress percentage input - handles ValueError.
    """
    # Check if progress is empty
    if not progress or progress.strip() == "":
        return False, None, "Progress cannot be empty!"
    
    try:
        # Convert to integer - this handles ValueError
        progress_num = int(progress)
        if 0 <= progress_num <= 100:
            return True, progress_num, "Valid"
        else:
            return False, None, "Progress must be between 0 and 100!"
    except ValueError:
        # This catches the ValueError when input is not a number
        return False, None, "Invalid input! Please enter a number between 0 and 100."


def validate_menu_choice(choice: str, max_choice: int) -> Tuple[bool, Optional[int], str]:
    """
    Validate menu choice input - handles ValueError.
    """
    try:
        # Convert to integer - this handles ValueError
        choice_num = int(choice)
        if 1 <= choice_num <= max_choice:
            return True, choice_num, "Valid"
        else:
            return False, None, f"Invalid choice! Please enter a number between 1 and {max_choice}"
    except ValueError:
        # This catches the ValueError when input is not a number
        return False, None, "Invalid input! Please enter a number."


def validate_yes_no(prompt: str) -> bool:
    """
    Validate yes/no input.
    """
    while True:
        response = input(prompt + " (y/n): ").lower().strip()
        if response in ['y', 'yes']:
            return True
        elif response in ['n', 'no']:
            return False
        else:
            print("❌ Please enter 'y' or 'n'")


def validate_email(email: str) -> Tuple[bool, str]:
    """
    Validate email format.
    """
    if not email or email.strip() == "":
        return False, "Email cannot be empty!"
    
    email = email.strip()
    
    # Check length
    if len(email) < 5:
        return False, "Email is too short!"
    
    # Basic email validation
    import re
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    
    if re.match(pattern, email):
        return True, email
    else:
        return False, "Invalid email format!"


def validate_date_range(start_date: str, end_date: str) -> Tuple[bool, str]:
    """
    Validate that end date is after start date.
    """
    is_valid_start, _, start_standardized = validate_due_date(start_date)
    is_valid_end, _, end_standardized = validate_due_date(end_date)
    
    if not is_valid_start:
        return False, "Invalid start date format!"
    
    if not is_valid_end:
        return False, "Invalid end date format!"
    
    if start_standardized and end_standardized:
        if start_standardized > end_standardized:
            return False, "End date must be after start date!"
    
    return True, "Valid"


def validate_non_empty_string(value: str, field_name: str = "Field") -> Tuple[bool, str]:
    """
    Validate that a string is not empty.
    """
    if not value or value.strip() == "":
        return False, f"{field_name} cannot be empty!"
    
    return True, value.strip()