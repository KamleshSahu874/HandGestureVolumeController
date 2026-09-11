import cv2
import mediapipe as mp
import numpy as np

from pycaw.pycaw import AudioUtilities


# =========================
# Initialize Webcam
# =========================

cap = cv2.VideoCapture(0)

cap.set(3, 1280)
cap.set(4, 720)


# =========================
# Initialize MediaPipe
# =========================

mp_hands = mp.solutions.hands

hands = mp_hands.Hands(
    static_image_mode=False,
    max_num_hands=1,
    min_detection_confidence=0.7,
    min_tracking_confidence=0.7
)

mp_draw = mp.solutions.drawing_utils


# =========================
# Initialize Pycaw
# =========================

devices = AudioUtilities.GetSpeakers()

volume_control = devices.EndpointVolume

volume_range = volume_control.GetVolumeRange()

min_volume = volume_range[0]
max_volume = volume_range[1]


# =========================
# Volume Settings
# =========================

MIN_DISTANCE = 30
MAX_DISTANCE = 200

current_volume = 0


# =========================
# Main Loop
# =========================

while True:

    success, frame = cap.read()

    if not success:
        print("Failed to access webcam")
        break

    # Flip webcam
    frame = cv2.flip(frame, 1)

    # Frame dimensions
    h, w, c = frame.shape

    # Convert BGR → RGB
    rgb_frame = cv2.cvtColor(
        frame,
        cv2.COLOR_BGR2RGB
    )

    # Detect hand
    results = hands.process(rgb_frame)


    # =========================
    # Hand Detected
    # =========================

    if results.multi_hand_landmarks:

        for hand_landmarks in results.multi_hand_landmarks:

            # Draw hand landmarks
            mp_draw.draw_landmarks(
                frame,
                hand_landmarks,
                mp_hands.HAND_CONNECTIONS
            )


            # =========================
            # Get Thumb & Index
            # =========================

            thumb = hand_landmarks.landmark[4]
            index = hand_landmarks.landmark[8]


            # Convert coordinates
            thumb_x = int(thumb.x * w)
            thumb_y = int(thumb.y * h)

            index_x = int(index.x * w)
            index_y = int(index.y * h)


            # =========================
            # Calculate Distance
            # =========================

            distance = np.linalg.norm(
                np.array([thumb_x, thumb_y])
                -
                np.array([index_x, index_y])
            )


            # =========================
            # Draw Finger Points
            # =========================

            cv2.circle(
                frame,
                (thumb_x, thumb_y),
                12,
                (255, 0, 0),
                cv2.FILLED
            )

            cv2.circle(
                frame,
                (index_x, index_y),
                12,
                (0, 255, 0),
                cv2.FILLED
            )


            # Draw connecting line
            cv2.line(
                frame,
                (thumb_x, thumb_y),
                (index_x, index_y),
                (255, 255, 255),
                3
            )


            # =========================
            # Controller Activation
            # =========================

            # Controller is active when
            # thumb and index are reasonably close

            if distance <= 80:

                status = "ACTIVE"

                status_color = (0, 255, 0)


                # Convert distance → volume
                target_volume = np.interp(
                    distance,
                    [MIN_DISTANCE, MAX_DISTANCE],
                    [0, 100]
                )

                target_volume = np.clip(
                    target_volume,
                    0,
                    100
                )


                # Smooth volume
                current_volume = (
                    current_volume * 0.8
                    +
                    target_volume * 0.2
                )


                # Convert percentage → Pycaw
                volume_level = np.interp(
                    current_volume,
                    [0, 100],
                    [min_volume, max_volume]
                )


                # Set Windows volume
                volume_control.SetMasterVolumeLevel(
                    volume_level,
                    None
                )

            else:

                status = "INACTIVE"

                status_color = (0, 0, 255)


            # =========================
            # Volume Bar
            # =========================

            bar_x = 50
            bar_y = 150

            bar_width = 40
            bar_height = 400


            # Background
            cv2.rectangle(
                frame,
                (bar_x, bar_y),
                (
                    bar_x + bar_width,
                    bar_y + bar_height
                ),
                (80, 80, 80),
                -1
            )


            # Filled height
            filled_height = int(
                (current_volume / 100)
                * bar_height
            )


            # Volume level
            cv2.rectangle(
                frame,
                (
                    bar_x,
                    bar_y + bar_height - filled_height
                ),
                (
                    bar_x + bar_width,
                    bar_y + bar_height
                ),
                (0, 255, 0),
                -1
            )


            # =========================
            # Display Status
            # =========================

            cv2.putText(
                frame,
                f"STATUS: {status}",
                (20, 50),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.9,
                status_color,
                2
            )


            # =========================
            # Display Distance
            # =========================

            cv2.putText(
                frame,
                f"Distance: {int(distance)}",
                (20, 90),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.7,
                (255, 255, 255),
                2
            )


            # =========================
            # Display Volume
            # =========================

            cv2.putText(
                frame,
                f"Volume: {int(current_volume)}%",
                (20, 590),
                cv2.FONT_HERSHEY_SIMPLEX,
                1,
                (255, 255, 255),
                2
            )


            # =========================
            # Display Title
            # =========================

            cv2.putText(
                frame,
                "HAND GESTURE VOLUME CONTROLLER",
                (350, 50),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.9,
                (255, 255, 255),
                2
            )


    else:

        # No hand detected
        cv2.putText(
            frame,
            "NO HAND DETECTED",
            (20, 50),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.9,
            (0, 0, 255),
            2
        )


    # =========================
    # Display Webcam
    # =========================

    cv2.imshow(
        "Hand Gesture Volume Controller",
        frame
    )


    # =========================
    # Quit
    # =========================

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break


# =========================
# Cleanup
# =========================

cap.release()
cv2.destroyAllWindows()