#!/bin/bash
# Setup script for performance visualization dependencies
# Author: Parallel Computing Assignment 3

echo "🚀 Setting up Performance Visualization Environment"
echo "=" * 50

# Check if Python 3 is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.7+ first."
    exit 1
fi

echo "✅ Python 3 found: $(python3 --version)"

# Check if pip is installed
if ! command -v pip3 &> /dev/null; then
    echo "❌ pip3 is not installed. Please install pip first."
    exit 1
fi

echo "✅ pip3 found"

# Install required packages
echo "📦 Installing required Python packages..."

packages=(
    "matplotlib>=3.0.0"
    "numpy>=1.18.0"
    "pandas>=1.0.0"
    "seaborn>=0.11.0"
)

for package in "${packages[@]}"; do
    echo "  Installing $package..."
    pip3 install "$package" || {
        echo "❌ Failed to install $package"
        exit 1
    }
done

echo "✅ All packages installed successfully!"

# Test import
echo "🧪 Testing imports..."
python3 -c "
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
print('✅ All imports successful!')
" || {
    echo "❌ Import test failed"
    exit 1
}

echo ""
echo "🎉 Setup complete! You can now use the visualization tools:"
echo "   • python3 collect_performance_data.py  - Automated data collection"
echo "   • python3 visualize_performance.py     - Comprehensive analysis"
echo "   • python3 quick_plot.py               - Simple manual plotting"

# Make the script executable
chmod +x collect_performance_data.py visualize_performance.py quick_plot.py

echo ""
echo "📋 Next steps:"
echo "1. Build your bitonic sort implementations: make all"
echo "2. Collect performance data: python3 collect_performance_data.py"
echo "3. Generate visualizations: python3 visualize_performance.py"