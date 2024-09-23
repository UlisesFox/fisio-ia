import cv2
import mediapipe as mp

# Inicializa los modelos específicos
mp_pose = mp.solutions.pose

def procesar_video_aduccion_hombro_distancia_derecha(video_front_path):
    cap_front = cv2.VideoCapture(video_front_path)

    if not cap_front.isOpened():
        return {"error": "Error al abrir el video"}

    # Inicializa el modelo de seguimiento de pose
    vertical_distances = []

    with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
        try:
            while cap_front.isOpened():

                success_front, image_front = cap_front.read()

                if not success_front:
                    break

                image_front_rgb = cv2.cvtColor(image_front, cv2.COLOR_BGR2RGB)
                results_front = pose.process(image_front_rgb)
                if results_front.pose_landmarks:
                    landmarks = results_front.pose_landmarks.landmark

                    shoulder = landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER]
                    wrist = landmarks[mp_pose.PoseLandmark.RIGHT_WRIST]

                    vertical_distance = abs(wrist.y - shoulder.y)
                    vertical_distances.append(vertical_distance)

        except Exception as e:
            return {"error": str(e)}
        finally:

            cap_front.release()

        resultado = {}
        if vertical_distances:
            max_vertical_distance = min(vertical_distances)
            redondeador = max_vertical_distance/0.01
            ajustador = round(redondeador)
            resultado['Distancia'] = ajustador

        return resultado