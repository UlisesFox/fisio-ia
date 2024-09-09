import tensorflow as tf
import numpy as np
import pandas as pd
from flask import Flask, request, jsonify

# Definir la clase para el modelo
class IACDE:
    def __init__(self, angle_file, anglesum_file, epochs=600):
        # Leer los datos desde archivos Excel
        angle = pd.read_excel(angle_file, usecols=['Angulo'])
        anglesum = pd.read_excel(anglesum_file, usecols=['CDE_res'])

        # Convertir los datos a arrays de numpy
        self.ids = angle['Angulo'].to_numpy(dtype=float)
        self.suma_ids = anglesum['CDE_res'].to_numpy(dtype=float)

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
        modelo = tf.keras.Sequential([
            tf.keras.layers.Dense(units=1, input_shape=[1]),
            tf.keras.layers.Dense(units=5),
            tf.keras.layers.Dense(units=5),
            tf.keras.layers.Dense(units=5),
            tf.keras.layers.Dense(units=5),
            tf.keras.layers.Dense(units=1)
        ])
        return modelo

    def predecir(self, angulo):
        resultado = self.modelo.predict(np.array([angulo]))
        ajustador = round(resultado[0][0])
        if ajustador <= 1098 or ajustador >= 1142:
            mensaje = "Deberias consultar con un fisioterapeuta"
        else:
            mensaje = "Rango aceptable"
        return mensaje

# Inicializar el predictor
predictor = IACDE('AngulosBase.xlsx', 'Espalda_CDE.xlsx')

# Crear la aplicación Flask
app = Flask(__name__)

@app.route('/predecirCDE', methods=['POST'])
def predecirCDE():
    data = request.json
    Angulo = data.get('Angulo', None)
    if Angulo is None:
        return jsonify({'error': 'No se proporcionó el ángulo'}), 400
    resultado = predictor.predecir(Angulo)
    return jsonify({'resultado': resultado})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000)