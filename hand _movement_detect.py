"""
Real-time Hand Gesture Recognition with Voice Output
Detects Like, Dislike, and Hello gestures within 25cm from camera
Uses mediapipe for hand tracking and pyttsx3 for voice output
"""
import cv2
import mediapipe as mp
import math
import pyttsx3
import threading
import time

mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
hands = mp_hands.Hands(
    static_image_mode=False,
    max_num_hands=1,
    min_detection_confidence=0.7,
    min_tracking_confidence=0.7
)

engine = pyttsx3.init()
engine.setProperty('rate', 150)
engine.setProperty('volume', 1.0)

last_gesture = None
last_gesture_time = 0
gesture_cooldown = 1.0
speaking = False

KNOWN_HAND_WIDTH = 9.0  # cm
FOCAL_LENGTH = 600      # pixels (adjust if needed)

def speak_async(text):
    global speaking
    if not speaking:
        speaking = True
        def speak():
            global speaking
            engine.say(text)
            engine.runAndWait()
            speaking = False
        threading.Thread(target=speak).start()

def calculate_distance(hand_width_pixels):
    if hand_width_pixels == 0:
        return float('inf')
    return (KNOWN_HAND_WIDTH * FOCAL_LENGTH) / hand_width_pixels

def get_hand_width(landmarks, image_width):
    wrist = landmarks[0]
    pinky_mcp = landmarks[17]
    return abs(pinky_mcp.x - wrist.x) * image_width

def count_extended_fingers(landmarks):
    tips = [4, 8, 12, 16, 20]
    pips = [2, 6, 10, 14, 18]
    extended = 0
    for tip, pip in zip(tips, pips):
        if tip == 4:
            if abs(landmarks[tip].x - landmarks[0].x) > abs(landmarks[3].x - landmarks[0].x):
                extended += 1
        else:
            if landmarks[tip].y < landmarks[pip].y:
                extended += 1
    return extended

def is_thumb_up(landmarks):
    return (landmarks[4].y < landmarks[3].y) and (count_extended_fingers(landmarks) <= 2)

def is_thumb_down(landmarks):
    return (landmarks[4].y > landmarks[3].y) and (count_extended_fingers(landmarks) <= 2)

def is_open_palm(landmarks):
    return count_extended_fingers(landmarks) >= 4

def recognize_gesture(landmarks):
    if is_thumb_up(landmarks): return "Like"
    elif is_thumb_down(landmarks): return "Dislike"
    elif is_open_palm(landmarks): return "Hello"
    return None

def main():
    global last_gesture, last_gesture_time
    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

    print("Camera started! Show gestures within 25 cm:")
    print("👍like 👎 dislike 👋 hello press 'q' to quit.")

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret: break

        frame = cv2.flip(frame, 1)
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = hands.process(rgb)
        h, w, _ = frame.shape
        gesture_text, distance_text = "No hand detected", ""

        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
                lm = hand_landmarks.landmark
                hand_width = get_hand_width(lm, w)
                distance = calculate_distance(hand_width)
                distance_text = f"Distance: {distance:.1f} cm"

                if distance <= 90:
                    gesture = recognize_gesture(lm)
                    if gesture:
                        gesture_text = f"{gesture} (in range)"
                        now = time.time()
                        if gesture != last_gesture or (now - last_gesture_time) > gesture_cooldown:
                            speak_async(f"{gesture}, {gesture}")
                            last_gesture, last_gesture_time = gesture, now
                    else:
                        gesture_text = "No gesture recognized"
                else:
                    gesture_text = "Hand too far"
                    last_gesture = None

        cv2.putText(frame, gesture_text, (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
        if distance_text:
            cv2.putText(frame, distance_text, (10, 60),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 0), 2)
        cv2.imshow("Gesture Recognition", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
    hands.close()

if __name__ == "__main__":
    main()