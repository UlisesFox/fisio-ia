import mediapipe as mp
import cv2
import math

# Inicializa el modelo específico
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils  

# Configura la captura de vídeo
cap = cv2.VideoCapture(0)

# Inicializa el modelo
with mp_hands.Hands(min_detection_confidence=0.5, min_tracking_confidence=0.5) as hands:
    while cap.isOpened():
        # Lee un frame de la cámara
        success, image = cap.read()
        if not success:
            print("No se puede leer el frame de la cámara")
            break

        # Convierte la imagen a RGB
        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

        # Procesa la imagen para detectar manos
        results = hands.process(image_rgb)

        # Si se detectan manos, dibuja puntos y conectores
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                # Dibuja los puntos de la mano
                mp_drawing.draw_landmarks(image, hand_landmarks, mp_hands.HAND_CONNECTIONS)
                
                # Calcula la puntos de la mano
                wrist = hand_landmarks.landmark[mp_hands.HandLandmark.WRIST]
                index_finger = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]
                angle = math.degrees(math.atan2(index_finger.y - wrist.y, index_finger.x - wrist.x))

        # Muestra el resultado
        cv2.imshow('MediaPipe Hands', image)

        # Si se presiona 'q', sal del bucle
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

# Libera recursos
cap.release()
cv2.destroyAllWindows()
