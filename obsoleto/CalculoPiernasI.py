import cv2
import mediapipe as mp
import math
import numpy as np

class AutoDocMovimiento:
    def __init__(self):
        self.mp_pose = mp.solutions.pose
        self.mp_drawing = mp.solutions.drawing_utils
        self.pose = self.mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5)

    def procesar_imagen(self, image_buffer):
        # Decodifica la imagen desde el buffer
        nparr = np.frombuffer(image_buffer, np.uint8)
        image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        
        # Redimensiona la imagen para que sea más pequeña
        scale_percent = 50  # Cambia este porcentaje para ajustar el tamaño
        width = int(image.shape[1] * scale_percent / 100)
        height = int(image.shape[0] * scale_percent / 100)
        dim = (width, height)
        image = cv2.resize(image, dim, interpolation=cv2.INTER_AREA)

        # Convierte la imagen a RGB
        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        # Procesa la imagen para detectar la pose
        results = self.pose.process(image_rgb)

        # Si se detecta la pose, dibuja landmarks y conectores
        if results.pose_landmarks:
            # Coordenadas de los puntos relevantes
            landmarks = results.pose_landmarks.landmark
            h, w, _ = image.shape

            puntos = {
                "cadera_izquierda": (int(landmarks[self.mp_pose.PoseLandmark.LEFT_HIP].x * w), int(landmarks[self.mp_pose.PoseLandmark.LEFT_HIP].y * h)),
                "cadera_derecha": (int(landmarks[self.mp_pose.PoseLandmark.RIGHT_HIP].x * w), int(landmarks[self.mp_pose.PoseLandmark.RIGHT_HIP].y * h)),
                "rodilla_izquierda": (int(landmarks[self.mp_pose.PoseLandmark.LEFT_KNEE].x * w), int(landmarks[self.mp_pose.PoseLandmark.LEFT_KNEE].y * h)),
                "rodilla_derecha": (int(landmarks[self.mp_pose.PoseLandmark.RIGHT_KNEE].x * w), int(landmarks[self.mp_pose.PoseLandmark.RIGHT_KNEE].y * h)),
                "tobillo_izquierdo": (int(landmarks[self.mp_pose.PoseLandmark.LEFT_ANKLE].x * w), int(landmarks[self.mp_pose.PoseLandmark.LEFT_ANKLE].y * h)),
                "tobillo_derecho": (int(landmarks[self.mp_pose.PoseLandmark.RIGHT_ANKLE].x * w), int(landmarks[self.mp_pose.PoseLandmark.RIGHT_ANKLE].y * h))
            }

            # Dibuja los landmarks específicos
            cv2.circle(image, puntos["cadera_izquierda"], 5, (0, 0, 255), cv2.FILLED)  # Rojo para la cintura
            cv2.circle(image, puntos["cadera_derecha"], 5, (0, 0, 255), cv2.FILLED)  # Rojo para la cintura
            cv2.circle(image, puntos["rodilla_izquierda"], 5, (0, 255, 0), cv2.FILLED)  # Verde para las rodillas
            cv2.circle(image, puntos["rodilla_derecha"], 5, (0, 255, 0), cv2.FILLED)  # Verde para las rodillas
            cv2.circle(image, puntos["tobillo_izquierdo"], 5, (255, 0, 0), cv2.FILLED)  # Azul para los tobillos
            cv2.circle(image, puntos["tobillo_derecho"], 5, (255, 0, 0), cv2.FILLED)  # Azul para los tobillos

            # Dibuja líneas moradas
            cv2.line(image, puntos["cadera_izquierda"], puntos["cadera_derecha"], (255, 0, 255), 2)
            cv2.line(image, puntos["cadera_izquierda"], puntos["rodilla_izquierda"], (255, 0, 255), 2)
            cv2.line(image, puntos["rodilla_izquierda"], puntos["tobillo_izquierdo"], (255, 0, 255), 2)
            cv2.line(image, puntos["cadera_derecha"], puntos["rodilla_derecha"], (255, 0, 255), 2)
            cv2.line(image, puntos["rodilla_derecha"], puntos["tobillo_derecho"], (255, 0, 255), 2)

        # Codifica la imagen procesada a un buffer
        _, buffer = cv2.imencode('.jpg', image)
        return buffer.tobytes()

