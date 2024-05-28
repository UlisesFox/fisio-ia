import cv2
import mediapipe as mp
import math
import numpy as np

class AutoDocPostura:
    def __init__(self):
        self.mp_pose = mp.solutions.pose
        self.pose = self.mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5)

    def calcular_angulo(self, puntoA, puntoB, puntoC):
        # Vectores BA y BC
        BA = (puntoA[0] - puntoB[0], puntoA[1] - puntoB[1])
        BC = (puntoC[0] - puntoB[0], puntoC[1] - puntoB[1])
        
        # Producto escalar y magnitudes de los vectores
        dot_product = BA[0] * BC[0] + BA[1] * BC[1]
        magnitude_BA = math.sqrt(BA[0]**2 + BA[1]**2)
        magnitude_BC = math.sqrt(BC[0]**2 + BC[1]**2)
        
        # Ángulo en radianes
        angle_radians = math.acos(dot_product / (magnitude_BA * magnitude_BC))
        
        # Convierte a grados
        angle_degrees = math.degrees(angle_radians)
        
        return angle_degrees

    def procesar_imagen(self, image_buffer):
        # Decodifica la imagen desde el buffer
        nparr = np.frombuffer(image_buffer, np.uint8)
        image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

        # Convierte la imagen a RGB
        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        # Procesa la imagen para detectar la pose
        results = self.pose.process(image_rgb)

        # Si se detecta la pose, calcula el ángulo de curvatura
        if results.pose_landmarks:
            # Coordenadas de los puntos relevantes
            landmarks = results.pose_landmarks.landmark
            h, w, _ = image.shape

            puntos = {
                "nariz": (int(landmarks[self.mp_pose.PoseLandmark.NOSE].x * w), int(landmarks[self.mp_pose.PoseLandmark.NOSE].y * h)),
                "hombro_izquierdo": (int(landmarks[self.mp_pose.PoseLandmark.LEFT_SHOULDER].x * w), int(landmarks[self.mp_pose.PoseLandmark.LEFT_SHOULDER].y * h)),
                "hombro_derecho": (int(landmarks[self.mp_pose.PoseLandmark.RIGHT_SHOULDER].x * w), int(landmarks[self.mp_pose.PoseLandmark.RIGHT_SHOULDER].y * h)),
                "cadera_izquierda": (int(landmarks[self.mp_pose.PoseLandmark.LEFT_HIP].x * w), int(landmarks[self.mp_pose.PoseLandmark.LEFT_HIP].y * h)),
                "cadera_derecha": (int(landmarks[self.mp_pose.PoseLandmark.RIGHT_HIP].x * w), int(landmarks[self.mp_pose.PoseLandmark.RIGHT_HIP].y * h))
            }

            # Coordenadas de los puntos relevantes para el ángulo
            A = puntos["nariz"]
            B = ((puntos["hombro_izquierdo"][0] + puntos["hombro_derecho"][0]) // 2, (puntos["hombro_izquierdo"][1] + puntos["hombro_derecho"][1]) // 2)
            C = ((puntos["cadera_izquierda"][0] + puntos["cadera_derecha"][0]) // 2, (puntos["cadera_izquierda"][1] + puntos["cadera_derecha"][1]) // 2)

            # Calcula el ángulo
            angulo_curvatura = self.calcular_angulo(A, B, C)
            return angulo_curvatura

        return None
