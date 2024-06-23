from flask import Flask, request, send_file
from CalculoEspaldaI import AutoDocPostura
from CalculoPiernasI import AutoDocMovimiento
import io

app = Flask(__name__)
auto_doc = AutoDocPostura()
auto_doc2 = AutoDocMovimiento()

@app.route('/server/autodoc_postura', methods=['POST'])
def autodoc_postura():
    if 'file' not in request.files:
        return "No file part", 400
    file = request.files['file']
    if file.filename == '':
        return "No selected file", 400

    # Lee el archivo en memoria
    image_buffer = file.read()

    # Procesa la imagen
    processed_image = auto_doc.procesar_imagen(image_buffer)

    # Devuelve la imagen procesada
    return send_file(io.BytesIO(processed_image), mimetype='image/jpeg')

@app.route('/server/autodoc_movimiento', methods=['POST'])
def autodoc_movimiento():
    if 'file' not in request.files:
        return "No file part", 400
    file = request.files['file']
    if file.filename == '':
        return "No selected file", 400

    # Lee el archivo en memoria
    image_buffer = file.read()

    # Procesa la imagen y obtiene la imagen con puntos marcados
    imagen_procesada = auto_doc2.procesar_imagen(image_buffer)

    # Devuelve la imagen procesada
    return send_file(io.BytesIO(imagen_procesada), mimetype='image/jpeg')

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
