import cv2
import math
import mediapipe as mp

# Inicializa los modelos específicos
mp_pose = mp.solutions.pose

def calcular_angulo(hip, knee, ankle):
    vector1 = (hip.x - knee.x, hip.y - knee.y)
    vector2 = (ankle.x - knee.x, ankle.y - knee.y)
    dot_product = vector1[0] * vector2[0] + vector1[1] * vector2[1]
    magnitude1 = math.sqrt(vector1[0]**2 + vector1[1]**2)
    magnitude2 = math.sqrt(vector2[0]**2 + vector2[1]**2)
    return math.degrees(math.acos(dot_product / (magnitude1 * magnitude2)))

def procesar_video_extension_rodilla_angulo_derecha(video_front_path):
    cap_front = cv2.VideoCapture(video_front_path)
    
    if not cap_front.isOpened():
        return {"error": "Error al abrir el video"}

    frontal_angles_right = []
    
    with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
        while cap_front.isOpened():
            success_front, image_front = cap_front.read()
            if not success_front:
                break
            
            image_front_rgb = cv2.cvtColor(image_front, cv2.COLOR_BGR2RGB)
            results_front = pose.process(image_front_rgb)

            if results_front.pose_landmarks:
                landmarks = results_front.pose_landmarks.landmark
                right_hip = landmarks[mp_pose.PoseLandmark.RIGHT_HIP]
                right_knee = landmarks[mp_pose.PoseLandmark.RIGHT_KNEE]
                right_ankle = landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE]
                angle_right = calcular_angulo(right_hip, right_knee, right_ankle)

                if 0 <= angle_right <= 200:
                    frontal_angles_right.append(angle_right)

    cap_front.release()

    if frontal_angles_right:
        return {"Angulo": round(max(frontal_angles_right))}

    return {}
