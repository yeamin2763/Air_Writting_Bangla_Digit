import os

def change_folder_names(directory):
    # Directory traversal
    for foldername in os.listdir(directory):
        # Check if it's a folder
        if os.path.isdir(os.path.join(directory, foldername)):
            old_name = os.path.join(directory, foldername)
            # New name logic (modify this according to your requirement)
            new_name = os.path.join(directory, "new_" + foldername)
            # Rename the folder
            os.rename(old_name, new_name)
            print(f"Renamed {old_name} to {new_name}")

# Directory path
directory_path = '/path/to/collected_data'

# Call the function to change folder names
change_folder_names(directory_path)
