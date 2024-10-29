import numpy as np
import pandas as pd
import tensorflow as tf
from flask import Flask, request, jsonify

class IAFlexionCadera:
    def __init__(self, archivo_angulos, archivo_resultados, epocas=600):
        #Inicializa el modelo leyendo los datos y entrenándolo.
        self.angulos = pd.read_excel(archivo_angulos, usecols=['Angulo']).to_numpy(dtype=float).flatten()
        self.resultados = pd.read_excel(archivo_resultados, usecols=['FDC_res']).to_numpy(dtype=float).flatten()

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

    def predecir(self, angulo):
        #Predice el resultado a partir del ángulo ingresados.
        prediccion = self.modelo.predict(np.array([angulo]))[0][0]
        if 7191 <= round(prediccion) <= 7211:
            return "No Deberías consultar con un fisioterapeuta"
        return "Deberías consultar con un fisioterapeuta"

# Configuración del servidor Flask
app = Flask(__name__)
modelo_espalda = IAFlexionCadera('Dataset.xlsx', 'Dataset.xlsx')

@app.route('/flexionCadera', methods=['POST'])
def FlexionCadera():
    angulo = request.form.get('dato')
    if angulo is None:
        return jsonify({'error': 'No se proporcionó el ángulo'}), 400
    resultado = modelo_espalda.predecir(float(angulo))
    return jsonify({'resultado': resultado})

@app.route('/vivo', methods=['POST'])
def vivo():
    
    respuesta = "si los estoy escuchando"
    
    return jsonify(respuesta)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5011)