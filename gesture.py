import cv2
import mediapipe as mp
import math
import pyautogui
from pycaw.pycaw import AudioUtilities
import time


mp_hands = mp.solutions.hands
mp_draw = mp.solutions.drawing_utils

hands = mp_hands.Hands(
    static_image_mode=False,
    max_num_hands=1,
    model_complexity=1,
    min_detection_confidence=0.7,
    min_tracking_confidence=0.7
)


endpoint_volume = AudioUtilities.GetSpeakers().EndpointVolume


gesture = "None"
status = "No Hand"
frame_count = 0
action_every_n_frames = 6
pTime = 0   


def process_frame(frame):
    global gesture, status, frame_count, pTime

    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    result = hands.process(rgb)

    if result.multi_hand_landmarks:
        status = "Hand Detected"

        for hand_landmarks in result.multi_hand_landmarks:

            
            mp_draw.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

            h, w, _ = frame.shape

            thumb = hand_landmarks.landmark[4]
            index = hand_landmarks.landmark[8]

            x1, y1 = int(thumb.x * w), int(thumb.y * h)
            x2, y2 = int(index.x * w), int(index.y * h)

            distance = math.hypot(x2 - x1, y2 - y1)
            
            vol = int((distance - 45) * 100 / (80 - 45))
            vol = max(0, min(100, vol))


            bar_x = w-60
            bar_y = 100


            bar_height = int((100 - vol) * 2)


            cv2.rectangle(frame, (bar_x, bar_y), (bar_x + 30, bar_y + 200), (255, 0, 0), 2)


            cv2.rectangle(frame, (bar_x, bar_y + bar_height), (bar_x + 30, bar_y + 200), (255, 0, 0), -1)


            cv2.putText(frame, f'{vol} %', (bar_x, bar_y + 230),
            cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 0, 0), 2)

            frame_count += 1

            if distance < 45:
                gesture = "VOLUME DOWN"
                if frame_count % action_every_n_frames == 0:
                    pyautogui.press("volumedown")

            elif distance > 80:
                gesture = "VOLUME UP"
                if frame_count % action_every_n_frames == 0:
                    pyautogui.press("volumeup")

            else:
                gesture = "HOLD"

            
            cv2.circle(frame, (x1, y1), 8, (0, 255, 0), -1)
            cv2.circle(frame, (x2, y2), 8, (0, 255, 0), -1)
            cv2.line(frame, (x1, y1), (x2, y2), (255, 0, 0), 2)

    else:
        status = "No Hand"
        gesture = "None"

   
    cTime = time.time()

    if pTime == 0:
        fps = 0
    else:
        fps = 1 / (cTime - pTime)

    pTime = cTime

    h, w, _ = frame.shape


    cv2.putText(frame, f'FPS: {int(fps)}', (w - 150, 30),
            cv2.FONT_HERSHEY_SIMPLEX, 1,
            (255, 0, 0), 2)


    cv2.putText(frame, gesture, (w - 250, 70),
            cv2.FONT_HERSHEY_SIMPLEX, 1,
            (0, 255, 0), 2)
    return frame
