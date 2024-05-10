import os
import shutil
import random

# Path to the augmented_data folder
data_folder = "collected_data"

# Path to the train and test folders
train_folder = "train"
test_folder = "test"

# Create train and test folders if they don't exist
os.makedirs(train_folder, exist_ok=True)
os.makedirs(test_folder, exist_ok=True)

# Function to split data into train and test sets
def split_data(data_folder, train_folder, test_folder, split_ratio=0.7):
    # Loop through each digit folder (0-9)
    for digit_folder in os.listdir(data_folder):
        digit_path = os.path.join(data_folder, digit_folder)
        if os.path.isdir(digit_path):
            # Create train and test folders for the current digit
            os.makedirs(os.path.join(train_folder, digit_folder), exist_ok=True)
            os.makedirs(os.path.join(test_folder, digit_folder), exist_ok=True)
            images = os.listdir(digit_path)
            random.shuffle(images)  # Shuffle images randomly
            split_index = int(len(images) * split_ratio)
            train_images = images[:split_index]
            test_images = images[split_index:]
            # Move images to train folder
            for img in train_images:
                src = os.path.join(digit_path, img)
                dst = os.path.join(train_folder, digit_folder, img)
                shutil.copy(src, dst)
            # Move images to test folder
            for img in test_images:
                src = os.path.join(digit_path, img)
                dst = os.path.join(test_folder, digit_folder, img)
                shutil.copy(src, dst)

# Call the split_data function
split_data(data_folder, train_folder, test_folder)
