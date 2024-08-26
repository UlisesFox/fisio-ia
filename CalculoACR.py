import mediapipe as mp
import cv2
import math

# Inicializa los modelos específicos
mp_pose = mp.solutions.pose

def procesar_videoACR(video_front_path, video_side_path):
    cap_front = cv2.VideoCapture(video_front_path)
    cap_side = cv2.VideoCapture(video_side_path)

    if not cap_front.isOpened() or not cap_side.isOpened():
        return {"error": "Error al abrir uno o ambos videos"}

    # Inicializa el modelo de seguimiento de pose
    frontal_angles_left = []
    frontal_angles_right = []

    with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
        try:
            while cap_front.isOpened() or cap_side.isOpened():
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
                        left_shoulder = landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER]
                        right_hip = landmarks[mp_pose.PoseLandmark.RIGHT_HIP]
                        right_knee = landmarks[mp_pose.PoseLandmark.RIGHT_KNEE]
                        right_shoulder = landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER]

                        # Calcula el ángulo izquierdo entre rodilla, cadera y hombro
                        vector1_left = (left_knee.x - left_hip.x, left_knee.y - left_hip.y)
                        vector2_left = (left_shoulder.x - left_hip.x, left_shoulder.y - left_hip.y)
                        dot_product_left = vector1_left[0] * vector2_left[0] + vector1_left[1] * vector2_left[1]
                        magnitude1_left = math.sqrt(vector1_left[0]**2 + vector1_left[1]**2)
                        magnitude2_left = math.sqrt(vector2_left[0]**2 + vector2_left[1]**2)
                        angle_left = math.degrees(math.acos(dot_product_left / (magnitude1_left * magnitude2_left)))

                        # Calcula el ángulo derecho entre rodilla, cadera y hombro
                        vector1_right = (right_knee.x - right_hip.x, right_knee.y - right_hip.y)
                        vector2_right = (right_shoulder.x - right_hip.x, right_shoulder.y - right_hip.y)
                        dot_product_right = vector1_right[0] * vector2_right[0] + vector1_right[1] * vector2_right[1]
                        magnitude1_right = math.sqrt(vector1_right[0]**2 + vector1_right[1]**2)
                        magnitude2_right = math.sqrt(vector2_right[0]**2 + vector2_right[1]**2)
                        angle_right = math.degrees(math.acos(dot_product_right / (magnitude1_right * magnitude2_right)))

                        # Agrega los ángulos a las listas
                        if 0 <= angle_left <= 180:
                            frontal_angles_left.append(angle_left)
                        if 0 <= angle_right <= 180:
                            frontal_angles_right.append(angle_right)

        except Exception as e:
            return {"error": str(e)}
        finally:
            # Libera recursos
            cap_front.release()
            cap_side.release()

        # Calcula los ángulos y distancias mayor y menor
        resultado = {}
        if frontal_angles_left:
            max_frontal_angle_left = max(frontal_angles_left)
            min_frontal_angle_left = min(frontal_angles_left)
            resultado['Max Frontal Left'] = int(max_frontal_angle_left)
            resultado['Min Frontal Left'] = int(min_frontal_angle_left)

        if frontal_angles_right:
            max_frontal_angle_right = max(frontal_angles_right)
            min_frontal_angle_right = min(frontal_angles_right)
            resultado['Max Frontal Right'] = int(max_frontal_angle_right)
            resultado['Min Frontal Right'] = int(min_frontal_angle_right)

        return resultado
