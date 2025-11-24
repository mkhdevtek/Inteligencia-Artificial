import cv2
import mediapipe as mp
import numpy as np


mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
hands = mp_hands.Hands(static_image_mode=False, max_num_hands=2, min_detection_confidence=0.5)

cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        break
    frame = cv2.flip(frame, 1)

    height, width, _ = frame.shape
    center_x = width // 2
    center_y = height // 2
    
    # Convertir imagen a RGB (MediaPipe usa RGB)
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(frame_rgb)

    # Variables para guardar coordenadas
    left_index = None
    right_index = None
    right_middle = None
    right_wrist = None

    rectsize = 100
    angle = 0
            
    if results.multi_hand_landmarks and results.multi_handedness:
        for hand_landmarks, handedness in zip(results.multi_hand_landmarks, results.multi_handedness):
            label = handedness.classification[0].label  # 'Left' o 'Right'
            #print(label)
            h, w, _ = frame.shape
            
            # Coordenadas del índice (landmark 8)
            index_tip = hand_landmarks.landmark[8]
            x, y = int(index_tip.x * w), int(index_tip.y * h)

            wrist = hand_landmarks.landmark[0]
            x_w, y_w = int(wrist.x * w), int(wrist.y * h)

            middle_tip = hand_landmarks.landmark[12]
            x_mt, y_mt = int(middle_tip.x * w), int(middle_tip.y * h)
            
            # Guardar según la mano
            if label == 'Left':
                left_index = (x, y)
            elif label == 'Right':
                right_index = (x, y)
                right_middle = (x_mt, y_mt)
                right_wrist = (x_w, y_w)

                angle = np.atan2(y_mt - y_w, x_mt - x_w)
                angle = np.degrees(angle)

            # Dibujar los landmarks (opcional)
            mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

        # Si ambas manos detectadas, dibujar línea entre los dos puntos
        if left_index and right_index:
            #cv2.line(frame, left_index, right_index, (0, 255, 0), 3)

            distancia_indices = np.linalg.norm(np.array(left_index) - np.array(right_index))
            print(f"cx:{center_x}, cy{center_y}")
            print(f"Distancia entre indices: {distancia_indices}")

            #MAXSIZERECT = 0.7
            if distancia_indices != None or distancia_indices > 0:
                rectsize = int(distancia_indices)
                #cv2.rectangle(
                #    frame,
                #    (int(center_x - int(distancia_indices) % width*MAXSIZERECT), int(center_y-int(distancia_indices) % height*MAXSIZERECT)),
                #    (int(center_x + int(distancia_indices) % width*MAXSIZERECT), int(center_y+int(distancia_indices) % height*MAXSIZERECT)),
                #    (99, 99, 99),
                #    3
                #)

            #cv2.rectangle(frame, left_index, right_index, (0, 255, 0), 3)
            cv2.circle(frame, left_index, 8, (255, 0, 0), -1)
            cv2.circle(frame, right_index, 8, (0, 0, 255), -1)

    MAXSIZERECT = 0.6
    if right_wrist and right_middle:
        rotated_rect = ((center_x, center_y), (int(rectsize * MAXSIZERECT), int(rectsize * MAXSIZERECT)), angle*4)

        box_points = cv2.boxPoints(rotated_rect)
        box_points = np.intp(box_points)

        cv2.putText(frame, f'Angulo', (center_x, center_y-45), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (100, 200, 0), 2, cv2.LINE_AA)
        cv2.putText(frame, f'({angle:.2f})', (center_x - 45, center_y), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (100, 200, 0), 2, cv2.LINE_AA)
        cv2.drawContours(frame, [box_points], 0, (100, 200, 0), 3)

    cv2.imshow("Line", frame)

    if cv2.waitKey(1) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()
