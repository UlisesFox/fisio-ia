from flask import Flask, request, jsonify
import os
# Imagen
from Espalda.CalculadorCDE import CDE

from Piernas.CalculadorCDP import CDP

# Video
from Rodilla.CalculadorEDRD import procesar_videoEDRD
from Rodilla.CalculadorEDRI import procesar_videoEDRI
from Rodilla.CalculadorFDRD import procesar_videoFDRD
from Rodilla.CalculadorFDRI import procesar_videoFDRI

from Cadera.CalculadorADCDD import procesar_videoADCDD
from Cadera.CalculadorADCDI import procesar_videoADCDI
from Cadera.CalculadorAYFDC import procesar_videoAYFDC
from Cadera.CalculadorEDC import procesar_videoEDC

from Codo.CalculadorEDCOD import procesar_videoEDCOD
from Codo.CalculadorEDCOI import procesar_videoEDCOI
from Codo.CalculadorFDCOD import procesar_videoFDCOD
from Codo.CalculadorFDCOI import procesar_videoFDCOI

from Hombro.CalculadorADHAD import procesar_videoADHAD
from Hombro.CalculadorADHAI import procesar_videoADHAI
from Hombro.CalculadorADHDD import procesar_videoADHDD
from Hombro.CalculadorADHDI import procesar_videoADHDI
from Hombro.CalculadorEDHD import procesar_videoEDHD
from Hombro.CalculadorEDHI import procesar_videoEDHI
from Hombro.CalculadorFDHD import procesar_videoFDHD
from Hombro.CalculadorFDHI import procesar_videoFDHI

app = Flask(__name__)
FCDE = CDE()
FCDP = CDP()
#Imagen
# Espalda
@app.route('/procesarCDE', methods=['POST'])
# Curvatura de espalda
def procesarCDE():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    # Lee el archivo en memoria
    image_buffer = file.read()

    # Procesa la imagen y obtiene el ángulo
    Angulo = FCDE.procesar_imagenCDE(image_buffer)

    if Angulo is None:
        return jsonify({"error": "No pose detected"}), 400

    # Devuelve solo el ángulo
    response = {
        'Angulo': Angulo
    }
    return jsonify(response)



# Piernas
@app.route('/procesarCDP', methods=['POST'])
def procesarCDP():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    # Lee el archivo en memoria
    image_buffer = file.read()

    # Procesa la imagen y obtiene los ángulos
    Angulos = FCDP.procesar_imagenCDP(image_buffer)

    if Angulos is None:
        return jsonify({"error": "No pose detected"}), 400

    # Devuelve los ángulos
    response = {
        'Angulos': Angulos
    }
    return jsonify(response)



# Video
# Rodilla
@app.route('/procesarEDRD', methods=['POST'])
# Extensión de rodilla derecha
def procesarEDRD():
    data = request.get_json()
    video_front_path = data.get('video_front_path')

    if not video_front_path:
        return jsonify({"error": "Faltan rutas de video"}), 400

    resultado = procesar_videoEDRD(video_front_path)
    return jsonify(resultado)

@app.route('/procesarEDRI', methods=['POST'])
# Extensión de rodilla izquierda
def procesarEDRI():
    data = request.get_json()
    video_front_path = data.get('video_front_path')

    if not video_front_path:
        return jsonify({"error": "Faltan rutas de video"}), 400

    resultado = procesar_videoEDRI(video_front_path)
    return jsonify(resultado)

@app.route('/procesarFDRD', methods=['POST'])
# Flexión de rodilla derecha
def procesarFDRD():
    data = request.get_json()
    video_front_path = data.get('video_front_path')

    if not video_front_path:
        return jsonify({"error": "Faltan rutas de video"}), 400

    resultado = procesar_videoFDRD(video_front_path)
    return jsonify(resultado)

@app.route('/procesarFDRI', methods=['POST'])
# Flexión de rodilla izquierda
def procesarFDRI():
    data = request.get_json()
    video_front_path = data.get('video_front_path')

    if not video_front_path:
        return jsonify({"error": "Faltan rutas de video"}), 400

    resultado = procesar_videoFDRI(video_front_path)
    return jsonify(resultado)



# Cadera
@app.route('/procesarADCDD', methods=['POST'])
# Aducción de cadera distancia derecha
def procesarADCDD():
    data = request.get_json()
    video_front_path = data.get('video_front_path')

    if not video_front_path:
        return jsonify({"error": "Faltan rutas de video"}), 400

    resultado = procesar_videoADCDD(video_front_path)
    return jsonify(resultado)

@app.route('/procesarADCDI', methods=['POST'])
# Aducción de cadera distancia izquierda
def procesarADCDI():
    data = request.get_json()
    video_front_path = data.get('video_front_path')

    if not video_front_path:
        return jsonify({"error": "Faltan rutas de video"}), 400

    resultado = procesar_videoADCDI(video_front_path)
    return jsonify(resultado)

