import cv2
import math
import mediapipe as mp

mp_pose = mp.solutions.pose

def calcular_angulo(punto1, punto2, punto3):
    vector1 = (punto1.x - punto2.x, punto1.y - punto2.y)
    vector2 = (punto3.x - punto2.x, punto3.y - punto2.y)
    dot_product = vector1[0] * vector2[0] + vector1[1] * vector2[1]
    magnitude1 = math.sqrt(vector1[0]**2 + vector1[1]**2)
    magnitude2 = math.sqrt(vector2[0]**2 + vector2[1]**2)
    return math.degrees(math.acos(dot_product / (magnitude1 * magnitude2)))

def procesar_video_extension_codo_angulo_izquierda(video_front_path):
    cap_front = cv2.VideoCapture(video_front_path)
    if not cap_front.isOpened():
        return {"error": "Error al abrir el video"}

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
                    shoulder = landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER]
                    elbow = landmarks[mp_pose.PoseLandmark.LEFT_ELBOW]
                    wrist = landmarks[mp_pose.PoseLandmark.LEFT_WRIST]

                    angle = calcular_angulo(shoulder, elbow, wrist)

                    if 0 <= angle <= 180:
                        angles.append(angle)

        except Exception as e:
            return {"error": str(e)}
        finally:
            cap_front.release()

    resultado = {}
    if angles:
        max_angle = max(angles)
        resultado['Angulo'] = round(max_angle)

    return resultado