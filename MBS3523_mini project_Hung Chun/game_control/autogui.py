import cv2
import mediapipe as mp
import pyautogui

# Initialize Mediapipe hand detection
mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands

# Open camera stream
cap = cv2.VideoCapture(0)
FPS = 30
with mp_hands.Hands(
    static_image_mode=False,
    max_num_hands=1,
    min_detection_confidence=0.5) as hands:

    while cap.isOpened():
        # Read camera stream
        ret, frame = cap.read()
        if not ret:
            break

        # Flip image horizontally
        frame = cv2.flip(frame, 1)

        # Convert image to RGB format
        image_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Detect hands
        results = hands.process(image_rgb)

        # Draw hand landmarks and connections
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                mp_drawing.draw_landmarks(
                    frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

                # Get hand landmarks coordinates
                for idx, landmark in enumerate(hand_landmarks.landmark):
                    if idx == 8:
                        image_height, image_width, _ = frame.shape
                        x, y = int(landmark.x * image_width), int(landmark.y * image_height)

                        if y < 0.5 * image_height:
                            position = "U"
                            pyautogui.keyDown('up')
                        else:
                            position = "M"
                            pyautogui.keyUp('up')

                        # Display coordinates and position
                        cv2.putText(frame, f'MOVE: ({x}, {y}) {position}', (10, 20),
                                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1, cv2.LINE_AA)

        # Show mirrored image
        cv2.imshow('Mirror Hand Tracking', frame)

        if cv2.waitKey(10) & 0xFF == ord('q'):
            break

# Release resources
cap.release()
cv2.destroyAllWindows()