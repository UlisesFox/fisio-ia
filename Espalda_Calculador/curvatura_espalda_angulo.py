import cv2
import math
import numpy as np
import mediapipe as mp

class CurvaturaEspalda:
    def __init__(self):
        self.mp_pose = mp.solutions.pose
        self.pose = self.mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5)

    def calcular_angulo(self, punto_a, punto_b, punto_c):
        #Calcula el ángulo entre tres puntos en un plano.
        vector_ba = (punto_a[0] - punto_b[0], punto_a[1] - punto_b[1])
        vector_bc = (punto_c[0] - punto_b[0], punto_c[1] - punto_b[1])
        
        producto_escalar = vector_ba[0] * vector_bc[0] + vector_ba[1] * vector_bc[1]
        magnitud_ba = math.sqrt(vector_ba[0]**2 + vector_ba[1]**2)
        magnitud_bc = math.sqrt(vector_bc[0]**2 + vector_bc[1]**2)
        
        angulo_radianes = math.acos(producto_escalar / (magnitud_ba * magnitud_bc))
        angulo_grados = math.degrees(angulo_radianes)

        return round(angulo_grados - 80 if angulo_grados >= 80 else angulo_grados + 281)

    def procesar_imagen(self, imagen_buffer):
        #Procesa una imagen para calcular la curvatura de la espalda.
        imagen = cv2.imdecode(np.frombuffer(imagen_buffer, np.uint8), cv2.IMREAD_COLOR)
        imagen_rgb = cv2.cvtColor(imagen, cv2.COLOR_BGR2RGB)
        
        resultados = self.pose.process(imagen_rgb)
        if resultados.pose_landmarks:
            h, w, _ = imagen.shape
            landmarks = resultados.pose_landmarks.landmark

            puntos = {
                "oreja_izquierda": self.obtener_coordenada(landmarks, self.mp_pose.PoseLandmark.LEFT_EAR, w, h),
                "oreja_derecha": self.obtener_coordenada(landmarks, self.mp_pose.PoseLandmark.RIGHT_EAR, w, h),
                "hombro_izquierdo": self.obtener_coordenada(landmarks, self.mp_pose.PoseLandmark.LEFT_SHOULDER, w, h),
                "hombro_derecho": self.obtener_coordenada(landmarks, self.mp_pose.PoseLandmark.RIGHT_SHOULDER, w, h),
                "cadera_izquierda": self.obtener_coordenada(landmarks, self.mp_pose.PoseLandmark.LEFT_HIP, w, h),
                "cadera_derecha": self.obtener_coordenada(landmarks, self.mp_pose.PoseLandmark.RIGHT_HIP, w, h)
            }

            punto_a = self.punto_medio(puntos["oreja_izquierda"], puntos["oreja_derecha"])
            punto_b = self.punto_medio(puntos["hombro_izquierdo"], puntos["hombro_derecho"])
            punto_c = self.punto_medio(puntos["cadera_izquierda"], puntos["cadera_derecha"])

            return self.calcular_angulo(punto_a, punto_b, punto_c)

        return None

    def obtener_coordenada(self, landmarks, punto, w, h):
        return int(landmarks[punto].x * w), int(landmarks[punto].y * h)

    def punto_medio(self, punto1, punto2):
        return (punto1[0] + punto2[0]) // 2, (punto1[1] + punto2[1]) // 2
