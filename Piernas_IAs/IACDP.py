import tensorflow as tf
import numpy as np
import pandas as pd
from flask import Flask, request, jsonify

# Definir la clase para el modelo
class IACDP:
    def __init__(self, angle_file, anglesum_file, epochs=600):
        # Leer los datos desde archivos Excel
        angle = pd.read_excel(angle_file, usecols=['Angulo'])
        anglesum = pd.read_excel(anglesum_file, usecols=['CDP_res'])

        # Convertir los datos a arrays de numpy
        self.ids = angle['Angulo'].to_numpy(dtype=float)
        self.suma_ids = anglesum['CDP_res'].to_numpy(dtype=float)

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

    def predecir(self, angulos):
        resultados = []
        for angulo in angulos:
            resultado = self.modelo.predict(np.array([angulo]))
            ajustador = round(resultado[0][0])
            if ajustador <= 1758 or ajustador >= 1802:
                mensaje = "Deberias consultar con un fisioterapeuta"
            else:
                mensaje = "Rango aceptable"
            resultados.append(mensaje)
        return resultados

# Inicializar el predictor
predictor = IACDP('AngulosBase.xlsx', 'Piernas_CDP.xlsx')

# Crear la aplicación Flask
app = Flask(__name__)

@app.route('/predecirCDP', methods=['POST'])
def predecirCDP():
    data = request.json
    Angulos = data.get('Angulos', None)
    if Angulos is None or not isinstance(Angulos, list) or len(Angulos) != 2:
        return jsonify({'error': 'Se deben proporcionar exactamente dos ángulos'}), 400
    resultado = predictor.predecir(Angulos)
    return jsonify({'resultado': resultado})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=4000)