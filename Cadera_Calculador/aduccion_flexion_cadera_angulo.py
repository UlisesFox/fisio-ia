import av
import cv2
import math
import numpy as np
import mediapipe as mp
from io import BytesIO

mp_pose = mp.solutions.pose

def calcular_angulo(ankle_der, ankle_izq, hip_der, hip_izq):
    cadera_media_x = (hip_der.x + hip_izq.x) / 2
    cadera_media_y = (hip_der.y + hip_izq.y) / 2
    vector1 = (ankle_izq.x - cadera_media_x, ankle_izq.y - cadera_media_y)
    vector2 = (ankle_der.x - cadera_media_x, ankle_der.y - cadera_media_y)
    dot_product = vector1[0] * vector2[0] + vector1[1] * vector2[1]
    magnitude1 = math.sqrt(vector1[0]**2 + vector1[1]**2)
    magnitude2 = math.sqrt(vector2[0]**2 + vector2[1]**2)
    return math.degrees(math.acos(dot_product / (magnitude1 * magnitude2)))

def procesar_video_aduccion_flexion_cadera_angulo(video_data):
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
                ankle_der = landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE]
                ankle_izq = landmarks[mp_pose.PoseLandmark.LEFT_ANKLE]
                hip_der = landmarks[mp_pose.PoseLandmark.RIGHT_HIP]
                hip_izq = landmarks[mp_pose.PoseLandmark.LEFT_HIP]
                angle = calcular_angulo(ankle_der, ankle_izq, hip_der, hip_izq)

                if 0 <= angle <= 180:
                    angles.append(angle)

    if angles:
        return {"response": round(max(angles))}

    return {}