import cv2
import mediapipe as mp

def calcular_distancia_horizontal(landmarks, hombro_idx, muñeca_idx):
    hombro = landmarks[hombro_idx]
    muñeca = landmarks[muñeca_idx]
    return abs(muñeca.x - hombro.x)

def procesar_video(video_front_path, hombro_idx, muñeca_idx):
    cap = cv2.VideoCapture(video_front_path)
    if not cap.isOpened():
        return {"error": "Error al abrir el video"}

    distancias_horizontales = []
    mp_pose = mp.solutions.pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5)

    while cap.isOpened():
        success, frame = cap.read()
        if not success:
            break

        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        resultados = mp_pose.process(frame_rgb)

        if resultados.pose_landmarks:
            distancia = calcular_distancia_horizontal(resultados.pose_landmarks.landmark, hombro_idx, muñeca_idx)
            distancias_horizontales.append(distancia)

    cap.release()

    if distancias_horizontales:
        max_distancia = round(max(distancias_horizontales) / 0.01)
        return {'Distancia': max_distancia}

    return {}

def procesar_video_extension_hombro_distancia_izquierda(video_front_path):
    return procesar_video(video_front_path, mp.solutions.pose.PoseLandmark.LEFT_SHOULDER, mp.solutions.pose.PoseLandmark.LEFT_WRIST)
