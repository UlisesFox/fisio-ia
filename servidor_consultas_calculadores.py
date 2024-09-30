from flask import Flask, request, jsonify
import os
from Espalda_Calculador.curvatura_espalda_angulo import CurvaturaEspalda
from Piernas_Calculador.curvatura_piernas_angulo import CurvaturaPiernas
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
curvatura_espalda_calculador = CurvaturaEspalda()
curvatura_piernas_calculador = CurvaturaPiernas()

# Funciones comunes para manejo de imagenes
def manejar_imagen_imagen(request):
    if 'imagen' not in request.files:
        return None, "No hay imagen", 400
    imagen = request.files['imagen']
    if imagen.filename == '':
        return None, "No se seleccionó imagen", 400
    return imagen.read(), None, 200

def procesar_video_endpoint(funcion_procesar_video, video):
    if not video:
        return {"error": "Falta la ruta del video"}, 400
    resultado = funcion_procesar_video(video)
    return resultado, 200

# Procesamiento de imágenes
@app.route('/procesar_curvatura_espalda', methods=['POST'])
def procesar_curvatura_espalda():
    imagen, error, status_code = manejar_imagen_imagen(request)
    if error:
        return jsonify({"error": error}), status_code
    
    angulo = curvatura_espalda_calculador.procesar_imagen(imagen)
    if angulo is None:
        return jsonify({"error": "No se detectó el movimiento"}), 400

    return jsonify({'Angulo': angulo}), 200

@app.route('/procesar_curvatura_piernas', methods=['POST'])
def procesar_curvatura_piernas():
    imagen, error, status_code = manejar_imagen_imagen(request)
    if error:
        return jsonify({"error": error}), status_code
    
    angulo = curvatura_piernas_calculador.procesar_imagen(imagen)
    if angulo is None:
        return jsonify({"error": "No se detectó el movimiento"}), 400

    return jsonify({'Angulo': angulo}), 200

# Procesamiento de videos
@app.route('/procesar_extension_rodilla_angulo_derecha', methods=['POST'])
def procesar_extension_rodilla_derecha():
    dato = request.get_json()
    video = dato.get('video')
    resultado, status_code = procesar_video_endpoint(procesar_video_extension_rodilla_angulo_derecha, video)
    return jsonify(resultado), status_code

@app.route('/procesar_extension_rodilla_angulo_izquierda', methods=['POST'])
def procesar_extension_rodilla_izquierda():
    dato = request.get_json()
    video = dato.get('video')
    resultado, status_code = procesar_video_endpoint(procesar_video_extension_rodilla_angulo_izquierda, video)
    return jsonify(resultado), status_code

@app.route('/procesar_flexion_rodilla_angulo_derecha', methods=['POST'])
def procesar_flexion_rodilla_derecha():
    dato = request.get_json()
    video = dato.get('video')
    resultado, status_code = procesar_video_endpoint(procesar_video_flexion_rodilla_angulo_derecha, video)
    return jsonify(resultado), status_code

@app.route('/procesar_flexion_rodilla_angulo_izquierda', methods=['POST'])
def procesar_flexion_rodilla_izquierda():
    dato = request.get_json()
    video = dato.get('video')
    resultado, status_code = procesar_video_endpoint(procesar_video_flexion_rodilla_angulo_izquierda, video)
    return jsonify(resultado), status_code

@app.route('/procesar_aduccion_cadera_distancia_derecha', methods=['POST'])
def procesar_aduccion_cadera_derecha():
    dato = request.get_json()
    video = dato.get('video')
    resultado, status_code = procesar_video_endpoint(procesar_video_aduccion_cadera_distancia_derecha, video)
    return jsonify(resultado), status_code

@app.route('/procesar_aduccion_cadera_distancia_izquierda', methods=['POST'])
def procesar_aduccion_cadera_izquierda():
    dato = request.get_json()
    video = dato.get('video')
    resultado, status_code = procesar_video_endpoint(procesar_video_aduccion_cadera_distancia_izquierda, video)
    return jsonify(resultado), status_code

@app.route('/procesar_aduccion_flexion_cadera', methods=['POST'])
def procesar_aduccion_flexion_cadera():
    dato = request.get_json()
    video = dato.get('video')
    resultado, status_code = procesar_video_endpoint(procesar_video_aduccion_flexion_cadera_angulo, video)
    return jsonify(resultado), status_code

