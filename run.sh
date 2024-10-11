#!/bin/bash

run_lexer() {
    echo "Available files:"
    ls *.txt 2>/dev/null
    
    echo 
    echo "Please enter the name of the file you would like to tokenize (or 'exit' to quit):"
    read user_input

    # Check if the user wants to exit
    if [ "$user_input" = "exit" ]; then
        echo "Exiting..."
        exit 0
    fi

    # Check if the file exists
    if [ ! -f "$user_input" ]; then
        echo "File not found. Please try again."
        return  # Return to the main loop
    fi

    # Call the Python lexer with the chosen file
    python3 CSVeaseLexer.py "$user_input"
    echo

    # Ask if the user wants to run it again
    echo "Do you want to try a different file? (yes/no)"
    read answer
}

# Start the loop
while true; do
    run_lexer

    if [ "$answer" != "yes" ]; then
        echo "Exiting..."
        break
    fi
done
