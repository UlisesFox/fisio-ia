import cv2
import mediapipe as mp

def calcular_distancia_vertical(landmarks, cadera_idx, muñeca_idx):
    cadera = landmarks[cadera_idx]
    muñeca = landmarks[muñeca_idx]
    return abs(muñeca.y - cadera.y)

def procesar_video_vertical(video_front_path, cadera_idx, muñeca_idx):
    cap = cv2.VideoCapture(video_front_path)
    if not cap.isOpened():
        return {"error": "Error al abrir el video"}

    distancias_verticales = []
    mp_pose = mp.solutions.pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5)

    while cap.isOpened():
        success, frame = cap.read()
        if not success:
            break

        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        resultados = mp_pose.process(frame_rgb)

        if resultados.pose_landmarks:
            distancia = calcular_distancia_vertical(resultados.pose_landmarks.landmark, cadera_idx, muñeca_idx)
            distancias_verticales.append(distancia)

    cap.release()

    if distancias_verticales:
        max_distancia = round(max(distancias_verticales) / 0.01)
        return {'Distancia': max_distancia}

    return {}

def procesar_video_flexion_hombro_distancia_derecha(video_front_path):
    return procesar_video_vertical(video_front_path, mp.solutions.pose.PoseLandmark.RIGHT_HIP, mp.solutions.pose.PoseLandmark.RIGHT_WRIST)
