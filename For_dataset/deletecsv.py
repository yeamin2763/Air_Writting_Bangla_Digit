import os

# Specify the directory containing the data
data_dir = "merged_data"

# Function to delete CSV files within the collected_data folder
def delete_csv_files(root_dir):
    for root, dirs, files in os.walk(root_dir):
        for file in files:
            if file.endswith(".csv"):  # Check if the file is a CSV
                file_path = os.path.join(root, file)
                os.remove(file_path)  # Delete the file
                print(f"Deleted: {file_path}")

# Call the function to delete CSV files
delete_csv_files(data_dir)
