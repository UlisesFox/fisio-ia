import cv2
import math
import numpy as np
import mediapipe as mp

class CurvaturaPiernas:
    def __init__(self):
        self.mp_pose = mp.solutions.pose
        self.pose = self.mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5)

    def calcular_angulo(self, punto_a, punto_b, punto_c):
        vector_ba = (punto_a[0] - punto_b[0], punto_a[1] - punto_b[1])
        vector_bc = (punto_c[0] - punto_b[0], punto_c[1] - punto_b[1])
        
        producto_escalar = vector_ba[0] * vector_bc[0] + vector_ba[1] * vector_bc[1]
        magnitud_ba = math.sqrt(vector_ba[0]**2 + vector_ba[1]**2)
        magnitud_bc = math.sqrt(vector_bc[0]**2 + vector_bc[1]**2)
        
        angulo_radianes = math.acos(producto_escalar / (magnitud_ba * magnitud_bc))
        angulo_grados = math.degrees(angulo_radianes)

        return round(angulo_grados - 80 if angulo_grados >= 80 else angulo_grados + 281)

    def procesar_imagen(self, image_buffer):
        image = cv2.imdecode(np.frombuffer(image_buffer, np.uint8), cv2.IMREAD_COLOR)
        image = cv2.resize(image, (image.shape[1] // 2, image.shape[0] // 2), interpolation=cv2.INTER_AREA)
        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        
        results = self.pose.process(image_rgb)
        if results.pose_landmarks:
            h, w, _ = image.shape
            landmarks = results.pose_landmarks.landmark

            puntos = {
                "cadera_izquierda": (int(landmarks[self.mp_pose.PoseLandmark.LEFT_HIP].x * w), 
                                     int(landmarks[self.mp_pose.PoseLandmark.LEFT_HIP].y * h)),
                "rodilla_izquierda": (int(landmarks[self.mp_pose.PoseLandmark.LEFT_KNEE].x * w), 
                                      int(landmarks[self.mp_pose.PoseLandmark.LEFT_KNEE].y * h)),
                "tobillo_izquierdo": (int(landmarks[self.mp_pose.PoseLandmark.LEFT_ANKLE].x * w), 
                                      int(landmarks[self.mp_pose.PoseLandmark.LEFT_ANKLE].y * h)),
                "cadera_derecha": (int(landmarks[self.mp_pose.PoseLandmark.RIGHT_HIP].x * w), 
                                   int(landmarks[self.mp_pose.PoseLandmark.RIGHT_HIP].y * h)),
                "rodilla_derecha": (int(landmarks[self.mp_pose.PoseLandmark.RIGHT_KNEE].x * w), 
                                    int(landmarks[self.mp_pose.PoseLandmark.RIGHT_KNEE].y * h)),
                "tobillo_derecho": (int(landmarks[self.mp_pose.PoseLandmark.RIGHT_ANKLE].x * w), 
                                    int(landmarks[self.mp_pose.PoseLandmark.RIGHT_ANKLE].y * h)),
            }

            angulo_izquierdo = self.calcular_angulo(puntos["cadera_izquierda"], puntos["rodilla_izquierda"], puntos["tobillo_izquierdo"])
            angulo_derecho = self.calcular_angulo(puntos["cadera_derecha"], puntos["rodilla_derecha"], puntos["tobillo_derecho"])

            return angulo_izquierdo, angulo_derecho

        return None