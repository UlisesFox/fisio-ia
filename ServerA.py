from flask import Flask, request, jsonify
from CalculoEspaldaA import AutoDocPostura
from CalculoPiernasA import AutoDocMovimiento

app = Flask(__name__)
auto_doc = AutoDocPostura()
auto_doc2 = AutoDocMovimiento()

@app.route('/server/autodoc_postura', methods=['POST'])
def autodoc_postura():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    # Lee el archivo en memoria
    image_buffer = file.read()

    # Procesa la imagen y obtiene el ángulo
    angle = auto_doc.procesar_imagen(image_buffer)

    if angle is None:
        return jsonify({"error": "No pose detected"}), 400

    # Devuelve solo el ángulo
    response = {
        'angle': angle
    }
    return jsonify(response)

@app.route('/server/autodoc_movimiento', methods=['POST'])
def autodoc_movimiento():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    # Lee el archivo en memoria
    image_buffer = file.read()

    # Procesa la imagen y obtiene los ángulos
    angulos = auto_doc2.procesar_imagen(image_buffer)

    if angulos is None:
        return jsonify({"error": "No pose detected"}), 400

    # Devuelve los ángulos
    response = {
        'angle': angulos,
    }
    return jsonify(response)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
