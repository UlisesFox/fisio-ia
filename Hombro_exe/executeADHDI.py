import requests

url = 'http://192.168.100.125:1000/procesarADHDI'
url2 = 'http://192.168.100.125:4100/predecirADHD'
video_front_path = 'C:/Users/Dark6/Downloads/pendiente por entregar/Aducción de hombro distancia.mp4'

data = {
    "video_front_path": video_front_path
}

response = requests.post(url, json=data)
if response.status_code == 200:
    # Extraer los datos como diccionario
    print(response.json())
    datos = response.json()
    
    # Extraer los valores específicos y convertirlos a enteros
    Distancia = int(datos['Distancia'])

    # Ahora enviamos los tres valores al servidor para la predicción
    data_predecir = {
        'Distancia': Distancia
    }
    response_predecir = requests.post(url2, json=data_predecir)
    
    if response_predecir.status_code == 200:
        print(response_predecir.json())
    else:
        print(f"Error en la predicción: {response_predecir.status_code}")
        print(response_predecir.json())
else:
    print(f"Error al procesar: {response.status_code}")
    print(response.json())