import os

import torch
import yaml
from ultralytics import YOLO

# Load configuration file
with open('resources/config.yaml', 'r') as f:
    config = yaml.safe_load(f)

# Initialize YOLO model
model = YOLO('yolov8m-cls.pt', task='classify')

# Set device for training
num_of_gpus = [x for x in range(config['num_of_available_gpus'])]
device = num_of_gpus if torch.cuda.is_available() and config['num_of_available_gpus'] > 0 else 'cpu'
model.to(device)

if device == 'cpu':
    print('There are no GPUs available on your device. You are training on CPU. If this is not intended, please exit the script.')

# Verify and set the dataset path
dataset_path = config['save_dir']
if not os.path.exists(dataset_path):
    raise ValueError(f"Dataset path {dataset_path} does not exist")
elif not os.path.exists(f'{dataset_path}/test'):
    raise ValueError(f"Dataset path folder 'test' does not exist. Test set is required for evaluating your model.")
elif not os.path.exists(f'{dataset_path}/train'):
    raise ValueError(f"Dataset path folder 'train' does not exist. Train set is required for training your model.")

# Train the model with parameters from config
results = model.train(
    data=dataset_path,
    epochs=config.get('epochs', 1000),
    imgsz=config.get('imgsz', 320),
    device=device,
    patience=config.get('patience', 50),
    batch=config.get('batch', 32),
    plots=config.get('plots', True)
)
""
# Export the model
model.export(format='onnx')  # Use 'onnx' for compatibility with various platforms
