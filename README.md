# Hand Gesture Volume Controller

A real-time **Hand Gesture Volume Controller** built with Python. The application uses a webcam to detect the user's hand, measures the distance between the thumb and index finger, and converts that gesture into Windows system volume control.

## Features

- Real-time hand detection using MediaPipe
- Thumb and index finger tracking
- Distance calculation using NumPy
- Gesture-based Windows volume control
- Smooth volume transitions
- Volume percentage display
- Visual volume bar
- Active/Inactive gesture status
- No-hand detection message
- Simple webcam-based interface

## Technologies Used

- **Python**
- **OpenCV** – webcam access and image processing
- **MediaPipe** – hand landmark detection
- **NumPy** – distance calculation and value mapping
- **Pycaw** – Windows system audio volume control
- **Comtypes** – Windows COM support used by Pycaw

## How It Works

The controller follows these steps:

1. The webcam captures live video.
2. OpenCV processes each video frame.
3. MediaPipe detects the hand and its landmarks.
4. Landmark **4** (thumb tip) and landmark **8** (index finger tip) are selected.
5. The distance between the two fingertips is calculated.
6. The distance is mapped to a volume percentage.
7. The volume value is smoothed to reduce sudden changes.
8. Pycaw converts the percentage into the Windows audio volume level.
9. The application displays the current status, distance, and volume.

## Project Structure

```text
HandGestureVolumeController/
│
├── main.py
├── README.md
└── requirements.txt
```

## Installation

### 1. Clone or download the project

Open PowerShell or Command Prompt and move into the project folder.

```powershell
cd "C:\Users\91877\Documents\HandGestureVolumeController"
```

### 2. Create a virtual environment (recommended)

```powershell
python -m venv venv
```

Activate it:

```powershell
venv\Scripts\activate
```

### 3. Install dependencies

```powershell
pip install -r requirements.txt
```

## Run the Project

Start the application with:

```powershell
python main.py
```

A webcam window named **Hand Gesture Volume Controller** will open.

### Controls

- Move the **thumb and index finger** to control the volume.
- Keep the fingers within the active gesture range to adjust the volume.
- Press **Q** to close the application.

## Volume Mapping

The project uses calibrated fingertip distances:

```text
Minimum Distance = 30
Maximum Distance = 200
```

The detected distance is converted into a volume value between:

```text
0% ─────────────── 100%
```

A smoothing formula is also used:

```text
current_volume = current_volume × 0.8 + target_volume × 0.2
```

This helps make the volume changes smoother and less sensitive to small hand movements.

## Requirements

- Windows operating system
- Python 3.10+ recommended
- Working webcam
- Working Windows audio output device

## Troubleshooting

### Webcam is not opening

Check that the webcam is available and not being used by another application.

### MediaPipe error involving `mp.solutions`

This project uses:

```text
mediapipe==0.10.21
```

Install the required version with:

```powershell
pip install mediapipe==0.10.21
```

### Pycaw audio error

Make sure the required packages are installed:

```powershell
pip install pycaw comtypes
```

### Permission or environment issues

If packages are installed but Python cannot find them, activate the virtual environment and run:

```powershell
python -m pip install -r requirements.txt
```

## Future Enhancements

Possible future improvements include:

- Support for multiple hand gestures
- Mute/unmute gesture
- Brightness control
- Media play/pause controls
- Previous/next track gestures
- Custom gesture configuration
- Graphical settings interface
- Gesture recognition using machine learning

## Author

**Hand Gesture Volume Controller**

Developed as a Python computer-vision project demonstrating real-time gesture recognition and system-level interaction.
