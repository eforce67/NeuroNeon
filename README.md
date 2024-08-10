# NeuroNeon

NeuroNeon is an open-source project that uses Ultralytics' YoloV8 to explore convolutional neural networks (CNNs) through Brawl Stars gameplay. It runs on the Null Brawl private server to follow Supercell's rules against bots in multiplayer. **Use at your own risk—I’m not responsible for any account bans.**

## How It Works

NeuroNeon learns to play the game by watching you play. The AI observes your gameplay, capturing your strategies, movements, and decision-making process. Over time, it starts to mimic your playstyle, making it a unique and personalized AI.

Rest assured, collecting the image data is straightforward. You only need about 100 matches in Brawl Stars to gather enough data for the model to start learning. The more you play, the better it understands your style. However, keep in mind that the AI is only as good as the data it learns from—if you make mistakes, so will it.

Currently, NeuroNeon is designed to play with two specific Brawlers: Jacky and Doug. These Brawlers require no aiming skill, making them perfect candidates for this AI. While the model can learn to play decently, the limitations do pose some challenges, which are outlined below.

## Installation

### Requirements
- Python 3.9+
- LDPlayer emulator
- Windows 10
- Decent GPU or CPU

### Python Libraries
```bash
pip install pywin32 numpy opencv-python pynput ultralytics
```

### PyTorch Installation
With GPU support:
```bash
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
```
CPU only:
```bash
pip install torch torchvision torchaudio
```

## AI Model Limitations

- **No Manual Aim Control:** The bot can't precisely control aim and is limited to basic mouse movements. This reduces its ability to respond accurately in real-time situations.
  
- **Button Spamming:** The bot only spams buttons instead of making thoughtful decisions. This can lead to less effective gameplay, especially in complex or high-pressure situations.

- **Fixed-Time Controls:** The bot's actions are based on fixed timing, which can be a problem in situations where timing is important. Adding more output options for movement duration could help.

- **No Memory:** The bot can't remember previous images it has seen, so it can't keep track of where enemies have moved.

- **Single Image Classification:** The bot makes only one decision per frame. While this works, multi-label classification could allow it to make several decisions at once, improving gameplay by pressing multiple buttons per frame. Additionally, you can try to overcome this problem by having multiple models predict an outcome for different tasks like attacking or dodging.

## Data Collection

Data is automatically collected in each frame when running `data_collection.py`. The bot captures images whenever a key is pressed, syncing your actions with the game frames in near real-time.

## Training YoloV8

For optimal performance, it’s recommended to use `Yolov8m-cls`, which is the medium classification model for YoloV8. It strikes a good balance between speed and accuracy and runs fast on most devices.

To train your YoloV8 models, check out these resources from Ultralytics:

- [Datasets for Classification](https://docs.ultralytics.com/datasets/classify/): How to set up and organize datasets for classification.
- [Classification Tasks](https://docs.ultralytics.com/tasks/classify/): How to configure and run classification tasks with YoloV8.

For visual help, watch this video: [How to Train YoloV8](https://youtu.be/9a1oRKIi104?si=Dj-Y7qqrMbes8Fq6).

## Custom Outputs

You can create your output labels by organizing your datasets into folders. `data_collection.py` will build your dataset, which you can tweak and modify as needed.

## Questions?

If you have any questions, post them in the Issues tab!