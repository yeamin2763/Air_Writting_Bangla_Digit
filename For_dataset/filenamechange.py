import os

def change_filenames(directory):
    # Iterate through each sub-folder (0-9)
    for subdir in range(10):
        subdir_path = os.path.join(directory, str(subdir))
        # Check if the sub-folder exists
        if os.path.exists(subdir_path):
            # Iterate through each file in the sub-folder
            for idx, filename in enumerate(os.listdir(subdir_path)):
                # Construct the new filename
                new_filename = f"{subdir}_{idx+1}.jpg"  # Assuming JPG images, change extension accordingly if needed
                # Rename the file
                os.rename(os.path.join(subdir_path, filename), os.path.join(subdir_path, new_filename))
                print(f"Renamed {filename} to {new_filename}")

# Directory where collected_data folder is located
directory = "small_data_1"
change_filenames(directory)
