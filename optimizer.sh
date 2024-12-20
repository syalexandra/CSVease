#!/bin/bash

# Display the options to the user
echo "Select an optimization test to run:"
echo "1. Dead code elimination"
echo "2. Constant Propagation"
echo "3. Constant Folding"
echo "4. Common SubExpression Elimination"
echo "Enter the number corresponding to your choice:"

# Read user input
read -r choice

# Execute the corresponding command based on the user's choice
case $choice in
    1)
        echo "Running Dead Code Elimination..."
        python3 CSVeaseOptimizer.py input/optimizer/DeadCodeElimination.ease DeadCodeElimination
        ;;
    2)
        echo "Running Constant Propagation..."
        python3 CSVeaseOptimizer.py input/optimizer/ConstantPropogation.ease ConstantPropagation
        ;;
    3)
        echo "Running Constant Folding..."
        python3 CSVeaseOptimizer.py input/optimizer/ConstantFolding.ease ConstantFolding
        ;;
    4)
        echo "Running Common SubExpression Elimination..."
        python3 CSVeaseOptimizer.py input/optimizer/CommonSubExpressionElimination.ease CommonSubExpressionElimination
        ;;
    *)
        echo "Invalid choice. Please run the script again and select a valid option."
        ;;
esac
