import tensorflow as tf
import numpy as np
import pandas as pd
from flask import Flask, request, jsonify

# Definir la clase para el modelo
class AngleSumPredictor:
    def __init__(self, angle_file, anglesum_file, epochs=600):
        # Leer los datos desde archivos Excel
        angle = pd.read_excel(angle_file, usecols=['angulo'])
        anglesum = pd.read_excel(anglesum_file, usecols=['datos'])

        # Convertir los datos a arrays de numpy
        self.ids = angle['angulo'].to_numpy(dtype=float)
        self.suma_ids = anglesum['datos'].to_numpy(dtype=float)

        # Definir y entrenar el modelo
        self.modelo = self._crear_modelo()
        self.modelo.compile(
            optimizer=tf.keras.optimizers.Adam(0.1),
            loss='mean_squared_error'
        )

        print("Comenzando entrenamiento...")
        self.historial = self.modelo.fit(self.ids, self.suma_ids, epochs=epochs, verbose=False)
        print("Modelo entrenado!")

    def _crear_modelo(self):
        capa = tf.keras.layers.Dense(units=1, input_shape=[1])
        modelo = tf.keras.Sequential([capa])
        return modelo

    def predecir(self, max_frontal_left, max_frontal_right, max_knee_distance, max_lateral_distance, min_frontal_left, min_frontal_right):
        # Predecir usando frontal_max
        resultado = self.modelo.predict(np.array([max_frontal_left]))[0][0]
        if resultado <= 65:
            mensaje = "Rango aceptable"
        else:
            mensaje = "Deberías consultar con un fisioterapeuta"

        resultado2 = self.modelo.predict(np.array([max_frontal_right]))[0][0]
        if resultado2 <= 65:
            mensaje2 = "Rango aceptable"
        else:
            mensaje2 = "Deberías consultar con un fisioterapeuta"

        # Evaluar lateral
        if max_knee_distance == 0:
            mensaje3 = "Rango aceptable"
        else:
            mensaje3 = "Deberías consultar con un fisioterapeuta"

        if max_lateral_distance == 0:
            mensaje4 = "Rango aceptable"
        else:
            mensaje4 = "Deberías consultar con un fisioterapeuta"

        # Evaluar frontal_min
        if min_frontal_left == 0 or min_frontal_left >= 20:
            mensaje5 = "Deberías consultar con un fisioterapeuta"
        else:
            mensaje5 = "Rango aceptable"

        if min_frontal_right == 0 or min_frontal_right >= 20:
            mensaje6 = "Deberías consultar con un fisioterapeuta"
        else:
            mensaje6 = "Rango aceptable"

        return mensaje, mensaje2, mensaje3, mensaje4, mensaje5, mensaje6


# Inicializar el predictor
predictor = AngleSumPredictor('angulos.xlsx', 'VerificadorV.xlsx')

# Crear la aplicación Flask
app = Flask(__name__)

@app.route('/predecir', methods=['POST'])
def predecir():
    data = request.json
    
    # Extraer los tres ángulos
    max_frontal_left = data.get('max_frontal_left')
    max_frontal_right = data.get('max_frontal_right')
    min_frontal_left = data.get('min_frontal_left')
    min_frontal_right = data.get('min_frontal_right')

    # Verificar si se proporcionaron los valores
    if max_frontal_left is None or max_frontal_right is None or min_frontal_left is None or min_frontal_right is None:
        return jsonify({'error': 'No se proporcionaron todos los ángulos'}), 400

    # Obtener los resultados de la predicción
    resultado_max_left, resultado_max_right, resultado_min_left, resultado_min_right = predictor.predecir(max_frontal_left, max_frontal_right, min_frontal_left, min_frontal_right)

    # Devolver los resultados
    return jsonify({
        'resultado_max_left': resultado_max_left,
        'resultado_max_right': resultado_max_right,
        'resultado_min_left': resultado_min_left,
        'resultado_min_right': resultado_min_right
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=6000)