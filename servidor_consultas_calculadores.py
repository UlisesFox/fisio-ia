from flask import Flask, request, jsonify
from Espalda_Calculador.curvatura_espalda_angulo import curvatura_espalda
from Piernas_Calculador.curvatura_piernas_angulo import curvatura_piernas
from Rodilla_Calculador.extension_rodilla_angulo_derecha import procesar_video_extension_rodilla_angulo_derecha
from Rodilla_Calculador.extension_rodilla_angulo_izquierda import procesar_video_extension_rodilla_angulo_izquierda
from Rodilla_Calculador.flexion_rodilla_angulo_derecha import procesar_video_flexion_rodilla_angulo_derecha
from Rodilla_Calculador.flexion_rodilla_angulo_izquierda import procesar_video_flexion_rodilla_angulo_izquierda
from Cadera_Calculador.aduccion_cadera_distancia_derecha import procesar_video_aduccion_cadera_distancia_derecha
from Cadera_Calculador.aduccion_cadera_distancia_izquierda import procesar_video_aduccion_cadera_distancia_izquierda
from Cadera_Calculador.aduccion_flexion_cadera_angulo import procesar_video_aduccion_flexion_cadera_angulo
from Cadera_Calculador.extension_cadera_distancia import procesar_video_extension_cadera_distancia
from Codo_Calculador.extension_codo_angulo_derecha import procesar_video_extension_codo_angulo_derecha
from Codo_Calculador.extension_codo_angulo_izquierda import procesar_video_extension_codo_angulo_izquierda
from Codo_Calculador.flexion_codo_angulo_derecha import procesar_video_flexion_codo_angulo_derecha
from Codo_Calculador.flexion_codo_angulo_izquierda import procesar_video_flexion_codo_angulo_izquierda
from Hombro_Calculador.aduccion_hombro_angulo_derecha import procesar_video_aduccion_hombro_angulo_derecha
from Hombro_Calculador.aduccion_hombro_angulo_izquierda import procesar_video_aduccion_hombro_angulo_izquierda
from Hombro_Calculador.aduccion_hombro_distancia_derecha import procesar_video_aduccion_hombro_distancia_derecha
from Hombro_Calculador.aduccion_hombro_distancia_izquierda import procesar_video_aduccion_hombro_distancia_izquierda
from Hombro_Calculador.extension_hombro_distancia_derecha import procesar_video_extension_hombro_distancia_derecha
from Hombro_Calculador.extension_hombro_distancia_izquierda import procesar_video_extension_hombro_distancia_izquierda
from Hombro_Calculador.flexion_hombro_distancia_derecha import procesar_video_flexion_hombro_distancia_derecha
from Hombro_Calculador.flexion_hombro_distancia_izquierda import procesar_video_flexion_hombro_distancia_izquierda

app = Flask(__name__)

# Instancias de las clases calculadoras
curvatura_espalda_calculador = curvatura_espalda()
curvatura_piernas_calculador = curvatura_piernas()

# Funciones comunes para manejo de imagenes
def procesar_imagen(request):
    if 'imagen' not in request.files:
        return None, "No hay imagen", 400
    imagen = request.files['imagen']
    if imagen.filename == '':
        return None, "No se seleccionó imagen", 400
    return imagen.read(), None, 200

def procesar_video(request):
    if 'video' not in request.files:
        return None, "No hay video", 400
    video = request.files['video']
    if video.filename == '':
        return None, "No se seleccionó video", 400
    return video.read(), None, 200

# Procesamiento de imágenes
@app.route('/CurvaturaEspalda', methods=['POST'])
def CurvaturaEspalda():
    imagen, error, status_code = procesar_imagen(request)
    if error:
        return jsonify({"error": error}), status_code
    
    resultado = curvatura_espalda_calculador.procesar_imagen(imagen)
    if resultado is None:
        return jsonify({"error": "No se detectó el movimiento"}), 400

    return jsonify({'Angulo': resultado}), 200

@app.route('/CurvaturaPiernas', methods=['POST'])
def CurvaturaPiernas():
    imagen, error, status_code = procesar_imagen(request)
    if error:
        return jsonify({"error": error}), status_code
    
    resultado = curvatura_piernas_calculador.procesar_imagen(imagen)
    if resultado is None:
        return jsonify({"error": "No se detectó el movimiento"}), 400

    return jsonify({'Angulo': resultado}), 200

