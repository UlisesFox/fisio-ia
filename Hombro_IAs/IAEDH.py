import tensorflow as tf
import numpy as np
import pandas as pd
from flask import Flask, request, jsonify

# Definir la clase para el modelo
class EDH:
    def __init__(self, angle_file, anglesum_file, epochs=600):
        # Leer los datos desde archivos Excel
        angle = pd.read_excel(angle_file, usecols=['Distancia'])
        anglesum = pd.read_excel(anglesum_file, usecols=['EDH_res'])

        # Convertir los datos a arrays de numpy
        self.ids = angle['Distancia'].to_numpy(dtype=float)
        self.suma_ids = anglesum['EDH_res'].to_numpy(dtype=float)

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

    def predecir(self, valor):
        resultado = self.modelo.predict(np.array([valor]))
        ajustador = round(resultado[0][0])
        if ajustador <= 4158 or ajustador >= 4180:
            mensaje = "Deberías consultar con un fisioterapeuta"
        else:
            mensaje = "Rango aceptable"
        print(ajustador)
        return mensaje


# Inicializar el predictor
predictor = EDH('DataBase.xlsx', 'DataBase.xlsx')

# Crear la aplicación Flask
app = Flask(__name__)

@app.route('/predecirEDH', methods=['POST'])
def predecirEDH():
    data = request.json
    Valor = data.get('Distancia', None)
    if Valor is None:
        return jsonify({'error': 'No se proporcionaron todos los ángulos'}), 400
    resultado = predictor.predecir(Valor)
    return jsonify({'resultado': resultado})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5100)