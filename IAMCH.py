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

    def predecir(self, frontal_max, frontal_min, lateral):
        # Predecir usando frontal_max
        resultado = self.modelo.predict(np.array([frontal_max]))[0][0]
        if resultado <= 244:
            mensaje = "Rango aceptable"
        else:
            mensaje = "Deberías consultar con un fisioterapeuta"

        # Evaluar frontal_min
        if frontal_min <= 19 or frontal_min >= 31:
            mensaje2 = "Deberías consultar con un fisioterapeuta"
        else:
            mensaje2 = "Rango aceptable"

        # Evaluar lateral
        if lateral == 0:
            mensaje3 = "Rango aceptable"
        else:
            mensaje3 = "Deberías consultar con un fisioterapeuta"

        return mensaje, mensaje2, mensaje3


# Inicializar el predictor
predictor = AngleSumPredictor('angulos.xlsx', 'VerificadorV.xlsx')

# Crear la aplicación Flask
app = Flask(__name__)

@app.route('/predecir', methods=['POST'])
def predecir():
    data = request.json
    
    # Extraer los tres ángulos
    frontal_max = data.get('frontal_max')
    frontal_min = data.get('frontal_min')
    lateral = data.get('lateral')

    # Verificar si se proporcionaron los valores
    if frontal_max is None or frontal_min is None or lateral is None:
        return jsonify({'error': 'No se proporcionaron todos los ángulos'}), 400

    # Obtener los resultados de la predicción
    resultado_max, resultado_min, resultado_lateral = predictor.predecir(frontal_max, frontal_min, lateral)

    # Devolver los resultados
    return jsonify({
        'resultado_max': resultado_max,
        'resultado_min': resultado_min,
        'resultado_lateral': resultado_lateral
    })


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=6000)