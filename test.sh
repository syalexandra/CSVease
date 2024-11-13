#!/bin/bash

run_test() {
    echo "Available tests:"
    
    # List all files in testing directory
    cd testing
    files=($(ls))
    if [ ${#files[@]} -eq 0 ]; then
        echo "No test files found in testing directory."
        cd ..
        return
    fi
    
    for i in "${!files[@]}"; do
        echo "$((i+1)). ${files[$i]}"
    done
    cd ..
    
    echo
    echo "Which test would you like to run?"
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
        return
    fi
    
    if [ "${files[$file_index]}" = "lexer_test.sh" ]; then
        echo "--------------------------"
        echo "TESTING LEXER"
        echo "--------------------------"
    fi

    if [ "${files[$file_index]}" = "parser_test.sh" ]; then
        echo "--------------------------"
        echo "TESTING PARSER"
        echo "--------------------------"
    fi

    if [ "${files[$file_index]}" = "pipeline.sh" ]; then
        echo "--------------------------"
        echo "TESTING PIPELINE"
        echo "--------------------------"
    fi

    selected_test="testing/${files[$file_index]}"

    # Execute the shell script
    bash "$selected_test"
    echo

    if [ "${files[$file_index]}" = "lexer_test.sh" ]; then
        echo "--------------------------"
        echo "COMPLETED TESTING LEXER"
        echo "--------------------------"
        echo
    fi

    if [ "${files[$file_index]}" = "parser_test.sh" ]; then
        echo "--------------------------"
        echo "COMPLETED TESTING PARSER"
        echo "--------------------------"
        echo
    fi

    if [ "${files[$file_index]}" = "pipeline.sh" ]; then
        echo "--------------------------"
        echo "COMPLETED TESTING PIPELINE"
        echo "--------------------------"
        echo
    fi


    echo "Would you like to run another test? (yes/no)"
    read answer
    if [ "$answer" != "yes" ]; then
        echo "Exiting..."
        exit 0
    fi
}

# Start the loop
while true; do
    run_test
done