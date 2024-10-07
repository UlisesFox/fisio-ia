import av
import cv2
import numpy as np
import mediapipe as mp
from io import BytesIO

mp_pose = mp.solutions.pose

def calcular_distancia(hip, ankle):
    distance = abs(hip.x - ankle.x)
    return distance

def procesar_video_aduccion_cadera_distancia_izquierda(video_data):
    video_bytes = BytesIO(video_data)
    container = av.open(video_bytes)

    distances = []

    with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
        for frame in container.decode(video=0):
            image = np.array(frame.to_image())
            image_bgr = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
            image_rgb = cv2.cvtColor(image_bgr, cv2.COLOR_BGR2RGB)

            results = pose.process(image_rgb)

            if results.pose_landmarks:
                landmarks = results.pose_landmarks.landmark
                hip = landmarks[mp_pose.PoseLandmark.LEFT_HIP]
                ankle = landmarks[mp_pose.PoseLandmark.LEFT_ANKLE]
                distance = calcular_distancia(hip, ankle)

                distances.append(distance)

    if distances:
        max_distance = max(distances)
        redondeador = max_distance/0.01
        ajustador = round(redondeador)
        return {"Distancia": ajustador}

    return {}