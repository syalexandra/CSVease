#!/bin/bash

run_lexer() {
    echo "Input a string you would to tokenize:"
    read user_input
    echo $user_input
    python3 lexer.py "$user_input"
    echo
    echo "Do you want to run it again? (yes/no)"
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
