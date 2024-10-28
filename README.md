# Raspberry Pi 5 Facial Recognition and Tracking Door Access System

This project is a smart door access system based on Raspberry Pi 5, using OpenCV for facial recognition and tracking. It adjusts the camera angle through a servo motor to track faces in real time and provides voice feedback for a more user-friendly experience.

## Features
- **Facial Recognition and Tracking**: Detects faces in real time, recognizes registered users, and opens the door automatically.
- **Servo Control**: Adjusts the camera angle based on face position, keeping the face centered in the frame.
- **Voice Feedback**: Welcomes known users and prompts unknown users, with the option to add new faces.
- **Automatic Door Control**: Operates door lock through servo or relay module upon face recognition.

## Hardware Requirements
- Raspberry Pi 5
- PiCamera module
- Servo motor (for camera adjustment)
- Relay module (optional, for door control)
- Speaker (for voice feedback)

## Software Requirements
- Python 3
- OpenCV
- Picamera2
- RPi.GPIO library
- Additional dependencies listed in `requirements.txt`

## Installation and Setup
1. Clone this repository:
   ```bash
   git clone https://github.com/yourusername/Face-Recognition-Door-Access-System.git
   cd Face-Recognition-Door-Access-System

2. Install dependencies:
    pip install -r requirements.txt

3. Ensure camera and servo motor are connected correctly.

4. Run 
    sudo python3 main.py 
    to start the system.

## Code Structure
main.py: The main program file that controls initialization and main logic.
cam_tracking.py: Face tracking and servo control module, adjusting the camera based on face location.
fac_recognition.py: Facial recognition module for loading known faces and detecting faces in the camera feed.
ser_control.py: Servo control module to adjust the camera angle based on detected face position.
aud_speaking.py: Voice feedback module for recognition announcements and new user prompts.
rel_control.py: Relay control module to manage door lock operation.

## Usage
Start the System: Run sudo python3 main.py to activate facial recognition and tracking.
Add New User: When prompted as an "Unknown User," press a and enter the new user's name to add their face to the system.
Door Control: The system opens the door when a known user is detected and automatically locks after a delay.

## Contributing
Issues and contributions are welcome! Feel free to open pull requests for improvements.