# Procesamiento de videos
@app.route('/ExtensionRodillaDerecha', methods=['POST'])
def ExtensionRodillaDerecha():
    video, error, status_code = procesar_video(request)
    if error:
        return jsonify({"error": error}), status_code
    
    resultado = procesar_video_extension_rodilla_angulo_derecha(video)
    if resultado is None:
        return jsonify({"error": "No se detectó el movimiento"}), 400
    
    return jsonify(resultado), 200

@app.route('/ExtensionRodillaIzquierda', methods=['POST'])
def ExtensionRodillaIzquierda():
    video, error, status_code = procesar_video(request)
    if error:
        return jsonify({"error": error}), status_code
    
    resultado = procesar_video_extension_rodilla_angulo_izquierda(video)
    if resultado is None:
        return jsonify({"error": "No se detectó el movimiento"}), 400
    
    return jsonify(resultado), 200

@app.route('/FlexionRodillaDerecha', methods=['POST'])
def FlexionRodillaDerecha():
    video, error, status_code = procesar_video(request)
    if error:
        return jsonify({"error": error}), status_code
    
    resultado = procesar_video_flexion_rodilla_angulo_derecha(video)
    if resultado is None:
        return jsonify({"error": "No se detectó el movimiento"}), 400
    
    return jsonify(resultado), 200

@app.route('/FlexionRodillaIzquierda', methods=['POST'])
def FlexionRodillaIzquierda():
    video, error, status_code = procesar_video(request)
    if error:
        return jsonify({"error": error}), status_code
    
    resultado = procesar_video_flexion_rodilla_angulo_izquierda(video)
    if resultado is None:
        return jsonify({"error": "No se detectó el movimiento"}), 400
    
    return jsonify(resultado), 200

@app.route('/AbduccionCadera', methods=['POST'])
def AbduccionCadera():
    video, error, status_code = procesar_video(request)
    if error:
        return jsonify({"error": error}), status_code
    
    resultado = procesar_video_aduccion_flexion_cadera_angulo(video)
    if resultado is None:
        return jsonify({"error": "No se detectó el movimiento"}), 400
    
    return jsonify(resultado), 200

@app.route('/AduccionCaderaDerecha', methods=['POST'])
def AduccionCaderaDerecha():
    video, error, status_code = procesar_video(request)
    if error:
        return jsonify({"error": error}), status_code
    
    resultado = procesar_video_aduccion_cadera_distancia_derecha(video)
    if resultado is None:
        return jsonify({"error": "No se detectó el movimiento"}), 400
    
    return jsonify(resultado), 200

@app.route('/AduccionCaderaIzquierda', methods=['POST'])
def AduccionCaderaIzquierda():
    video, error, status_code = procesar_video(request)
    if error:
        return jsonify({"error": error}), status_code
    
    resultado = procesar_video_aduccion_cadera_distancia_izquierda(video)
    if resultado is None:
        return jsonify({"error": "No se detectó el movimiento"}), 400
    
    return jsonify(resultado), 200

@app.route('/FlexionCadera', methods=['POST'])
def FlexionCadera():
    video, error, status_code = procesar_video(request)
    if error:
        return jsonify({"error": error}), status_code
    
    resultado = procesar_video_aduccion_flexion_cadera_angulo(video)
    if resultado is None:
        return jsonify({"error": "No se detectó el movimiento"}), 400
    
    return jsonify(resultado), 200

@app.route('/ExtensionCadera', methods=['POST'])
def ExtensionCadera():
    video, error, status_code = procesar_video(request)
    if error:
        return jsonify({"error": error}), status_code
    
    resultado = procesar_video_extension_cadera_distancia(video)
    if resultado is None:
        return jsonify({"error": "No se detectó el movimiento"}), 400
    
    return jsonify(resultado), 200

@app.route('/ExtensionCodoDerecha', methods=['POST'])
def ExtensionCodoDerecha():
    video, error, status_code = procesar_video(request)
    if error:
        return jsonify({"error": error}), status_code
    
    resultado = procesar_video_extension_codo_angulo_derecha(video)
    if resultado is None:
        return jsonify({"error": "No se detectó el movimiento"}), 400
    
    return jsonify(resultado), 200

@app.route('/ExtensionCodoIzquierda', methods=['POST'])
def ExtensionCodoIzquierda():
    video, error, status_code = procesar_video(request)
    if error:
        return jsonify({"error": error}), status_code
    
    resultado = procesar_video_extension_codo_angulo_izquierda(video)
    if resultado is None:
        return jsonify({"error": "No se detectó el movimiento"}), 400
    
    return jsonify(resultado), 200

