import os
import random
import shutil

import yaml

# Load configuration
with open('resources/config.yaml', 'r') as f:
    config = yaml.safe_load(f)

def move_subset_to_test(dataset_path, train_folder, test_folder, percentage):
    train_path = os.path.join(dataset_path, train_folder)
    test_path = os.path.join(dataset_path, test_folder)

    # Create the test folder if it doesn't exist
    os.makedirs(test_path, exist_ok=True)

    # Iterate through each subfolder in the train folder
    for subfolder in os.listdir(train_path):
        subfolder_train_path = os.path.join(train_path, subfolder)
        subfolder_test_path = os.path.join(test_path, subfolder)

        # Skip if not a directory
        if not os.path.isdir(subfolder_train_path):
            continue

        # Create corresponding subfolder in test directory
        os.makedirs(subfolder_test_path, exist_ok=True)

        # Get list of files in the subfolder
        files = [f for f in os.listdir(subfolder_train_path) if os.path.isfile(os.path.join(subfolder_train_path, f))]

        # Calculate number of files to move
        num_files_to_move = int(len(files) * percentage)

        # Randomly select files to move
        files_to_move = random.sample(files, num_files_to_move)

        # Move the selected files
        for file in files_to_move:
            src = os.path.join(subfolder_train_path, file)
            dst = os.path.join(subfolder_test_path, file)
            shutil.move(src, dst)
            print(f"Moved {file} from {subfolder} to test folder")

        print(f"Moved {num_files_to_move} files from {subfolder} to test")

# Set the paths and parameters
dataset_path = config.get('dataset_path', 'dataset')
train_folder = config.get('train_folder', 'train')
test_folder = config.get('test_folder', 'test')
percentage = config['percent']/100 # 12% generally recommended

# Run the function
move_subset_to_test(dataset_path, train_folder, test_folder, percentage)
