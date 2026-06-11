# Task Management System

A comprehensive, modular task management system built in Python that allows users to manage tasks, track progress, and stay organized.

## Features

- ✅ **Add Tasks** - Create new tasks with title, description, due date, and priority
- ✅ **Mark Complete** - Mark tasks as done when finished
- ✅ **Update Progress** - Track progress from 0% to 100%
- ✅ **View Pending** - See only incomplete tasks
- ✅ **View All Tasks** - Display complete task list with status
- ✅ **Progress Tracking** - Visual progress bars and statistics
- ✅ **Search Tasks** - Find tasks by keyword, priority, or status
- ✅ **Filter by Priority** - View High/Medium/Low priority tasks
- ✅ **Remove Tasks** - Delete tasks with confirmation
- ✅ **Input Validation** - All user inputs are validated

## Directory Structure

## Installation

### Prerequisites
- Python 3.6 or higher
- No external dependencies required (uses only standard library)

### Setup

1. **Clone or download** the project files to your computer

2. **Verify the directory structure:**
   ```bash
   task_management_system/
   ├── main.py
   └── task_manager/
       ├── __init__.py
       ├── task_utils.py
       └── validation.py
Adding a Task
When adding a task, you'll be prompted for:

Title (required, min 3 characters)

Description (optional)

Due Date (optional, format: YYYY-MM-DD)

Priority (High/Medium/Low or H/M/L)

Progress Tracking
Tasks can have progress from 0% to 100%

Visual progress bars show completion status

Overall statistics show completion rates

Priority breakdown shows progress by priority level