@app.route('/procesar_extension_cadera', methods=['POST'])
def procesar_extension_cadera():
    dato = request.get_json()
    video = dato.get('video')
    resultado, status_code = procesar_video_endpoint(procesar_video_extension_cadera_distancia, video)
    return jsonify(resultado), status_code

@app.route('/procesar_extension_codo_angulo_derecha', methods=['POST'])
def procesar_extension_codo_derecha():
    dato = request.get_json()
    video = dato.get('video')
    resultado, status_code = procesar_video_endpoint(procesar_video_extension_codo_angulo_derecha, video)
    return jsonify(resultado), status_code

@app.route('/procesar_extension_codo_angulo_izquierda', methods=['POST'])
def procesar_extension_codo_izquierda():
    dato = request.get_json()
    video = dato.get('video')
    resultado, status_code = procesar_video_endpoint(procesar_video_extension_codo_angulo_izquierda, video)
    return jsonify(resultado), status_code

@app.route('/procesar_flexion_codo_angulo_derecha', methods=['POST'])
def procesar_flexion_codo_derecha():
    dato = request.get_json()
    video = dato.get('video')
    resultado, status_code = procesar_video_endpoint(procesar_video_flexion_codo_angulo_derecha, video)
    return jsonify(resultado), status_code

@app.route('/procesar_flexion_codo_angulo_izquierda', methods=['POST'])
def procesar_flexion_codo_izquierda():
    dato = request.get_json()
    video = dato.get('video')
    resultado, status_code = procesar_video_endpoint(procesar_video_flexion_codo_angulo_izquierda, video)
    return jsonify(resultado), status_code

@app.route('/procesar_aduccion_hombro_angulo_derecha', methods=['POST'])
def procesar_aduccion_hombro_derecha():
    dato = request.get_json()
    video = dato.get('video')
    resultado, status_code = procesar_video_endpoint(procesar_video_aduccion_hombro_angulo_derecha, video)
    return jsonify(resultado), status_code

@app.route('/procesar_aduccion_hombro_angulo_izquierda', methods=['POST'])
def procesar_aduccion_hombro_izquierda():
    dato = request.get_json()
    video = dato.get('video')
    resultado, status_code = procesar_video_endpoint(procesar_video_aduccion_hombro_angulo_izquierda, video)
    return jsonify(resultado), status_code

@app.route('/procesar_aduccion_hombro_distancia_derecha', methods=['POST'])
def procesar_aduccion_hombro_distancia_derecha():
    dato = request.get_json()
    video = dato.get('video')
    resultado, status_code = procesar_video_endpoint(procesar_video_aduccion_hombro_distancia_derecha, video)
    return jsonify(resultado), status_code

@app.route('/procesar_aduccion_hombro_distancia_izquierda', methods=['POST'])
def procesar_aduccion_hombro_distancia_izquierda():
    dato = request.get_json()
    video = dato.get('video')
    resultado, status_code = procesar_video_endpoint(procesar_video_aduccion_hombro_distancia_izquierda, video)
    return jsonify(resultado), status_code

@app.route('/procesar_extension_hombro_distancia_derecha', methods=['POST'])
def procesar_extension_hombro_derecha():
    dato = request.get_json()
    video = dato.get('video')
    resultado, status_code = procesar_video_endpoint(procesar_video_extension_hombro_distancia_derecha, video)
    return jsonify(resultado), status_code

@app.route('/procesar_extension_hombro_distancia_izquierda', methods=['POST'])
def procesar_extension_hombro_izquierda():
    dato = request.get_json()
    video = dato.get('video')
    resultado, status_code = procesar_video_endpoint(procesar_video_extension_hombro_distancia_izquierda, video)
    return jsonify(resultado), status_code

@app.route('/procesar_flexion_hombro_distancia_derecha', methods=['POST'])
def procesar_flexion_hombro_derecha():
    dato = request.get_json()
    video = dato.get('video')
    resultado, status_code = procesar_video_endpoint(procesar_video_flexion_hombro_distancia_derecha, video)
    return jsonify(resultado), status_code

@app.route('/procesar_flexion_hombro_distancia_izquierda', methods=['POST'])
def procesar_flexion_hombro_izquierda():
    dato = request.get_json()
    video = dato.get('video')
    resultado, status_code = procesar_video_endpoint(procesar_video_flexion_hombro_distancia_izquierda, video)
    return jsonify(resultado), status_code

if __name__ == '__main__':
    app.run()