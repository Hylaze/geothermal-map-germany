import json, csv, pandas as pd
from fuzzywuzzy import fuzz, process
# Input and output file paths
input_file_path_json = "geotis_filtered.json"
input_file_path_excel = "projektliste.xlsx"
output_file_path = "data_output.json"
output_file_path_csv = "projektliste.csv"


# Load JSON file into a DataFrame
with open(input_file_path_json, "r", encoding="utf-8") as json_file:
    json_data = json.load(json_file)

# Assuming the JSON data has a "features" key with a list of features
# Adjust `json_normalize` path as needed based on JSON structure
json_df = pd.json_normalize(json_data['features'])

# Load Excel file into a DataFrame
# Load Excel file, skipping rows and setting the correct header
excel_df = pd.read_excel(
    "projektliste.xlsx",
    skiprows=3,  # Adjust based on where the actual headers start
    header=0   # Set the correct header row
)

# Display the head of each DataFrame
# print("JSON DataFrame:")
# print(json_df.info())
# print(json_df.columns.tolist())


# Save the DataFrame to a CSV file
# Path to the CSV file
input_file_path_csv = "projektliste_export.csv"

# Read the CSV file with semicolon delimiter
csv_df = pd.read_csv(input_file_path_csv, sep=';', encoding="utf-8")

# Print the first few rows to inspect the data
# print("CSV DataFrame:")
# print(csv_df.info())
# print(csv_df.columns.tolist())
# Function to get the best match from a list of strings
def get_best_match(query, choices, score_cutoff=60):
    # Get the best match using fuzzywuzzy
    result = process.extractOne(query, choices, scorer=fuzz.token_sort_ratio)
    
    # Debug: print the result to understand the structure
   # print(f"Debug - Matching result for query '{query}': {result}")

    if result:
        # Unpack only the first two elements (best_match and score)
        best_match, score, _ = result  # Ignore the third element
        if score >= score_cutoff:
            return best_match
    return None  # Return None if no valid match is found

# Create a new column in json_df with the best match for each "properties.name" in csv_df['Name']
json_df['best_match_name'] = json_df['properties.title'].apply(lambda x: get_best_match(x, csv_df['Name']))

# Now merge the data on the matched names
merged_df = pd.merge(json_df, csv_df, left_on='best_match_name', right_on='Name', how='left')

# Display the merged DataFrame
print(merged_df.head())
columns_order = ['Name', 'properties.title'] + [col for col in merged_df.columns if col not in ['Name', 'properties.title']]

# Reorder the DataFrame
merged_df = merged_df[columns_order]

merged_df.to_csv("merged_geothermie_data.csv", index=False, encoding="utf-8")