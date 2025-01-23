from flask import Flask, request, jsonify
from Espalda_Calculador.curvatura_espalda_angulo import curvatura_espalda
from Piernas_Calculador.curvatura_piernas_angulo import curvatura_piernas
from Rodilla_Calculador.extension_rodilla_angulo_derecha import procesar_video_extension_rodilla_angulo_derecha
from Rodilla_Calculador.extension_rodilla_angulo_izquierda import procesar_video_extension_rodilla_angulo_izquierda
from Rodilla_Calculador.flexion_rodilla_angulo_derecha import procesar_video_flexion_rodilla_angulo_derecha
from Rodilla_Calculador.flexion_rodilla_angulo_izquierda import procesar_video_flexion_rodilla_angulo_izquierda
from Cadera_Calculador.abduccion_cadera_angulo_derecha import procesar_video_abduccion_cadera_angulo_derecha
from Cadera_Calculador.abduccion_cadera_angulo_izquierda import procesar_video_abduccion_cadera_angulo_izquierda
from Cadera_Calculador.aduccion_cadera_distancia_derecha import procesar_video_aduccion_cadera_distancia_derecha
from Cadera_Calculador.aduccion_cadera_distancia_izquierda import procesar_video_aduccion_cadera_distancia_izquierda
from Cadera_Calculador.extension_cadera_angulo_derecha import procesar_video_extension_cadera_angulo_derecha
from Cadera_Calculador.extension_cadera_angulo_izquierda import procesar_video_extension_cadera_angulo_izquierda
from Cadera_Calculador.flexion_cadera_angulo_derecha import procesar_video_flexion_cadera_angulo_derecha
from Cadera_Calculador.flexion_cadera_angulo_izquierda import procesar_video_flexion_cadera_angulo_izquierda
from Codo_Calculador.extension_codo_angulo_derecha import procesar_video_extension_codo_angulo_derecha
from Codo_Calculador.extension_codo_angulo_izquierda import procesar_video_extension_codo_angulo_izquierda
from Codo_Calculador.flexion_codo_angulo_derecha import procesar_video_flexion_codo_angulo_derecha
from Codo_Calculador.flexion_codo_angulo_izquierda import procesar_video_flexion_codo_angulo_izquierda
from Hombro_Calculador.abduccion_hombro_angulo_derecha import procesar_video_abduccion_hombro_angulo_derecha
from Hombro_Calculador.abduccion_hombro_angulo_izquierda import procesar_video_abduccion_hombro_angulo_izquierda
from Hombro_Calculador.aduccion_hombro_angulo_derecha import procesar_video_aduccion_hombro_angulo_derecha
from Hombro_Calculador.aduccion_hombro_angulo_izquierda import procesar_video_aduccion_hombro_angulo_izquierda
from Hombro_Calculador.extension_hombro_angulo_derecha import procesar_video_extension_hombro_angulo_derecha
from Hombro_Calculador.extension_hombro_angulo_izquierda import procesar_video_extension_hombro_angulo_izquierda
from Hombro_Calculador.flexion_hombro_angulo_derecha import procesar_video_flexion_hombro_angulo_derecha
from Hombro_Calculador.flexion_hombro_angulo_izquierda import procesar_video_flexion_hombro_angulo_izquierda

app = Flask(__name__)

# Instancias de las clases calculadoras
curvatura_espalda_calculador = curvatura_espalda()
curvatura_piernas_calculador = curvatura_piernas()

# Funciones comunes para manejo de imagenes
def procesar_imagen(request):
    if 'dato' not in request.files:
        return None, "No hay imagen", 400
    imagen = request.files['dato']
    if imagen.filename == '':
        return None, "No se seleccionó imagen", 400
    return imagen.read(), None, 200

def procesar_video(request):
    if 'dato' not in request.files:
        return None, "No hay video", 400
    video = request.files['dato']
    if video.filename == '':
        return None, "No se seleccionó video", 400
    return video.read(), None, 200

# Procesamiento de imágenes
@app.route('/curvaturaEspalda', methods=['POST'])
def CurvaturaEspalda():
    tipo = "angulo"
    desde = "hombros"
    imagen, error, status_code = procesar_imagen(request)
    if error:
        return jsonify({"error": error}), status_code

    resultado = curvatura_espalda_calculador.procesar_imagen(imagen)
    if resultado is None:
        return jsonify({"error": "No se detectó el movimiento"}), 400

    return jsonify({'response': resultado, 'tipo': tipo, 'desde': desde}), 200

@app.route('/curvaturaPiernas', methods=['POST'])
def CurvaturaPiernas():
    tipo = "angulo"
    desde = "rodillas"
    imagen, error, status_code = procesar_imagen(request)
    if error:
        return jsonify({"error": error}), status_code
    
    resultado = curvatura_piernas_calculador.procesar_imagen(imagen)
    if resultado is None:
        return jsonify({"error": "No se detectó el movimiento"}), 400

    return jsonify({'response': resultado, 'tipo': tipo, 'desde': desde}), 200

