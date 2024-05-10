import os
import shutil

def merge_data(source_folder, destination_folder):
    if not os.path.exists(destination_folder):
        os.makedirs(destination_folder)

    for person_folder in os.listdir(source_folder):
        person_folder_path = os.path.join(source_folder, person_folder)
        if os.path.isdir(person_folder_path):
            for class_folder in range(10):
                class_source_folder = os.path.join(person_folder_path, str(class_folder))
                if os.path.exists(class_source_folder):
                    for root, dirs, files in os.walk(class_source_folder):
                        for index, file in enumerate(files):
                            source_file = os.path.join(root, file)
                            destination_file = os.path.join(destination_folder, str(class_folder), f"{person_folder}_{class_folder}_{index}{os.path.splitext(file)[1]}")
                            if not os.path.exists(os.path.dirname(destination_file)):
                                os.makedirs(os.path.dirname(destination_file))
                            shutil.copy(source_file, destination_file)

# Source folder containing data for each person
source_folder = 'collected_data'

# Destination folder where merged data will be stored
destination_folder = 'merged_data'

merge_data(source_folder, destination_folder)
