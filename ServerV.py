from flask import Flask, request, jsonify
import os
from CalculoMCH import procesar_videoMCH
from CalculoCHA import procesar_videoCHA
from CalculoACR import procesar_videoACR
from CalculoCRT import procesar_videoCRT

app = Flask(__name__)

@app.route('/procesarMCH', methods=['POST'])
def procesarMCH():
    data = request.get_json()
    video_front_path = data.get('video_front_path')
    video_side_path = data.get('video_side_path')

    if not video_front_path or not video_side_path:
        return jsonify({"error": "Faltan rutas de video"}), 400

    resultado = procesar_videoMCH(video_front_path, video_side_path)
    return jsonify(resultado)

@app.route('/procesarCHA', methods=['POST'])
def procesarCHA():
    data = request.get_json()
    video_front_path = data.get('video_front_path')
    video_side_path = data.get('video_side_path')

    if not video_front_path or not video_side_path:
        return jsonify({"error": "Faltan rutas de video"}), 400

    resultado = procesar_videoCHA(video_front_path, video_side_path)
    return jsonify(resultado)

@app.route('/procesarACR', methods=['POST'])
def procesar():
    data = request.get_json()
    video_front_path = data.get('video_front_path')
    video_side_path = data.get('video_side_path')

    if not video_front_path or not video_side_path:
        return jsonify({"error": "Faltan rutas de video"}), 400

    resultado = procesar_videoACR(video_front_path, video_side_path)
    return jsonify(resultado)

@app.route('/procesarCRT', methods=['POST'])
def analizar():
    data = request.json
    video_front_path = data.get('video_front_path')
    video_side_path = data.get('video_side_path')

    if not video_front_path or not video_side_path:
        return jsonify({"error": "Rutas de video no proporcionadas"}), 400
        
    resultado = procesar_videoCRT(video_front_path, video_side_path)
    return jsonify(resultado)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=2000)
