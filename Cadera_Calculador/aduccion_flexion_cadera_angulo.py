import cv2
import math
import mediapipe as mp

# Inicializa el modelo de pose de MediaPipe
mp_pose = mp.solutions.pose

def procesar_video_aduccion_flexion_cadera_angulo(video_path):
    #Procesa el video para calcular el ángulo entre los tobillos con la cadera como punto medio.
    cap = cv2.VideoCapture(video_path)

    if not cap.isOpened():
        return {"error": "Error al abrir el video"}

    angulos = []

    # Inicia el modelo de detección de pose
    with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
        try:
            while cap.isOpened():
                ret, frame = cap.read()

                if not ret:
                    break

                frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                results = pose.process(frame_rgb)

                if results.pose_landmarks:
                    landmarks = results.pose_landmarks.landmark

                    tobillo_der = landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE]
                    tobillo_izq = landmarks[mp_pose.PoseLandmark.LEFT_ANKLE]
                    cadera_der = landmarks[mp_pose.PoseLandmark.RIGHT_HIP]
                    cadera_izq = landmarks[mp_pose.PoseLandmark.LEFT_HIP]

                    cadera_media_x = (cadera_der.x + cadera_izq.x) / 2
                    cadera_media_y = (cadera_der.y + cadera_izq.y) / 2

                    vector_izq = (tobillo_izq.x - cadera_media_x, tobillo_izq.y - cadera_media_y)
                    vector_der = (tobillo_der.x - cadera_media_x, tobillo_der.y - cadera_media_y)

                    producto_escalar = vector_izq[0] * vector_der[0] + vector_izq[1] * vector_der[1]
                    magnitud_izq = math.sqrt(vector_izq[0]**2 + vector_izq[1]**2)
                    magnitud_der = math.sqrt(vector_der[0]**2 + vector_der[1]**2)

                    angulo = math.degrees(math.acos(producto_escalar / (magnitud_izq * magnitud_der)))

                    if 0 <= angulo <= 180:
                        angulos.append(angulo)

        except Exception as e:
            return {"error": str(e)}

        finally:
            cap.release()

        if angulos:
            max_angulo = max(angulos)
            return {'Angulo': round(max_angulo)}

        return {"error": "No se detectaron poses en el video"}