@app.route('/FlexionCodoDerecha', methods=['POST'])
def FlexionCodoDerecha():
    video, error, status_code = procesar_video(request)
    if error:
        return jsonify({"error": error}), status_code
    
    resultado = procesar_video_flexion_codo_angulo_derecha(video)
    if resultado is None:
        return jsonify({"error": "No se detectó el movimiento"}), 400
    
    return jsonify(resultado), 200

@app.route('/FlexionCodoIzquierda', methods=['POST'])
def FlexionCodoIzquierda():
    video, error, status_code = procesar_video(request)
    if error:
        return jsonify({"error": error}), status_code
    
    resultado = procesar_video_flexion_codo_angulo_izquierda(video)
    if resultado is None:
        return jsonify({"error": "No se detectó el movimiento"}), 400
    
    return jsonify(resultado), 200

@app.route('/AbduccionHombroDerecha', methods=['POST'])
def AbduccionHombroDerecha():
    video, error, status_code = procesar_video(request)
    if error:
        return jsonify({"error": error}), status_code
    
    resultado = procesar_video_aduccion_hombro_angulo_derecha(video)
    if resultado is None:
        return jsonify({"error": "No se detectó el movimiento"}), 400
    
    return jsonify(resultado), 200

@app.route('/AbduccionHombroIzquierda', methods=['POST'])
def AbduccionHombroIzquierda():
    video, error, status_code = procesar_video(request)
    if error:
        return jsonify({"error": error}), status_code
    
    resultado = procesar_video_aduccion_hombro_angulo_izquierda(video)
    if resultado is None:
        return jsonify({"error": "No se detectó el movimiento"}), 400
    
    return jsonify(resultado), 200

@app.route('/AduccionHombroDerecha', methods=['POST'])
def AduccionHombroDerecha():
    video, error, status_code = procesar_video(request)
    if error:
        return jsonify({"error": error}), status_code
    
    resultado = procesar_video_aduccion_hombro_distancia_derecha(video)
    if resultado is None:
        return jsonify({"error": "No se detectó el movimiento"}), 400
    
    return jsonify(resultado), 200

@app.route('/AduccionHombroIzquierda', methods=['POST'])
def AduccionHombroIzquierda():
    video, error, status_code = procesar_video(request)
    if error:
        return jsonify({"error": error}), status_code
    
    resultado = procesar_video_aduccion_hombro_distancia_izquierda(video)
    if resultado is None:
        return jsonify({"error": "No se detectó el movimiento"}), 400
    
    return jsonify(resultado), 200

@app.route('/ExtensionHombroDerecha', methods=['POST'])
def ExtensionHombroDerecha():
    video, error, status_code = procesar_video(request)
    if error:
        return jsonify({"error": error}), status_code
    
    resultado = procesar_video_extension_hombro_distancia_derecha(video)
    if resultado is None:
        return jsonify({"error": "No se detectó el movimiento"}), 400
    
    return jsonify(resultado), 200

@app.route('/ExtensionHombroIzquierda', methods=['POST'])
def ExtensionHombroIzquierda():
    video, error, status_code = procesar_video(request)
    if error:
        return jsonify({"error": error}), status_code
    
    resultado = procesar_video_extension_hombro_distancia_izquierda(video)
    if resultado is None:
        return jsonify({"error": "No se detectó el movimiento"}), 400
    
    return jsonify(resultado), 200

@app.route('/FlexionHombroDerecha', methods=['POST'])
def FlexionHombroDerecha():
    video, error, status_code = procesar_video(request)
    if error:
        return jsonify({"error": error}), status_code
    
    resultado = procesar_video_flexion_hombro_distancia_derecha(video)
    if resultado is None:
        return jsonify({"error": "No se detectó el movimiento"}), 400
    
    return jsonify(resultado), 200

@app.route('/FlexionHombroIzquierda', methods=['POST'])
def FlexionHombroIzquierda():
    video, error, status_code = procesar_video(request)
    if error:
        return jsonify({"error": error}), status_code
    
    resultado = procesar_video_flexion_hombro_distancia_izquierda(video)
    if resultado is None:
        return jsonify({"error": "No se detectó el movimiento"}), 400
    
    return jsonify(resultado), 200

@app.route('/vivo', methods=['POST'])
def vivo():

    respuesta = "si los estoy escuchando"
    
    return jsonify(respuesta)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)