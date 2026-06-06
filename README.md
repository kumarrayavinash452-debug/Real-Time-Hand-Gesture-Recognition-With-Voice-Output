# Real-Time Hand Gesture Recognition with Voice Output

A computer vision project that recognizes hand gestures in real time using a webcam and provides voice feedback. The system detects **Like 👍**, **Dislike 👎**, and **Hello 👋** gestures using MediaPipe hand tracking and converts the recognized gesture into speech using a text-to-speech engine.

## Features

* Real-time hand gesture recognition
* Detects:

  * 👍 Like
  * 👎 Dislike
  * 👋 Hello
* Voice output for recognized gestures
* Hand distance estimation from the camera
* Gesture cooldown system to prevent repeated voice announcements
* Live visualization of hand landmarks
* Works with a standard webcam

## Technologies Used

* Python
* OpenCV
* MediaPipe
* pyttsx3 (Text-to-Speech)
* Threading

## Project Workflow

1. Capture video from webcam.
2. Detect hand landmarks using MediaPipe.
3. Estimate hand distance from the camera.
4. Identify gesture based on finger positions.
5. Convert detected gesture into speech.
6. Display gesture and distance information on screen.

## Supported Gestures

| Gesture    | Description |
| ---------- | ----------- |
| 👍 Like    | Thumb Up    |
| 👎 Dislike | Thumb Down  |
| 👋 Hello   | Open Palm   |

## Installation

### Clone the Repository

git clone https://github.com/kumarrayavinash452-debug/Real-Time-Hand-Gesture-Recognition-With-Voice-Output.git

cd Real-Time-Hand-Gesture-Recognition-With-Voice-Output

### Install Dependencies

```bash
pip install opencv-python mediapipe pyttsx3
```

## Run the Project
hand_movement_detect.py


## Controls

| Key | Action           |
| --- | ---------------- |
| Q   | Quit Application |

## Project Structure

```text
├── hand_movement_detect.py

## Future Improvements

* Add more hand gestures
* Support multiple hands
* Improve gesture accuracy using machine learning
* Add gesture-based system control
* Create a graphical user interface (GUI)
* Support multiple languages for voice output

## Applications

* Human-Computer Interaction (HCI)
* Smart Home Control
* Accessibility Systems
* Touchless Interfaces
* Educational Projects
* AI and Computer Vision Research

## Output Example

```text
Camera started!
Show gestures within range:

👍 Like
👎 Dislike
👋 Hello

Voice Output:
"Like, Like"
"Dislike, Dislike"
"Hello, Hello"
```

## Author

Avinash kumar Ray


##Branch

Artificial Intteligence and Machine Learning

-->> If you found this project useful, please consider giving it a star on GitHub.
