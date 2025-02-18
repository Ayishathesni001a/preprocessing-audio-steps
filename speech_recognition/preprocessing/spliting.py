import os
import glob
import shutil
import random

# Define the input directory (features from normalization)
input_dir = "/home/user/Desktop/voice-to-text/speech_recognition/preprocessing/output_feature_normalise"

# Define the new output directory for splitting
split_output_dir = "/home/user/Desktop/voice-to-text/speech_recognition/preprocessing/output_spliting"
os.makedirs(split_output_dir, exist_ok=True)

# Create subdirectories for train, valid, and test within the output_spliting folder
train_dir = os.path.join(split_output_dir, "train")
valid_dir = os.path.join(split_output_dir, "valid")
test_dir  = os.path.join(split_output_dir, "test")

os.makedirs(train_dir, exist_ok=True)
os.makedirs(valid_dir, exist_ok=True)
os.makedirs(test_dir, exist_ok=True)

# Get a list of all .npy feature files in the input directory
all_files = glob.glob(os.path.join(input_dir, "*.npy"))
print(f"Found {len(all_files)} feature files in the input directory.")

# Shuffle the file list to randomize the split
random.shuffle(all_files)

# Define split ratios: 80% train, 10% valid, 10% test
num_files = len(all_files)
train_split = int(0.8 * num_files)
valid_split = int(0.9 * num_files)  # next 10% for validation; remaining 10% for test

train_files = all_files[:train_split]
valid_files = all_files[train_split:valid_split]
test_files  = all_files[valid_split:]

print(f"Splitting into {len(train_files)} train, {len(valid_files)} validation, and {len(test_files)} test files.")

# Copy the files into their respective directories
for f in train_files:
    shutil.copy(f, os.path.join(train_dir, os.path.basename(f)))
for f in valid_files:
    shutil.copy(f, os.path.join(valid_dir, os.path.basename(f)))
for f in test_files:
    shutil.copy(f, os.path.join(test_dir, os.path.basename(f)))

print("Dataset splitting complete!")
