import cv2
import mediapipe as mp
import math
import numpy as np

class AutoDocPostura:
    def __init__(self):
        self.mp_pose = mp.solutions.pose
        self.mp_drawing = mp.solutions.drawing_utils
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
                "nariz": (int(landmarks[self.mp_pose.PoseLandmark.NOSE].x * w), int(landmarks[self.mp_pose.PoseLandmark.NOSE].y * h)),
                "hombro_izquierdo": (int(landmarks[self.mp_pose.PoseLandmark.LEFT_SHOULDER].x * w), int(landmarks[self.mp_pose.PoseLandmark.LEFT_SHOULDER].y * h)),
                "hombro_derecho": (int(landmarks[self.mp_pose.PoseLandmark.RIGHT_SHOULDER].x * w), int(landmarks[self.mp_pose.PoseLandmark.RIGHT_SHOULDER].y * h)),
                "cadera_izquierda": (int(landmarks[self.mp_pose.PoseLandmark.LEFT_HIP].x * w), int(landmarks[self.mp_pose.PoseLandmark.LEFT_HIP].y * h)),
                "cadera_derecha": (int(landmarks[self.mp_pose.PoseLandmark.RIGHT_HIP].x * w), int(landmarks[self.mp_pose.PoseLandmark.RIGHT_HIP].y * h))
            }

            # Dibuja los landmarks específicos
            cv2.circle(image, puntos["nariz"], 5, (0, 0, 255), cv2.FILLED)  # Rojo para la nariz
            cv2.circle(image, puntos["hombro_izquierdo"], 5, (0, 255, 0), cv2.FILLED)  # Verde para los hombros
            cv2.circle(image, puntos["hombro_derecho"], 5, (0, 255, 0), cv2.FILLED)  # Verde para los hombros
            cv2.circle(image, puntos["cadera_izquierda"], 5, (255, 0, 0), cv2.FILLED)  # Azul para la cintura
            cv2.circle(image, puntos["cadera_derecha"], 5, (255, 0, 0), cv2.FILLED)  # Azul para la cintura

            # Coordenadas de los puntos relevantes para el ángulo
            A = puntos["nariz"]
            B = ((puntos["hombro_izquierdo"][0] + puntos["hombro_derecho"][0]) // 2, (puntos["hombro_izquierdo"][1] + puntos["hombro_derecho"][1]) // 2)
            C = ((puntos["cadera_izquierda"][0] + puntos["cadera_derecha"][0]) // 2, (puntos["cadera_izquierda"][1] + puntos["cadera_derecha"][1]) // 2)

            # Dibuja líneas moradas entre cuello (nariz), hombros y cintura
            cv2.line(image, A, B, (255, 0, 255), 2)
            cv2.line(image, B, C, (255, 0, 255), 2)

            # Calcula el ángulo
            angulo_curvatura = self.calcular_angulo(A, B, C)
            print(f"Ángulo de curvatura: {angulo_curvatura:.2f} grados")

        # Codifica la imagen procesada a un buffer
        _, buffer = cv2.imencode('.jpg', image)
        return buffer.tobytes()

