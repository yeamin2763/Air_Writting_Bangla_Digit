import imgaug.augmenters as iaa
import os
import cv2
import shutil

# Define the augmentation sequence
seq = iaa.Sequential([
    iaa.Affine(scale={"x": (0.8, 1.2), "y": (0.8, 1.2)}),  # Zoom in/out
    iaa.Affine(shear=(-10, 10)),   # Shearing
    iaa.AddToBrightness((-30, 30)), # Brightness adjustment
    iaa.GammaContrast((0.5, 2.0)),  # Contrast adjustment
    iaa.AdditiveGaussianNoise(scale=(0.0, 0.05*255)),  # Noise injection
    #iaa.Fliplr(0.5),  # Horizontal flipping
    #iaa.Flipud(0.5),  # Vertical flipping
    iaa.Sometimes(0.5, iaa.Crop(percent=(0, 0.1))),  # Random cropping
    iaa.Sometimes(0.5, iaa.ElasticTransformation(alpha=(0, 3.0), sigma=0.25))  # Elastic distortion
])

# Path to your collected_data folder
data_folder = "merged_data"

# Create a new folder for augmented data
augmented_folder = os.path.join(data_folder, "augmented_data")
os.makedirs(augmented_folder, exist_ok=True)

# Iterate over each class folder (0-9)
for class_folder in os.listdir(data_folder):
    class_path = os.path.join(data_folder, class_folder)
    
    # Create a folder for the class within augmented data folder
    class_augmented_folder = os.path.join(augmented_folder, class_folder)
    os.makedirs(class_augmented_folder, exist_ok=True)
    
    # Iterate over images in the class folder
    for filename in os.listdir(class_path):
        img_path = os.path.join(class_path, filename)
        
        # Load the image
        img = cv2.imread(img_path)
        
        # Check if the image is loaded successfully
        if img is not None:
            # Apply augmentation sequence to the image
            augmented_images = [seq(image=img) for _ in range(5)]  # Augment each image 5 times
            
            # Save augmented images into the class-specific augmented folder
            for i, aug_img in enumerate(augmented_images):
                aug_img_path = os.path.join(class_augmented_folder, f"{filename.split('.')[0]}_aug_{i}.jpg")
                cv2.imwrite(aug_img_path, aug_img)
        else:
            print(f"Failed to load image: {img_path}")

print("Data augmentation complete.")
