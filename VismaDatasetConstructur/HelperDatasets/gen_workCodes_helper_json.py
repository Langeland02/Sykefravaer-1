import json
import glob
import os

# Step 1: Load the helper dataset
with open('workCodes_helper.json', 'r') as helper_file:
    helper_data = json.load(helper_file)

# Step 2: Define the JSON files to be processed (based on specific year/number patterns)
json_files = glob.glob('workCodes_*.json')
# Filtering for files matching the required patterns (1, 2020, 2021, 2022, 2023)
required_years = ["1", "2020", "2021", "2022", "2023"]
filtered_files = [file for file in json_files if any(year in file for year in required_years)]

# Step 3: Initialize a counter for edits
edits_count = 0

# Step 4: Process each filtered file
for file_path in filtered_files:
    with open(file_path, 'r') as json_file:
        data = json.load(json_file)

        # Step 5: Extract the work codes from the structure
        for team_name, codes in data.items():
            for work_code in codes.keys():
                # Step 6: Add missing work codes to the helper dataset
                if work_code not in helper_data:
                    helper_data[work_code] = "U"  # Or another default value if needed
                    edits_count += 1  # Increment the counter each time a new code is added

# Step 7: Save the updated helper dataset back to the file
with open('workCodes_helper.json', 'w') as helper_file:
    json.dump(helper_data, helper_file, indent=4)

print(f"Helper dataset updated successfully! Number of edits made: {edits_count}")
