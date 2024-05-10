from PIL import Image
import os

def compress_images(input_folder, output_folder, target_size_min, target_size_max):
    # Create the output folder if it doesn't exist
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    
    # Loop through each file in the input folder
    for filename in os.listdir(input_folder):
        input_path = os.path.join(input_folder, filename)
        output_path = os.path.join(output_folder, filename)
        
        # Check if the current item is a directory
        if os.path.isdir(input_path):
            # Recursively call the function for subdirectories
            compress_images(input_path, os.path.join(output_folder, filename), target_size_min, target_size_max)
        else:
            # Open the image
            img = Image.open(input_path)
            
            # Compress the image while maintaining quality within the target size range
            quality = 95  # Initial quality
            img.save(output_path, optimize=True, quality=quality)
            
            # Check if the compressed image size is within the target range
            while os.path.getsize(output_path) > target_size_max and quality > 0:
                # Reduce quality further until the size falls within the target range
                quality -= 5
                img.save(output_path, optimize=True, quality=quality)
            
            # Check if the size is below the minimum target size
            if os.path.getsize(output_path) < target_size_min:
                # Increase quality until it reaches the maximum while still keeping size within range
                while os.path.getsize(output_path) < target_size_min and quality <= 100:
                    quality += 5
                    img.save(output_path, optimize=True, quality=quality)
            
            print(f"Compressed {filename} to {os.path.getsize(output_path) / (1024 * 1024):.2f} MB with quality {quality}")

# Define input and output folders
input_folder = "train_test_split/train"
output_folder = "train_test_split/train_1"
target_size_min = 100 * 1024 * 1024  # 100 MB in bytes
target_size_max = 200 * 1024 * 1024  # 200 MB in bytes

# Compress images within subfolders labeled from 0 to 9
for folder_name in os.listdir(input_folder):
    folder_path = os.path.join(input_folder, folder_name)
    if os.path.isdir(folder_path):
        compress_images(folder_path, os.path.join(output_folder, folder_name), target_size_min, target_size_max)