# Procesamiento de videos
@app.route('/extensionRodillaDerecha', methods=['POST'])
def ExtensionRodillaDerecha():
    video, error, status_code = procesar_video(request)
    if error:
        return jsonify({"error": error}), status_code
    
    resultado = procesar_video_extension_rodilla_angulo_derecha(video)
    if resultado is None:
        return jsonify({"error": "No se detectó el movimiento"}), 400
    
    return jsonify(resultado), 200

@app.route('/extensionRodillaIzquierda', methods=['POST'])
def ExtensionRodillaIzquierda():
    video, error, status_code = procesar_video(request)
    if error:
        return jsonify({"error": error}), status_code
    
    resultado = procesar_video_extension_rodilla_angulo_izquierda(video)
    if resultado is None:
        return jsonify({"error": "No se detectó el movimiento"}), 400
    
    return jsonify(resultado), 200

@app.route('/flexionRodillaDerecha', methods=['POST'])
def FlexionRodillaDerecha():
    video, error, status_code = procesar_video(request)
    if error:
        return jsonify({"error": error}), status_code
    
    resultado = procesar_video_flexion_rodilla_angulo_derecha(video)
    if resultado is None:
        return jsonify({"error": "No se detectó el movimiento"}), 400
    
    return jsonify(resultado), 200

@app.route('/flexionRodillaIzquierda', methods=['POST'])
def FlexionRodillaIzquierda():
    video, error, status_code = procesar_video(request)
    if error:
        return jsonify({"error": error}), status_code
    
    resultado = procesar_video_flexion_rodilla_angulo_izquierda(video)
    if resultado is None:
        return jsonify({"error": "No se detectó el movimiento"}), 400
    
    return jsonify(resultado), 200

@app.route('/abduccionCaderaDerecha', methods=['POST'])
def AbduccionCaderaDerecha():
    video, error, status_code = procesar_video(request)
    if error:
        return jsonify({"error": error}), status_code
    
    resultado = procesar_video_abduccion_cadera_angulo_derecha(video)
    if resultado is None:
        return jsonify({"error": "No se detectó el movimiento"}), 400
    
    return jsonify(resultado), 200

@app.route('/abduccionCaderaIzquierda', methods=['POST'])
def AbduccionCaderaIzquierda():
    video, error, status_code = procesar_video(request)
    if error:
        return jsonify({"error": error}), status_code
    
    resultado = procesar_video_abduccion_cadera_angulo_izquierda(video)
    if resultado is None:
        return jsonify({"error": "No se detectó el movimiento"}), 400
    
    return jsonify(resultado), 200

@app.route('/aduccionCaderaDerecha', methods=['POST'])
def AduccionCaderaDerecha():
    video, error, status_code = procesar_video(request)
    if error:
        return jsonify({"error": error}), status_code
    
    resultado = procesar_video_aduccion_cadera_distancia_derecha(video)
    if resultado is None:
        return jsonify({"error": "No se detectó el movimiento"}), 400
    
    return jsonify(resultado), 200

@app.route('/aduccionCaderaIzquierda', methods=['POST'])
def AduccionCaderaIzquierda():
    video, error, status_code = procesar_video(request)
    if error:
        return jsonify({"error": error}), status_code
    
    resultado = procesar_video_aduccion_cadera_distancia_izquierda(video)
    if resultado is None:
        return jsonify({"error": "No se detectó el movimiento"}), 400
    
    return jsonify(resultado), 200

@app.route('/extensionCaderaDerecha', methods=['POST'])
def ExtensionCaderaDerecha():
    video, error, status_code = procesar_video(request)
    if error:
        return jsonify({"error": error}), status_code
    
    resultado = procesar_video_extension_cadera_angulo_derecha(video)
    if resultado is None:
        return jsonify({"error": "No se detectó el movimiento"}), 400
    
    return jsonify(resultado), 200

@app.route('/extensionCaderaIzquierda', methods=['POST'])
def ExtensionCaderaIzquierda():
    video, error, status_code = procesar_video(request)
    if error:
        return jsonify({"error": error}), status_code
    
    resultado = procesar_video_extension_cadera_angulo_izquierda(video)
    if resultado is None:
        return jsonify({"error": "No se detectó el movimiento"}), 400
    
    return jsonify(resultado), 200

@app.route('/flexionCaderaDerecha', methods=['POST'])
def FlexionCaderaDerecha():
    video, error, status_code = procesar_video(request)
    if error:
        return jsonify({"error": error}), status_code
    
    resultado = procesar_video_flexion_cadera_angulo_derecha(video)
    if resultado is None:
        return jsonify({"error": "No se detectó el movimiento"}), 400
    
    return jsonify(resultado), 200

@app.route('/flexionCaderaIzquierda', methods=['POST'])
def FlexionCaderaIzquierda():
    video, error, status_code = procesar_video(request)
    if error:
        return jsonify({"error": error}), status_code
    
    resultado = procesar_video_flexion_cadera_angulo_izquierda(video)
    if resultado is None:
        return jsonify({"error": "No se detectó el movimiento"}), 400
    
    return jsonify(resultado), 200

