import mediapipe as mp
import cv2

# Inicializa los modelos específicos
mp_pose = mp.solutions.pose

def procesar_videoADCDI(video_front_path):
    cap_front = cv2.VideoCapture(video_front_path)

    if not cap_front.isOpened():
        return {"error": "Error al abrir el video"}

    # Inicializa el modelo de seguimiento de pose
    horizontal_distances_left = []

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
                    left_hip = landmarks[mp_pose.PoseLandmark.LEFT_HIP]
                    left_ankle = landmarks[mp_pose.PoseLandmark.LEFT_ANKLE]

                    # Calcula la distancia horizontal entre cadera y tobillo derechos
                    horizontal_distance_left = abs(left_hip.x - left_ankle.x)

                    # Convierte la distancia a unidades reales si se necesita (opcional)
                    horizontal_distances_left.append(horizontal_distance_left)

        except Exception as e:
            return {"error": str(e)}
        finally:
            # Libera recursos
            cap_front.release()

        # Calcula la distancia máxima
        resultado = {}
        if horizontal_distances_left:
            max_horizontal_distance_left = max(horizontal_distances_left)
            redondeador = max_horizontal_distance_left/0.01
            ajustador = round(redondeador)
            resultado['Distancia'] = ajustador

        return resultado
