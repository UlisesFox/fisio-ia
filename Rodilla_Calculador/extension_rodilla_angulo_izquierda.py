import av
import cv2
import math
import numpy as np
import mediapipe as mp
from io import BytesIO

mp_pose = mp.solutions.pose

def calcular_angulo(hip, knee, ankle):
    vector1 = (hip.x - knee.x, hip.y - knee.y)
    vector2 = (ankle.x - knee.x, ankle.y - knee.y)
    dot_product = vector1[0] * vector2[0] + vector1[1] * vector2[1]
    magnitude1 = math.sqrt(vector1[0]**2 + vector1[1]**2)
    magnitude2 = math.sqrt(vector2[0]**2 + vector2[1]**2)
    return math.degrees(math.acos(dot_product / (magnitude1 * magnitude2)))

def procesar_video_extension_rodilla_angulo_izquierda(video_data):
    video_bytes = BytesIO(video_data)
    container = av.open(video_bytes)

    angles = []
    
    with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
        for frame in container.decode(video=0):
            image = np.array(frame.to_image())
            image_bgr = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
            image_rgb = cv2.cvtColor(image_bgr, cv2.COLOR_BGR2RGB)

            results = pose.process(image_rgb)

            if results.pose_landmarks:
                landmarks = results.pose_landmarks.landmark
                hip = landmarks[mp_pose.PoseLandmark.LEFT_HIP]
                knee = landmarks[mp_pose.PoseLandmark.LEFT_KNEE]
                ankle = landmarks[mp_pose.PoseLandmark.LEFT_ANKLE]
                angle = calcular_angulo(hip, knee, ankle)

                if 0 <= angle <= 200:
                    angles.append(angle)

    if angles:
        return {"response": round(max(angles))}

    return {}