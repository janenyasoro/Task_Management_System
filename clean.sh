#!/bin/bash
echo "🧹 Cleaning cache files..."
find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null
find . -name "*.pyc" -delete
echo "✅ Clean complete!"
