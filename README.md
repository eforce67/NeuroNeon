# NeuroNeon

NeuroNeon is an open-source project that uses Ultralytics' YoloV8 to explore convolutional neural networks (CNNs) through Brawl Stars gameplay. It runs on the Null Brawl private server to follow Supercell's rules against bots in multiplayer. **Use at your own risk—I’m not responsible for any account bans.**

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

## How It Works

NeuroNeon uses YoloV8 for single-class classification to decide the best actions based on what it "sees" on the screen. This method focuses on understanding the content of images rather than just identifying objects, inspired by [subwAI](https://github.com/nikp06/subwAI).

## AI Model Limitations

- **No Manual Aim Control:** The bot can't precisely control aim and is limited to basic mouse movements. This reduces its ability to respond accurately in real-time situations.

- **Button Spamming:** The bot only spams buttons instead of making thoughtful decisions. This can lead to less effective gameplay, especially in complex or high-pressure situations.

- **Fixed-Time Controls:** The bot's actions are based on fixed timing, which can be a problem in situations where timing is important. Adding more output options for movement duration could help.

- **No Memory:** The bot can't remember previous images it has seen, so it can't keep track of where enemies have moved.

- **Single Image Classification:** The bot makes only one decision per frame. While this works, multi-label classification could allow it to make several decisions at once, improving gameplay by pressing multiple buttons per frame.

## Data Collection

Data is automatically collected each frame when running `data_collection.py`. The bot captures images whenever a key is pressed, syncing your actions with the game frames in near real-time.

## Training YoloV8

To train your YoloV8 models, check out these resources from Ultralytics:

- [Datasets for Classification](https://docs.ultralytics.com/datasets/classify/): How to set up and organize datasets for classification.
- [Classification Tasks](https://docs.ultralytics.com/tasks/classify/): How to configure and run classification tasks with YoloV8.

For visual help, watch this video: [How to Train YoloV8](https://youtu.be/9a1oRKIi104?si=Dj-Y7qqrMbes8Fq6).

## Custom Outputs

You can create your own output labels by organizing your datasets into folders. `data_collection.py` will build your dataset, which you can tweak and modify as needed.

## Questions?

If you have any questions, post them in the Issues tab!