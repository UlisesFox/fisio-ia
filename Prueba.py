import cv2
import mediapipe as mp

# Inicializar el módulo de MediaPipe
lapose = mp.solutions.pose

# Objeto de la pose
posestimada = lapose.Pose()

# Cargar una imagen o se puede inicializar la captura de video con OpenCV (pendinente por indagar)
image = cv2.imread('brazo.jpeg')

# Convertir la imagen a RGB
image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

# Realizar la estimación de las poses
resultado = posestimada.process(image_rgb)

# Dibujar las articulaciones en la imagen (pendiente pot correguir)
if resultado.pose_landmarks is not None:
    for marca in resultado.pose_landmarks.landmark:
        # se optiene coordenadas de las articulaciones en pixel
        height, width, _ = image.shape
        cx, cy = int(marca.x * width), int(marca.y * height)

        # Deberia dibujar un circulo en la articulacion
        cv2.circle(image, (cx, cy), 5, (0, 255, 0), -1)

# Muestra la imagen
cv2.imshow('Pose Estimation', image)
cv2.waitKey(0)
cv2.destroyAllWindows()