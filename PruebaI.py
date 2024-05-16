import mediapipe as mp
import cv2
import math

# Inicializa el modelo específico
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils  

# Lee la imagen desde el disco
image = cv2.imread("brazo.jpeg")  # Reemplaza "ruta/a/tu/imagen.jpg" con la ruta de tu imagen

# Convierte la imagen a RGB
image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

# Inicializa el modelo de seguimiento de manos
with mp_hands.Hands(min_detection_confidence=0.5, min_tracking_confidence=0.5) as hands:

    # Procesa la imagen para detectar manos
    results = hands.process(image_rgb)

    # Si se detectan manos, dibuja landmarks y conectores
    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            # Dibuja los landmarks de la mano con puntos rojos y líneas verdes
            mp_drawing.draw_landmarks(image, hand_landmarks, mp_hands.HAND_CONNECTIONS, landmark_drawing_spec=mp_drawing.DrawingSpec(color=(0, 0, 255), thickness=2, circle_radius=4), connection_drawing_spec=mp_drawing.DrawingSpec(color=(0, 255, 0), thickness=2))

            # Calcula la inclinación de la mano
            wrist = hand_landmarks.landmark[mp_hands.HandLandmark.WRIST]
            index_finger = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]
            angle = math.degrees(math.atan2(index_finger.y - wrist.y, index_finger.x - wrist.x))

            cv2.putText(image, f'Angle: {int(angle)}', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)


    # Muestra el resultado
    cv2.imshow('MediaPipe Hands', image)
    cv2.waitKey(0)  # Espera hasta que se presione una tecla

# Cierra la ventana
cv2.destroyAllWindows()
