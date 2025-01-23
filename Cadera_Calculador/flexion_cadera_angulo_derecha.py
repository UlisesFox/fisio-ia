import av
import cv2
import math
import numpy as np
import mediapipe as mp
from io import BytesIO

mp_pose = mp.solutions.pose

def calcular_angulo(ankle_left, hip, ankle_right):
    x1, y1 = ankle_left.x, ankle_left.y
    x2, y2 = hip.x, hip.y
    x3, y3 = ankle_right.x, ankle_right.y

    theta = math.acos(
        ((y2 - y1) * (y3 - y2)) /
        (math.sqrt((x2 - x1)**2 + (y2 - y1)**2) * math.sqrt((x3 - x2)**2 + (y3 - y2)**2))
    )
    degree = math.degrees(theta)
    return degree

def procesar_video_flexion_cadera_angulo_derecha(video_data):
    video_bytes = BytesIO(video_data)
    container = av.open(video_bytes)

    angles = []
    tipo = "angulo"
    desde = "cadera"
    
    with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
        for frame in container.decode(video=0):
            image = np.array(frame.to_image())
            image_bgr = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
            image_rgb = cv2.cvtColor(image_bgr, cv2.COLOR_BGR2RGB)

            results = pose.process(image_rgb)

            if results.pose_landmarks:
                landmarks = results.pose_landmarks.landmark
                ankle_left = landmarks[mp_pose.PoseLandmark.LEFT_ANKLE]
                hip = landmarks[mp_pose.PoseLandmark.LEFT_HIP]
                ankle_right = landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE]
                dato = calcular_angulo(ankle_left, hip, ankle_right)

                angle = dato-30
                if 0 <= angle <= 180:
                    angles.append(angle)

    if angles:
        return {"response": round(max(angles)), "tipo": tipo, "desde": desde}

    return {}