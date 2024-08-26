import cv2
import mediapipe as mp
import math
import numpy as np

class AutoDocMovimiento:
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

        if angle_degrees >= 80:
            angle_degrees_filter=angle_degrees-80
        elif angle_degrees <= 79:
            angle_degrees_filter=angle_degrees+281
        
        return round(angle_degrees_filter)
    
    def calcular_angulo2(self, puntoA, puntoB, puntoC):
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

        if angle_degrees >= 80:
            angle_degrees_filter=angle_degrees-80
        elif angle_degrees <= 79:
            angle_degrees_filter=angle_degrees+281
        
        return round(angle_degrees_filter)

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

        # Si se detecta la pose, calcula el ángulo de curvatura
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

            # Coordenadas de los puntos relevantes para el ángulo
            A = puntos["cadera_izquierda"]
            B = puntos["rodilla_izquierda"]
            C = puntos["tobillo_izquierdo"]

            D = puntos["cadera_derecha"]
            E = puntos["rodilla_derecha"]
            F = puntos["tobillo_derecho"]

            # Calcula el ángulo
            angulo_curvatura = self.calcular_angulo(A, B, C)
            angulo_curvatura2 = self.calcular_angulo2(D, E, F)
            return angulo_curvatura, angulo_curvatura2

        return None