@app.route('/extensionCodoDerecha', methods=['POST'])
def ExtensionCodoDerecha():
    video, error, status_code = procesar_video(request)
    if error:
        return jsonify({"error": error}), status_code
    
    resultado = procesar_video_extension_codo_angulo_derecha(video)
    if resultado is None:
        return jsonify({"error": "No se detectó el movimiento"}), 400
    
    return jsonify(resultado), 200

@app.route('/extensionCodoIzquierda', methods=['POST'])
def ExtensionCodoIzquierda():
    video, error, status_code = procesar_video(request)
    if error:
        return jsonify({"error": error}), status_code
    
    resultado = procesar_video_extension_codo_angulo_izquierda(video)
    if resultado is None:
        return jsonify({"error": "No se detectó el movimiento"}), 400
    
    return jsonify(resultado), 200

@app.route('/flexionCodoDerecha', methods=['POST'])
def FlexionCodoDerecha():
    video, error, status_code = procesar_video(request)
    if error:
        return jsonify({"error": error}), status_code
    
    resultado = procesar_video_flexion_codo_angulo_derecha(video)
    if resultado is None:
        return jsonify({"error": "No se detectó el movimiento"}), 400
    
    return jsonify(resultado), 200

@app.route('/flexionCodoIzquierda', methods=['POST'])
def FlexionCodoIzquierda():
    video, error, status_code = procesar_video(request)
    if error:
        return jsonify({"error": error}), status_code
    
    resultado = procesar_video_flexion_codo_angulo_izquierda(video)
    if resultado is None:
        return jsonify({"error": "No se detectó el movimiento"}), 400
    
    return jsonify(resultado), 200

@app.route('/abduccionHombroDerecha', methods=['POST'])
def AbduccionHombroDerecha():
    video, error, status_code = procesar_video(request)
    if error:
        return jsonify({"error": error}), status_code
    
    resultado = procesar_video_abduccion_hombro_angulo_derecha(video)
    if resultado is None:
        return jsonify({"error": "No se detectó el movimiento"}), 400
    
    return jsonify(resultado), 200

@app.route('/abduccionHombroIzquierda', methods=['POST'])
def AbduccionHombroIzquierda():
    video, error, status_code = procesar_video(request)
    if error:
        return jsonify({"error": error}), status_code
    
    resultado = procesar_video_abduccion_hombro_angulo_izquierda(video)
    if resultado is None:
        return jsonify({"error": "No se detectó el movimiento"}), 400
    
    return jsonify(resultado), 200

@app.route('/aduccionHombroDerecha', methods=['POST'])
def AduccionHombroDerecha():
    video, error, status_code = procesar_video(request)
    if error:
        return jsonify({"error": error}), status_code
    
    resultado = procesar_video_aduccion_hombro_angulo_derecha(video)
    if resultado is None:
        return jsonify({"error": "No se detectó el movimiento"}), 400
    
    return jsonify(resultado), 200

@app.route('/aduccionHombroIzquierda', methods=['POST'])
def AduccionHombroIzquierda():
    video, error, status_code = procesar_video(request)
    if error:
        return jsonify({"error": error}), status_code
    
    resultado = procesar_video_aduccion_hombro_angulo_izquierda(video)
    if resultado is None:
        return jsonify({"error": "No se detectó el movimiento"}), 400
    
    return jsonify(resultado), 200

@app.route('/extensionHombroDerecha', methods=['POST'])
def ExtensionHombroDerecha():
    video, error, status_code = procesar_video(request)
    if error:
        return jsonify({"error": error}), status_code
    
    resultado = procesar_video_extension_hombro_angulo_derecha(video)
    if resultado is None:
        return jsonify({"error": "No se detectó el movimiento"}), 400
    
    return jsonify(resultado), 200

@app.route('/extensionHombroIzquierda', methods=['POST'])
def ExtensionHombroIzquierda():
    video, error, status_code = procesar_video(request)
    if error:
        return jsonify({"error": error}), status_code
    
    resultado = procesar_video_extension_hombro_angulo_izquierda(video)
    if resultado is None:
        return jsonify({"error": "No se detectó el movimiento"}), 400
    
    return jsonify(resultado), 200

@app.route('/flexionHombroDerecha', methods=['POST'])
def FlexionHombroDerecha():
    video, error, status_code = procesar_video(request)
    if error:
        return jsonify({"error": error}), status_code
    
    resultado = procesar_video_flexion_hombro_angulo_derecha(video)
    if resultado is None:
        return jsonify({"error": "No se detectó el movimiento"}), 400
    
    return jsonify(resultado), 200

@app.route('/flexionHombroIzquierda', methods=['POST'])
def FlexionHombroIzquierda():
    video, error, status_code = procesar_video(request)
    if error:
        return jsonify({"error": error}), status_code
    
    resultado = procesar_video_flexion_hombro_angulo_izquierda(video)
    if resultado is None:
        return jsonify({"error": "No se detectó el movimiento"}), 400
    
    return jsonify(resultado), 200

@app.route('/vivo', methods=['POST'])
def vivo():

    respuesta = "si los estoy escuchando"
    
    return jsonify(respuesta)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)