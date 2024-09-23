import cv2
import math
import mediapipe as mp

# Inicializa los modelos específicos
mp_pose = mp.solutions.pose

def procesar_video_aduccion_hombro_angulo_derecha(video_front_path):
    cap_front = cv2.VideoCapture(video_front_path)

    if not cap_front.isOpened():
        return {"error": "Error al abrir el video"}

    # Inicializa el modelo de seguimiento de pose
    angles = []

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

                    hip = landmarks[mp_pose.PoseLandmark.RIGHT_HIP]
                    elbow = landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW]
                    shoulder = landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER]

                    vector1 = (hip.x - shoulder.x, hip.y - shoulder.y)
                    vector2 = (elbow.x - shoulder.x, elbow.y - shoulder.y)
                    dot_product = vector1[0] * vector2[0] + vector1[1] * vector2[1]
                    magnitude1 = math.sqrt(vector1[0]**2 + vector1[1]**2)
                    magnitude2 = math.sqrt(vector2[0]**2 + vector2[1]**2)
                    angle = math.degrees(math.acos(dot_product / (magnitude1 * magnitude2)))

                    if 0 <= angle <= 180:
                        angles.append(angle)

        except Exception as e:
            return {"error": str(e)}
        finally:
            cap_front.release()

        resultado = {}
        if angles:
            max_angle = max(angles)
            ajustador = round(max_angle)
            resultado['Angulo'] = ajustador

        return resultado
