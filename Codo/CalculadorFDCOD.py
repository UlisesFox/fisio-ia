import mediapipe as mp
import cv2
import math

# Inicializa los modelos específicos
mp_pose = mp.solutions.pose

def procesar_videoFDCOD(video_front_path):
    cap_front = cv2.VideoCapture(video_front_path)

    if not cap_front.isOpened():
        return {"error": "Error al abrir el video"}

    # Inicializa el modelo de seguimiento de pose
    angles = []

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
                    # Puntos para el hombro, codo y muñeca
                    shoulder = landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER]
                    elbow = landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW]
                    wrist = landmarks[mp_pose.PoseLandmark.RIGHT_WRIST]

                    # Calcula el ángulo entre hombro, codo y muñeca
                    vector1 = (shoulder.x - elbow.x, shoulder.y - elbow.y)
                    vector2 = (wrist.x - elbow.x, wrist.y - elbow.y)
                    dot_product = vector1[0] * vector2[0] + vector1[1] * vector2[1]
                    magnitude1 = math.sqrt(vector1[0]**2 + vector1[1]**2)
                    magnitude2 = math.sqrt(vector2[0]**2 + vector2[1]**2)
                    angle = math.degrees(math.acos(dot_product / (magnitude1 * magnitude2)))

                    # Almacena el ángulo si está en el rango de 0 a 180 grados
                    if 0 <= angle <= 180:
                        angles.append(angle)

        except Exception as e:
            return {"error": str(e)}
        finally:
            # Libera recursos
            cap_front.release()

        # Calcula el ángulo máximo
        resultado = {}
        if angles:
            max_angle = min(angles)
            resultado['Angulo'] = max_angle

        return resultado
