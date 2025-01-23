import cv2
import math
import av
import numpy as np
import mediapipe as mp
from io import BytesIO

mp_pose = mp.solutions.pose

def calcular_angulo(hip, shoulder, wrist):
    x1, y1 = hip.x, hip.y
    x2, y2 = shoulder.x, shoulder.y
    x3, y3 = wrist.x, wrist.y

    theta = math.acos(
        ((y2 - y1) * (y3 - y2)) /
        (math.sqrt((x2 - x1)**2 + (y2 - y1)**2) * math.sqrt((x3 - x2)**2 + (y3 - y2)**2))
    )
    degree = math.degrees(theta)
    return degree

def procesar_video_flexion_hombro_angulo_derecha(video_data):
    video_bytes = BytesIO(video_data)
    container = av.open(video_bytes)

    angles = []
    tipo = "angulo"
    desde = "hombro"

    with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
        for frame in container.decode(video=0):
            image_front = np.array(frame.to_image())
            image_front_bgr = cv2.cvtColor(image_front, cv2.COLOR_RGB2BGR)
            image_front_rgb = cv2.cvtColor(image_front_bgr, cv2.COLOR_BGR2RGB)

            results_front = pose.process(image_front_rgb)

            if results_front.pose_landmarks:
                landmarks = results_front.pose_landmarks.landmark
                hip = landmarks[mp_pose.PoseLandmark.RIGHT_HIP]
                shoulder = landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER]
                wrist = landmarks[mp_pose.PoseLandmark.RIGHT_WRIST]
                dato = calcular_angulo(hip, shoulder, wrist)

                angle= dato+90
                if 0 <= angle <= 180:
                    angles.append(angle)

    if angles:
        return {"response": round(max(angles)), "tipo": tipo, "desde": desde}

    return {}