import mediapipe as mp
import cv2
import math

# Inicializa los modelos específicos
mp_pose = mp.solutions.pose

def procesar_videoFDRD(video_front_path):
    cap_front = cv2.VideoCapture(video_front_path)

    if not cap_front.isOpened():
        return {"error": "Error al abrir el video"}

    # Inicializa el modelo de seguimiento de pose
    frontal_angles_right = []

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
                        # Puntos para el lado derecho
                        right_hip = landmarks[mp_pose.PoseLandmark.RIGHT_HIP]
                        right_knee = landmarks[mp_pose.PoseLandmark.RIGHT_KNEE]
                        right_ankle = landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE]

                        # Calcula el ángulo derecho entre cadera, rodilla y tobillo
                        vector1_right = (right_hip.x - right_knee.x, right_hip.y - right_knee.y)
                        vector2_right = (right_ankle.x - right_knee.x, right_ankle.y - right_knee.y)
                        dot_product_right = vector1_right[0] * vector2_right[0] + vector1_right[1] * vector2_right[1]
                        magnitude1_right = math.sqrt(vector1_right[0]**2 + vector1_right[1]**2)
                        magnitude2_right = math.sqrt(vector2_right[0]**2 + vector2_right[1]**2)
                        angle_right = math.degrees(math.acos(dot_product_right / (magnitude1_right * magnitude2_right)))

                        # Agrega los ángulos a la lista si está en el rango de 0 a 180 grados
                        if 0 <= angle_right <= 180:
                            frontal_angles_right.append(angle_right)

        except Exception as e:
            return {"error": str(e)}
        finally:
            # Libera recursos
            cap_front.release()

        # Calcula el ángulo máximo
        resultado = {}
        if frontal_angles_right:
            max_frontal_angle_right = min(frontal_angles_right)
            ajustador = round(max_frontal_angle_right)
            resultado['Angulo'] = int(ajustador)

        return resultado
