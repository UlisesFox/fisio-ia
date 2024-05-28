import cv2
import mediapipe as mp

class Menu1:
    def menu():
        print("\nSelección de analisis")
        print("1. AutoDoc Postura")
        print("2. AutoDoc Movimiento")
        print("0. Salir")

    def postura():
        while True:
            MenuP.menu()
            opcion = input("Seleccione una opción: ")
            
            if opcion == '1':
                MenuP.postura()
            elif opcion == '2':
                MenuP.movimiento()
            elif opcion == '0':
                print("Regresado...")
                break
            else:
                print("Opción no válida. Por favor, seleccione nuevamente.")

    def movimiento():
        print("Proximamente...")

class MenuP:
    def menu():
        print("\nMenú de Postura a analizar")
        print("1. Postura de espalda")
        print("2. Postura de pies")
        print("0. Salir")

    def postura():
        print("Cargando...")
        Docespalda = espalda()
        imagen = "ImagenTempoEspalda.jpeg"
        Docespalda.procesarE(imagen)

    def movimiento():
        print("Cargando...")
        Docpiernas = piernas()
        Dimagen = "ImagenTempoEspalda.jpeg"
        Docpiernas.procesarP(Dimagen)

class MenuM:
    def menu():
        print("\nMenú de Movimiento a analizar")
        print("1. Postura de espalda")
        print("2. Postura de pies")
        print("0. Salir")

    def postura():
        print("Proximamente...")

    def movimiento():
        print("Proximamente...")



class espalda:
    def __init__(self):
        self.mp_pose = mp.solutions.pose
        self.mp_drawing = mp.solutions.drawing_utils
        self.pose = self.mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5)

    def procesarE(self, image_path):
        # Lee la imagen desde el disco
        image = cv2.imread(image_path)
        # Redimensiona la imagen para que sea más pequeña
        scale_percent = 50  # Cambia este porcentaje para ajustar el tamaño
        width = int(image.shape[1] * scale_percent / 100)
        height = int(image.shape[0] * scale_percent / 100)
        dim = (width, height)
        image = cv2.resize(image, dim, interpolation=cv2.INTER_AREA)

        # Convierte la imagen a RGB
        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        # Procesa la imagen para detectar la pose
        results = self.pose.process(image_rgb)

        # Si se detecta la pose, dibuja landmarks y conectores
        if results.pose_landmarks:
            # Dibuja los landmarks de la pose con colores diferentes para cuello, hombros y cintura
            for landmark_id, landmark in enumerate(results.pose_landmarks.landmark):
                h, w, _ = image.shape
                cx, cy = int(landmark.x * w), int(landmark.y * h)

                # Lista de landmarks a excluir (ojos y boca)
                exclude_landmarks = [
                    self.mp_pose.PoseLandmark.LEFT_EYE_INNER,
                    self.mp_pose.PoseLandmark.LEFT_EYE,
                    self.mp_pose.PoseLandmark.LEFT_EYE_OUTER,
                    self.mp_pose.PoseLandmark.RIGHT_EYE_INNER,
                    self.mp_pose.PoseLandmark.RIGHT_EYE,
                    self.mp_pose.PoseLandmark.RIGHT_EYE_OUTER,
                    self.mp_pose.PoseLandmark.LEFT_EAR,
                    self.mp_pose.PoseLandmark.RIGHT_EAR,
                    self.mp_pose.PoseLandmark.MOUTH_LEFT,
                    self.mp_pose.PoseLandmark.MOUTH_RIGHT,
                    self.mp_pose.PoseLandmark.LEFT_WRIST,
                    self.mp_pose.PoseLandmark.RIGHT_WRIST,
                    self.mp_pose.PoseLandmark.LEFT_ELBOW,
                    self.mp_pose.PoseLandmark.RIGHT_ELBOW,
                    self.mp_pose.PoseLandmark.LEFT_KNEE,
                    self.mp_pose.PoseLandmark.RIGHT_KNEE,
                    self.mp_pose.PoseLandmark.LEFT_ANKLE,
                    self.mp_pose.PoseLandmark.RIGHT_ANKLE,
                    self.mp_pose.PoseLandmark.LEFT_PINKY,
                    self.mp_pose.PoseLandmark.RIGHT_PINKY,
                    self.mp_pose.PoseLandmark.LEFT_INDEX,
                    self.mp_pose.PoseLandmark.RIGHT_INDEX,
                    self.mp_pose.PoseLandmark.LEFT_THUMB,
                    self.mp_pose.PoseLandmark.RIGHT_THUMB
                ]

                if landmark_id in exclude_landmarks:
                    continue

                if landmark_id in [self.mp_pose.PoseLandmark.LEFT_SHOULDER, self.mp_pose.PoseLandmark.RIGHT_SHOULDER]:
                    color = (0, 0, 255)
                elif landmark_id in [self.mp_pose.PoseLandmark.LEFT_HIP, self.mp_pose.PoseLandmark.RIGHT_HIP]:
                    color = (0, 255, 0)
                elif landmark_id == self.mp_pose.PoseLandmark.NOSE:
                    color = (255, 0, 0)
                else:
                    color = (255, 255, 255)

                cv2.circle(image, (cx, cy), 5, color, cv2.FILLED)

                landmarks = results.pose_landmarks.landmark
                left_shoulder = (int(landmarks[self.mp_pose.PoseLandmark.LEFT_SHOULDER].x * w), int(landmarks[self.mp_pose.PoseLandmark.LEFT_SHOULDER].y * h))
                right_shoulder = (int(landmarks[self.mp_pose.PoseLandmark.RIGHT_SHOULDER].x * w), int(landmarks[self.mp_pose.PoseLandmark.RIGHT_SHOULDER].y * h))
                left_hip = (int(landmarks[self.mp_pose.PoseLandmark.LEFT_HIP].x * w), int(landmarks[self.mp_pose.PoseLandmark.LEFT_HIP].y * h))
                right_hip = (int(landmarks[self.mp_pose.PoseLandmark.RIGHT_HIP].x * w), int(landmarks[self.mp_pose.PoseLandmark.RIGHT_HIP].y * h))
                nose = (int(landmarks[self.mp_pose.PoseLandmark.NOSE].x * w), int(landmarks[self.mp_pose.PoseLandmark.NOSE].y * h))

                # Dibuja líneas moradas entre cuello (nariz), hombros y cintura
                cv2.line(image, nose, left_shoulder, (255, 255, 255), 2)
                cv2.line(image, nose, right_shoulder, (255, 255, 255), 2)
                cv2.line(image, left_shoulder, left_hip, (255, 255, 255), 2)
                cv2.line(image, right_shoulder, right_hip, (255, 255, 255), 2)

        # Muestra el resultado
        cv2.imshow('AutoDoc Postura', image)
        cv2.waitKey(0)  # Espera hasta que se presione una tecla
        cv2.destroyAllWindows()

class piernas:
    def procesarP(image_path):
        print("En progreso...")