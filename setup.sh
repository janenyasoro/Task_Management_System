#!/bin/bash
# Complete setup script for Task Management System

echo "🚀 Setting up Task Management System..."

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
source venv/bin/activate

# Create task_manager directory if it doesn't exist
if [ ! -d "task_manager" ]; then
    mkdir task_manager
    echo "📁 Created task_manager directory"
fi

# Create __init__.py if it doesn't exist
if [ ! -f "task_manager/__init__.py" ]; then
    cat > task_manager/__init__.py << 'EOF'
# task_manager/__init__.py
from task_manager.task_utils import *
from task_manager.validation import *

__all__ = [
    "add_task",
    "mark_task_as_complete",
    "view_pending_tasks",
    "view_all_tasks",
    "update_task_progress",
    "calculate_progress",
    "remove_task",
    "validate_task_title",
    "validate_task_description",
    "validate_due_date",
    "validate_priority",
    "validate_task_number",
    "validate_progress",
    "validate_menu_choice",
    "validate_yes_no"
]
EOF
    echo "✅ Created task_manager/__init__.py"
fi

# Create requirements.txt if it doesn't exist
if [ ! -f "requirements.txt" ]; then
    echo "# No external dependencies" > requirements.txt
    echo "✅ Created requirements.txt"
fi

# Install dependencies
echo "📦 Installing dependencies..."
pip install -r requirements.txt

# Clean up __pycache__ files
echo "🧹 Cleaning up __pycache__..."
find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null

echo ""
echo "✅ Setup complete!"
echo ""
echo "📋 To run the program:"
echo "   source venv/bin/activate"
echo "   python3 main.py"
echo ""
echo "📋 To run tests:"
echo "   export TEST_MODE=1"
echo "   python3 main.py"