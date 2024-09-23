import cv2
import mediapipe as mp


# Inicializa el modelo de pose de MediaPipe
mp_pose = mp.solutions.pose

def procesar_video_extension_cadera_distancia(video_path):
    #Procesa el video para calcular la distancia vertical entre los tobillos.
    cap = cv2.VideoCapture(video_path)

    if not cap.isOpened():
        return {"error": "Error al abrir el video"}

    distancias_verticales = []

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
  
                    distancia_vertical = abs(tobillo_der.y - tobillo_izq.y)
                    distancias_verticales.append(distancia_vertical)

        except Exception as e:
            return {"error": str(e)}

        finally:
            cap.release()
        if distancias_verticales:
            max_distancia = max(distancias_verticales)
            return {'Distancia': round(max_distancia / 0.01)}

        return {"error": "No se detectaron poses en el video"}
