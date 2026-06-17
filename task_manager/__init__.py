# task_manager/__init__.py
# Package initializer - makes task_manager a Python package

"""
Task Manager Package

A comprehensive task management system with validation and progress tracking.
"""

# Import from task_utils
from task_manager.task_utils import (
    add_task,
    mark_task_as_complete,
    view_pending_tasks,
    view_all_tasks,
    update_task_progress,
    calculate_progress,
    remove_task,
    create_progress_bar,
    get_priority_icon
)

# Import from validation
from task_manager.validation import (
    validate_task_title,
    validate_task_description,
    validate_due_date,
    validate_priority,
    validate_task_number,
    validate_progress,
    validate_menu_choice,
    validate_yes_no,
    validate_email,
    validate_date_range
)

# Package metadata
__version__ = "1.0.0"
__author__ = "Task Management System"
__description__ = "A modular task management system with validation and progress tracking"

# Define what gets imported with "from task_manager import *"
__all__ = [
    # From task_utils
    "add_task",
    "mark_task_as_complete",
    "view_pending_tasks",
    "view_all_tasks",
    "update_task_progress",
    "calculate_progress",
    "remove_task",
    "create_progress_bar",
    "get_priority_icon",
    
    # From validation
    "validate_task_title",
    "validate_task_description",
    "validate_due_date",
    "validate_priority",
    "validate_task_number",
    "validate_progress",
    "validate_menu_choice",
    "validate_yes_no",
    "validate_email",
    "validate_date_range"
]