@app.route('/procesarAYFDC', methods=['POST'])
# Aducción y flexion de cadera
def procesarAYFDC():
    data = request.get_json()
    video_front_path = data.get('video_front_path')

    if not video_front_path:
        return jsonify({"error": "Faltan rutas de video"}), 400

    resultado = procesar_videoAYFDC(video_front_path)
    return jsonify(resultado)

@app.route('/procesarEDC', methods=['POST'])
# Extensión de cadera
def procesarEDC():
    data = request.get_json()
    video_front_path = data.get('video_front_path')

    if not video_front_path:
        return jsonify({"error": "Faltan rutas de video"}), 400

    resultado = procesar_videoEDC(video_front_path)
    return jsonify(resultado)



# Codo
@app.route('/procesarEDCOD', methods=['POST'])
# Extensión de codo derecha
def procesarEDCOD():
    data = request.get_json()
    video_front_path = data.get('video_front_path')

    if not video_front_path:
        return jsonify({"error": "Faltan rutas de video"}), 400

    resultado = procesar_videoEDCOD(video_front_path)
    return jsonify(resultado)

@app.route('/procesarEDCOI', methods=['POST'])
# Extensión de codo izquierda
def procesarEDCOI():
    data = request.get_json()
    video_front_path = data.get('video_front_path')

    if not video_front_path:
        return jsonify({"error": "Faltan rutas de video"}), 400

    resultado = procesar_videoEDCOI(video_front_path)
    return jsonify(resultado)

@app.route('/procesarFDCOD', methods=['POST'])
# Flexión de codo derecha
def procesarFDCOD():
    data = request.get_json()
    video_front_path = data.get('video_front_path')

    if not video_front_path:
        return jsonify({"error": "Faltan rutas de video"}), 400

    resultado = procesar_videoFDCOD(video_front_path)
    return jsonify(resultado)

@app.route('/procesarFDCOI', methods=['POST'])
# Flexión de codo izquierda
def procesarFDCOI():
    data = request.get_json()
    video_front_path = data.get('video_front_path')

    if not video_front_path:
        return jsonify({"error": "Faltan rutas de video"}), 400

    resultado = procesar_videoFDCOI(video_front_path)
    return jsonify(resultado)



# Hombro
@app.route('/procesarADHAD', methods=['POST'])
# Aducción de hombro ángulo derecha
def procesarADHAD():
    data = request.get_json()
    video_front_path = data.get('video_front_path')

    if not video_front_path:
        return jsonify({"error": "Faltan rutas de video"}), 400

    resultado = procesar_videoADHAD(video_front_path)
    return jsonify(resultado)

@app.route('/procesarADHAI', methods=['POST'])
# Aducción de hombro ángulo izquierda
def procesarADHAI():
    data = request.get_json()
    video_front_path = data.get('video_front_path')

    if not video_front_path:
        return jsonify({"error": "Faltan rutas de video"}), 400

    resultado = procesar_videoADHAI(video_front_path)
    return jsonify(resultado)

@app.route('/procesarADHDD', methods=['POST'])
# Aducción de hombro distancia derecha
def procesarADHDD():
    data = request.get_json()
    video_front_path = data.get('video_front_path')

    if not video_front_path:
        return jsonify({"error": "Faltan rutas de video"}), 400

    resultado = procesar_videoADHDD(video_front_path)
    return jsonify(resultado)

@app.route('/procesarADHDI', methods=['POST'])
# Aducción de hombro distancia izquierda
def procesarADHDI():
    data = request.get_json()
    video_front_path = data.get('video_front_path')

    if not video_front_path:
        return jsonify({"error": "Faltan rutas de video"}), 400

    resultado = procesar_videoADHDI(video_front_path)
    return jsonify(resultado)

@app.route('/procesarEDHD', methods=['POST'])
# Extensión de hombro derecha
def procesarEDHD():
    data = request.get_json()
    video_front_path = data.get('video_front_path')

    if not video_front_path:
        return jsonify({"error": "Faltan rutas de video"}), 400

    resultado = procesar_videoEDHD(video_front_path)
    return jsonify(resultado)

@app.route('/procesarEDHI', methods=['POST'])
# Extensión de hombro derecha
def procesarEDHI():
    data = request.get_json()
    video_front_path = data.get('video_front_path')

    if not video_front_path:
        return jsonify({"error": "Faltan rutas de video"}), 400

    resultado = procesar_videoEDHI(video_front_path)
    return jsonify(resultado)

@app.route('/procesarFDHD', methods=['POST'])
# Flexión de hombro derecha
def procesarFDHD():
    data = request.get_json()
    video_front_path = data.get('video_front_path')

    if not video_front_path:
        return jsonify({"error": "Faltan rutas de video"}), 400

    resultado = procesar_videoFDHD(video_front_path)
    return jsonify(resultado)

@app.route('/procesarFDHI', methods=['POST'])
# Flexión de hombro izquierda
def procesarFDHI():
    data = request.get_json()
    video_front_path = data.get('video_front_path')

    if not video_front_path:
        return jsonify({"error": "Faltan rutas de video"}), 400

    resultado = procesar_videoFDHI(video_front_path)
    return jsonify(resultado)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=2000)