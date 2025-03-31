#!/bin/bash

# Define the strings
# string1="vbiasn0"
# string2="vbiasn0={{vbiasn0}} "
# string3=""

# # Define the directory
# folder="/homes/dkochar/migration_project/open-source/working_superset/working_PTM_new/working_current/eval_engines/spectre/netlist_templates/7nm"

# # Loop through all files in the folder
# for file in "$folder"/*; do
#  # Check if the file is a regular file
#  if [[ -f "$file" ]]; then
#    # Search for string1 starting from line 4
#    if ! tail -n +4 "$file" | grep -q "$string1"; then
#      # Replace string2 with string3 if string1 is not found
#      sed -i "s/$string2/$string3/g" "$file"
#    fi
#  fi
# done

# Variables for the strings to search
# string1="Vbiasp0"
# string2="//.PININFO"
# string3="V"

# # Folder containing the files to be processed
# folder_path="/homes/dkochar/migration_project/open-source/working_superset/working_PTM_new/working_current/eval_engines/spectre/netlist_templates/7nm"

# # Loop through all files in the folder
# for file in "$folder_path"/*; do
#   # Check if file is a regular file
#   if [[ -f $file ]]; then
#     # Flag to determine if string1 was found in lines starting with string2
#     found_string1_in_string2=false

#     # Read through the file line by line
#     while IFS= read -r line; do
#       # Check if the line starts with string2 and contains string1
#       if [[ $line == "$string2"* ]] && [[ $line == *"$string1"* ]]; then
#         found_string1_in_string2=true
#         break
#       fi
#     done < "$file"

#     # If string1 was not found in any line starting with string2, process the file
#     if ! $found_string1_in_string2; then
#       # Create a temporary file to store the processed content
#       temp_file=$(mktemp)

#       # Read through the file line by line again to remove the required lines
#       while IFS= read -r line; do
#         # Remove lines that start with string3 and contain string1
#         if [[ $line == "$string3"* ]] && [[ $line == *"$string1"* ]]; then
#           continue
#         fi
#         # Otherwise, write the line to the temporary file
#         echo "$line" >> "$temp_file"
#       done < "$file"

#       # Move the temporary file back to the original file
#       mv "$temp_file" "$file"
#     fi
#   fi
# done


# # # Folder containing the files to be processed
# # folder_path="/homes/dkochar/migration_project/open-source/working_superset/working_PTM_new/working_current/eval_engines/spectre/netlist_templates/7nm"
# # # Loop through all files in the folder
# # for file in "$folder_path"/*; do
# #   # Check if file is a regular file
# #   if [[ -f $file ]]; then
# #     # Use sed to replace "x" with "x0" only when it is standalone
# #     sed -i 's/\<Vbiasn\>/Vbiasn0/g' "$file"
# #   fi
# # done

#!/bin/bash

#!/bin/bash

# Define your strings and folder path
string1="MM14 "
string2=" MM14:gm MM14:ids MM14:region"
string3="save "
folder_path="/homes/dkochar/migration_project/open-source/working_superset/working_PTM_new/working_current/eval_engines/spectre/netlist_templates/7nm"

# Loop through all files in the folder
for file in "$folder_path"/*; do
  # Check if file is a regular file
  if [[ -f $file ]]; then
    # Check if the file contains string1
    if grep -q "$string1" "$file"; then
      # Append string2 to the end of lines starting with string3
      sed -i "/^$string3/s/$/ $string2/" "$file"
    fi
  fi
done
