import numpy as np
import pandas as pd
import tensorflow as tf
from flask import Flask, request, jsonify

class IAExtensionHombro:
    def __init__(self, archivo_angulos, archivo_resultados, epocas=600):
        #Inicializa el modelo leyendo los datos y entrenándolo.
        self.angulos = pd.read_excel(archivo_angulos, usecols=['Distancia']).to_numpy(dtype=float).flatten()
        self.resultados = pd.read_excel(archivo_resultados, usecols=['EDH_res']).to_numpy(dtype=float).flatten()

        self.modelo = self.crear_modelo()
        self.modelo.compile(optimizer=tf.keras.optimizers.Adam(0.1), loss='mean_squared_error')

        print("Entrenando modelo...")
        self.historial = self.modelo.fit(self.angulos, self.resultados, epochs=epocas, verbose=False)
        print("Entrenamiento completado.")

    def crear_modelo(self):
        #Crea el modelo de red neuronal.
        return tf.keras.Sequential([
            tf.keras.layers.Dense(units=1, input_shape=[1]),
            tf.keras.layers.Dense(units=5, activation='relu'),
            tf.keras.layers.Dense(units=5, activation='relu'),
            tf.keras.layers.Dense(units=1)
        ])

    def predecir(self, distancia):
        #Predice el resultado a partir de una distancia ingresados.
        prediccion = self.modelo.predict(np.array([distancia]))[0][0]
        if 4159 <= round(prediccion) <= 4179:
            return "No Deberías consultar con un fisioterapeuta"
        return "Deberías consultar con un fisioterapeuta"

# Configuración del servidor Flask
app = Flask(__name__)
modelo_espalda = IAExtensionHombro('Dataset.xlsx', 'Dataset.xlsx')

@app.route('/extensionHombro', methods=['POST'])
def ExtensionHombro():
    angulo = request.form.get('dato')
    if distancia is None:
        return jsonify({'error': 'No se proporcionó una distancia'}), 400
    resultado = modelo_espalda.predecir(float(distancia))
    return jsonify({'resultado': resultado})

@app.route('/vivo', methods=['POST'])
def vivo():
    
    respuesta = "si los estoy escuchando"
    
    return jsonify(respuesta)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5005)