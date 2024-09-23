import cv2
import mediapipe as mp

# Inicializa el modelo de pose de MediaPipe
mp_pose = mp.solutions.pose

def procesar_video_aduccion_cadera_distancia_izquierda(video_front_path):
    #Procesa el video para calcular la distancia horizontal entre cadera y tobillo izquierda.
    cap_front = cv2.VideoCapture(video_front_path)

    if not cap_front.isOpened():
        return {"error": "Error al abrir el video"}

    distancias_horizontales_izquierdas = []

    # Inicia el modelo de detección de pose
    with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
        try:
            while cap_front.isOpened():
                ret, frame = cap_front.read()

                if not ret:
                    break

                frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                results = pose.process(frame_rgb)

                if results.pose_landmarks:
                    landmarks = results.pose_landmarks.landmark

                    cadera_izquierda = landmarks[mp_pose.PoseLandmark.LEFT_HIP]
                    tobillo_izquierdo = landmarks[mp_pose.PoseLandmark.LEFT_ANKLE]

                    distancia_horizontal = abs(cadera_izquierda.x - tobillo_izquierdo.x)
                    distancias_horizontales_izquierdas.append(distancia_horizontal)

        except Exception as e:
            return {"error": str(e)}

        finally:
            cap_front.release() 
        
        if distancias_horizontales_izquierdas:
            max_distancia = max(distancias_horizontales_izquierdas)
            resultado_ajustado = round(max_distancia / 0.01)
            return {'Distancia': resultado_ajustado}

        return {"error": "No se detectaron poses en el video"}