import numpy as np
import pandas as pd
import tensorflow as tf
from flask import Flask, request, jsonify

class IACurvaturaPiernas:
    def __init__(self, archivo_angulos, archivo_resultados, epochs=600):
        #Inicializa el modelo leyendo los datos y entrenándolo.
        self.angulos = pd.read_excel(archivo_angulos, usecols=['Angulo']).to_numpy(dtype=float).flatten()
        self.resultados = pd.read_excel(archivo_resultados, usecols=['CDP_res']).to_numpy(dtype=float).flatten()

        self.modelo = self.crear_modelo()
        self.modelo.compile(optimizer=tf.keras.optimizers.Adam(0.1), loss='mean_squared_error')

        print("Entrenando el modelo...")
        self.historial = self.modelo.fit(self.angulos, self.resultados, epochs=epochs, verbose=False)
        print("Modelo entrenado!")

    def crear_modelo(self):
        #Crea el modelo de red neuronal.
        return tf.keras.Sequential([
            tf.keras.layers.Dense(units=1, input_shape=[1]),
            tf.keras.layers.Dense(units=5, activation='relu'),
            tf.keras.layers.Dense(units=5, activation='relu'),
            tf.keras.layers.Dense(units=5, activation='relu'),
            tf.keras.layers.Dense(units=1)
        ])

    def predecir(self, angulos):
        #Predice el resultado a partir de los ángulos ingresados.
        resultados = []
        for angulo in angulos:
            prediccion = self.modelo.predict(np.array([angulo]))[0][0]
            ajustado = round(prediccion)

            if ajustado <= 1758 or ajustado >= 1802:
                mensaje = "Deberías consultar con un fisioterapeuta"
            else:
                mensaje = "Rango aceptable"
            resultados.append(mensaje)

        return resultados

# Configuración del servidor Flask
app = Flask(__name__)
modelo_pierna = IACurvaturaPiernas('Dataset.xlsx', 'Dataset.xlsx')

@app.route('/recomendacion_piernas', methods=['POST'])
def recomendacion_piernas():
    data = request.json
    angulos = data.get('Angulo', [])
    if len(angulos) != 2:
        return jsonify({'error': 'No se proporcionó los ángulos'}), 400
    resultado = modelo_pierna.predecir(angulos)
    return jsonify({'resultado': resultado})

if __name__ == '__main__':
    app.run()