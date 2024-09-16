import mediapipe as mp
import cv2
import math

# Inicializa los modelos específicos
mp_pose = mp.solutions.pose

def procesar_videoEDRI(video_front_path):
    cap_front = cv2.VideoCapture(video_front_path)

    if not cap_front.isOpened():
        return {"error": "Error al abrir el video"}

    # Inicializa el modelo de seguimiento de pose
    frontal_angles_left = []

    with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
        try:
            while cap_front.isOpened():
                # Lee un frame de cada video
                success_front, image_front = cap_front.read()
                
                # Detener si no se puede leer un frame de uno o ambos videos
                if not success_front:
                    break

                # Procesa el video frontal
                if success_front:
                    image_front_rgb = cv2.cvtColor(image_front, cv2.COLOR_BGR2RGB)
                    results_front = pose.process(image_front_rgb)
                    if results_front.pose_landmarks:
                        landmarks = results_front.pose_landmarks.landmark
                        # Puntos para el lado izquierdo
                        left_hip = landmarks[mp_pose.PoseLandmark.LEFT_HIP]
                        left_knee = landmarks[mp_pose.PoseLandmark.LEFT_KNEE]
                        left_ankle = landmarks[mp_pose.PoseLandmark.LEFT_ANKLE]

                        # Calcula el ángulo derecho entre cadera, rodilla y tobillo
                        vector1_left = (left_hip.x - left_knee.x, left_hip.y - left_knee.y)
                        vector2_left = (left_ankle.x - left_knee.x, left_ankle.y - left_knee.y)
                        dot_product_left = vector1_left[0] * vector2_left[0] + vector1_left[1] * vector2_left[1]
                        magnitude1_left = math.sqrt(vector1_left[0]**2 + vector1_left[1]**2)
                        magnitude2_left = math.sqrt(vector2_left[0]**2 + vector2_left[1]**2)
                        angle_left = math.degrees(math.acos(dot_product_left / (magnitude1_left * magnitude2_left)))

                        # Agrega los ángulos a la lista si está en el rango de 0 a 180 grados
                        if 0 <= angle_left <= 200:
                            frontal_angles_left.append(angle_left)

        except Exception as e:
            return {"error": str(e)}
        finally:
            # Libera recursos
            cap_front.release()

        # Calcula el ángulo máximo
        resultado = {}
        if frontal_angles_left:
            max_frontal_angle_left = max(frontal_angles_left)
            ajustador = round(max_frontal_angle_left)
            resultado['Angulo'] = int(ajustador)

        return resultado
