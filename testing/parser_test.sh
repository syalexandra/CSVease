#!/bin/bash

run_parser() {
    echo "Available tests:"
    cd input/
    # List all files and number them
    files=($(ls *.ease 2>/dev/null))
    if [ ${#files[@]} -eq 0 ]; then
        echo "No .ease files found."
        return
    fi
    
    for i in "${!files[@]}"; do
        echo "$((i+1)). $(basename ${files[$i]})"  # Just show filename without path
    done
    
    echo
    echo "Please enter the number of the file you would like to tokenize (or 'exit' to quit):"
    read user_input

    # Check if the user wants to exit
    if [ "$user_input" = "exit" ]; then
        echo "Exiting..."
        exit 0
    fi

    # Validate the input as a number
    if ! [[ "$user_input" =~ ^[0-9]+$ ]]; then
        echo "Invalid input. Please enter a number."
        return
    fi

    # Get the selected file
    file_index=$((user_input-1))
    if [ $file_index -lt 0 ] || [ $file_index -ge ${#files[@]} ]; then
        echo "Invalid selection. Please try again."
        return  # Fixed typo 'returnå'
    fi
    
    selected_file="${files[$file_index]}"
    # Call the Python lexer with the selected file
    python3 ../CSVeaseParser.py "$selected_file"
    echo

    # Ask if the user wants to run it again
    echo "Do you want to try a different file? (yes/no)"
    read answer
}

# Start the loop
while true; do
    run_parser

    if [ "$answer" != "yes" ]; then
        echo "Exiting..."
        break
    fi
done