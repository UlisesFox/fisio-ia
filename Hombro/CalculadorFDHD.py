import mediapipe as mp
import cv2

# Inicializa los modelos específicos
mp_pose = mp.solutions.pose

def procesar_videoFDHD(video_front_path):
    cap_front = cv2.VideoCapture(video_front_path)

    if not cap_front.isOpened():
        return {"error": "Error al abrir el video"}

    # Inicializa el modelo de seguimiento de pose
    vertical_distances = []

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
                    # Puntos para la cadera y la muñeca
                    hip = landmarks[mp_pose.PoseLandmark.RIGHT_HIP]
                    wrist = landmarks[mp_pose.PoseLandmark.RIGHT_WRIST]

                    # Calcula la distancia vertical entre la cadera y la muñeca
                    vertical_distance = abs(wrist.y - hip.y)
                    vertical_distances.append(vertical_distance)

        except Exception as e:
            return {"error": str(e)}
        finally:
            # Libera recursos
            cap_front.release()

        # Calcula la distancia vertical máxima
        resultado = {}
        if vertical_distances:
            max_vertical_distance = max(vertical_distances)
            redondeador = max_vertical_distance/0.01
            ajustador = round(redondeador)
            resultado['Distancia'] = ajustador

        return resultado
