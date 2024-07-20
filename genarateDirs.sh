#!/bin/bash

# List of filenames
FILENAMES=("Adventures of Tintin" "Jack and Jill" "Glee" "The Vampire Diaries" "King Arthur" "Windows XP"
           "Harry Potter" "Kung Fu Panda" "Lady Gaga" "Twilight" "Windows 8" "Mission Impossible"
           "Turn Up The Music" "Super Mario" "American Pickers" "Microsoft Office 2010"
           "Happy Feet" "Modern Family" "American Idol" "Hacking for Dummies")

# Number of directories
NUM_DIRECTORIES=$1

# Function to generate a random file with 1MB content
generate_random_file() {
    FILENAME=$1
    head -c 1M </dev/urandom >"$FILENAME"
}

# Create directories and files
for ((i = 1; i <= NUM_DIRECTORIES; i++)); do
    DIRECTORY="drive$i"
    mkdir -p "$DIRECTORY"
    for FILENAME in "${FILENAMES[@]}"; do
        RANDOM_FILENAME="${FILENAMES[$RANDOM % ${#FILENAMES[@]}]}"
        generate_random_file "$DIRECTORY/$RANDOM_FILENAME.txt"
    done
done

echo "Directories and files generated successfully!"
