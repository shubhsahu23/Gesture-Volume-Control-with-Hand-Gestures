Gesture Volume Control with Hand Gestures

📌 Description

This project controls system volume using hand gestures through a webcam. It uses computer vision techniques to detect hand movements and adjust volume in real time.

🛠 Technologies Used

- Python
- OpenCV
- MediaPipe
- Flask
- Pycaw
- PyAutoGUI

⚙️ How it Works

- Webcam captures live video
- MediaPipe detects hand landmarks
- Distance between thumb and index finger is calculated
- Volume up/down key events are triggered based on finger distance
- Current system volume is fetched for display

▶️ Run Project

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Run the application:
   ```bash
   python app.py
   ```

3. Open browser:
   ```
   http://127.0.0.1:5000
   ```

4. Platform note:
   This app uses `pycaw` and `pyautogui` for system volume behavior and is intended for Windows.

🎯 Features

- Real-time gesture-based volume control
- Live webcam preview
- Horizontal & vertical volume indicators
- Start/Stop control buttons