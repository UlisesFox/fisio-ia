import av
import cv2
import math
import numpy as np
import mediapipe as mp
from io import BytesIO

mp_pose = mp.solutions.pose

def findAngle(x1, y1, x2, y2):
    theta = math.acos((y2 - y1) * (-y1) / (math.sqrt((x2 - x1)**2 + (y2 - y1)**2) * y1))
    degree = int(180 / math.pi) * theta
    return degree

def procesar_video_flexion_cadera_angulo(video_data):
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
                ankle_izq = landmarks[mp_pose.PoseLandmark.LEFT_ANKLE]
                hip_izq = landmarks[mp_pose.PoseLandmark.LEFT_HIP]
                ankle_der = landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE]
                hip_der = landmarks[mp_pose.PoseLandmark.RIGHT_HIP]
                
                x1_izq, y1_izq = ankle_izq.x, ankle_izq.y
                x2_izq, y2_izq = hip_izq.x, hip_izq.y
                x1_der, y1_der = ankle_der.x, ankle_der.y
                x2_der, y2_der = hip_der.x, hip_der.y
                
                angle_izq = findAngle(x1_izq, y1_izq, x2_izq, y2_izq)
                angle_der = findAngle(x1_der, y1_der, x2_der, y2_der)

                if 0 <= angle_izq <= 180:
                    angles.append(angle_izq)
                if 0 <= angle_der <= 180:
                    angles.append(angle_der)

    if angles:
        return {"response": round(max(angles))}

    return {}

def procesar_video_abduccion_cadera_angulo(video_data):
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
                ankle_izq = landmarks[mp_pose.PoseLandmark.LEFT_ANKLE]
                hip_izq = landmarks[mp_pose.PoseLandmark.LEFT_HIP]
                ankle_der = landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE]
                hip_der = landmarks[mp_pose.PoseLandmark.RIGHT_HIP]
                
                x1_izq, y1_izq = ankle_izq.x, ankle_izq.y
                x2_izq, y2_izq = hip_izq.x, hip_izq.y
                x1_der, y1_der = ankle_der.x, ankle_der.y
                x2_der, y2_der = hip_der.x, hip_der.y
                
                angle_izq = findAngle(x1_izq, y1_izq, x2_izq, y2_izq)
                angle_der = findAngle(x1_der, y1_der, x2_der, y2_der)

                if 0 <= angle_izq <= 180:
                    angles.append(angle_izq)
                if 0 <= angle_der <= 180:
                    angles.append(angle_der)

    if angles:
        return {"response": round(min(angles))}

    return {}
