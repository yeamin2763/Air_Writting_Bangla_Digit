import os
import shutil

def rename_and_move_images(dataset_path):
    # Iterate through each digit folder (0-9)
    for digit_folder in os.listdir(dataset_path):
        digit_folder_path = os.path.join(dataset_path, digit_folder)
        if os.path.isdir(digit_folder_path):
            # Get list of images in the digit folder
            images = os.listdir(digit_folder_path)
            # Rename and move each image to its respective folder
            for i, image in enumerate(images):
                # Splitting the file extension
                name, ext = os.path.splitext(image)
                # Renaming the image file
                new_name = f"{digit_folder}_{i+1}{ext}"
                old_image_path = os.path.join(digit_folder_path, image)
                new_image_path = os.path.join(digit_folder_path, new_name)  # Modified this line
                os.rename(old_image_path, new_image_path)
                # Move the renamed image to its respective digit folder
                shutil.move(new_image_path, os.path.join(dataset_path, digit_folder, new_name))
                print(f"Moved {new_name} to {digit_folder}")

# Provide the path to your dataset folder
dataset_path = "merged_data"
rename_and_move_images(dataset_path)
