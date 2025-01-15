import av
import cv2
import math
import numpy as np
import mediapipe as mp
from io import BytesIO

mp_pose = mp.solutions.pose

def calcular_angulo(shoulder, elbow, wrist):
    x1, y1 = shoulder.x, shoulder.y
    x2, y2 = elbow.x, elbow.y
    x3, y3 = wrist.x, wrist.y

    theta = math.acos(
        ((y2 - y1) * (y3 - y2)) /
        (math.sqrt((x2 - x1)**2 + (y2 - y1)**2) * math.sqrt((x3 - x2)**2 + (y3 - y2)**2))
    )
    degree = math.degrees(theta)
    return degree


def procesar_video_flexion_codo_angulo_izquierda(video_data):
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
                shoulder = landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER]
                elbow = landmarks[mp_pose.PoseLandmark.LEFT_ELBOW]
                wrist = landmarks[mp_pose.PoseLandmark.LEFT_WRIST]
                angle = calcular_angulo(shoulder, elbow, wrist)

                if 0 <= angle <= 180:
                    angles.append(angle)

    if angles:
        return {"response": round(min(angles))}

    return {}