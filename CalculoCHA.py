import mediapipe as mp
import cv2
import math

# Inicializa los modelos específicos
mp_pose = mp.solutions.pose

def procesar_videoCHA(video_front_path, video_side_path):
    cap_front = cv2.VideoCapture(video_front_path)
    cap_side = cv2.VideoCapture(video_side_path)

    if not cap_front.isOpened() or not cap_side.isOpened():
        return {"error": "Error al abrir uno o ambos videos"}

    # Inicializa el modelo de seguimiento de pose
    frontal_angles = []

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
                        shoulder = landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER]
                        elbow = landmarks[mp_pose.PoseLandmark.LEFT_ELBOW]
                        abdomen = landmarks[mp_pose.PoseLandmark.LEFT_HIP]  # Usaremos la cadera como referencia del abdomen
                        
                        # Calcula el ángulo entre hombro, codo y abdomen
                        vector1 = (shoulder.x - elbow.x, shoulder.y - elbow.y)
                        vector2 = (abdomen.x - elbow.x, abdomen.y - elbow.y)
                        dot_product = vector1[0] * vector2[0] + vector1[1] * vector2[1]
                        magnitude1 = math.sqrt(vector1[0]**2 + vector1[1]**2)
                        magnitude2 = math.sqrt(vector2[0]**2 + vector2[1]**2)
                        angle = math.degrees(math.acos(dot_product / (magnitude1 * magnitude2)))

                        # Asegurarse de que el ángulo sea razonable para un humano
                        if 20 <= angle <= 180:
                            frontal_angles.append(angle)

        except Exception as e:
            return {"error": str(e)}
        finally:
            # Libera recursos
            cap_front.release()
            cap_side.release()

        # Calcula los ángulos y distancias mayor y menor
        resultado = {}
        if frontal_angles:
            max_frontal_angle = max(frontal_angles)
            min_frontal_angle = min(frontal_angles)
            resultado['Frontal max'] = int(max_frontal_angle)
            resultado['Frontal min'] = int(min_frontal_angle)

        return resultado