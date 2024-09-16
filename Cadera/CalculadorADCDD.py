import mediapipe as mp
import cv2

# Inicializa los modelos específicos
mp_pose = mp.solutions.pose

def procesar_videoADCDD(video_front_path):
    cap_front = cv2.VideoCapture(video_front_path)

    if not cap_front.isOpened():
        return {"error": "Error al abrir el video"}

    # Inicializa el modelo de seguimiento de pose
    horizontal_distances_right = []

    with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
        try:
            while cap_front.isOpened():
                # Lee un frame del video
                success_front, image_front = cap_front.read()
                
                # Detener si no se puede leer un frame
                if not success_front:
                    break

                # Procesa el video frontal
                image_front_rgb = cv2.cvtColor(image_front, cv2.COLOR_BGR2RGB)
                results_front = pose.process(image_front_rgb)
                if results_front.pose_landmarks:
                    landmarks = results_front.pose_landmarks.landmark
                    # Puntos para el lado derecho
                    right_hip = landmarks[mp_pose.PoseLandmark.RIGHT_HIP]
                    right_ankle = landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE]

                    # Calcula la distancia horizontal entre cadera y tobillo derechos
                    horizontal_distance_right = abs(right_hip.x - right_ankle.x)

                    # Convierte la distancia a unidades reales si se necesita (opcional)
                    horizontal_distances_right.append(horizontal_distance_right)

        except Exception as e:
            return {"error": str(e)}
        finally:
            # Libera recursos
            cap_front.release()

        # Calcula la distancia máxima
        resultado = {}
        if horizontal_distances_right:
            max_horizontal_distance_right = max(horizontal_distances_right)
            redondeador = max_horizontal_distance_right/0.01
            ajustador = round(redondeador)
            resultado['Distancia'] = ajustador

        return resultado
