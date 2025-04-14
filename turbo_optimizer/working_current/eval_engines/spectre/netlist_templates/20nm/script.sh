#!/bin/bash

# Directory containing the text files
DIR="/homes/dkochar/migration_project/open-source/working_superset/working_PTM_new/working_current/eval_engines/spectre/netlist_templates/7nm"

# Loop through all text files in the directory
for FILE in "$DIR"/*.scs; do
    # Use a temporary file to store the updated content
    TEMP_FILE=$(mktemp)

    # Read each line of the file
    while IFS= read -r LINE; do
        # Check if the line contains "save MM"
        if [[ $LINE == *"save V0"* ]]; then
            # Process the line to add the ":vgs" entries
            UPDATED_LINE=$(echo "$LINE" | sed -E 's/(MM[0-9]+:gm)/\1 \1:vgs \1:vds/g')
            echo "$UPDATED_LINE" >> "$TEMP_FILE"
        else
            echo "$LINE" >> "$TEMP_FILE"
        fi
    done < "$FILE"

    # Replace the original file with the updated content
    mv "$TEMP_FILE" "$FILE"
done


# Loop through all text files in the directory and replace "gm:vgs" with "vgs"
for FILE in "$DIR"/*.scs; do
    sed -i 's/gm:vgs/vgs/g' "$FILE"
    sed -i 's/gm:vds/vds/g' "$FILE"
done

echo "All files have been processed."
