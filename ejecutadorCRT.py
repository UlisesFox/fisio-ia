import requests

# URL del servidor
url = "http://192.168.100.125:2000/procesarCRT"
url2 = 'http://192.168.100.125:6000/predecir'
video_front_path = 'C:/Users/Dark6/Downloads/pendiente por entregar/PieF.mp4'

data = {
    "video_front_path": video_front_path
}

response = requests.post(url, json=data)
if response.status_code == 200:
    # Extraer los datos como diccionario
    print(response.json())
    datos = response.json()
    
    # Extraer los valores específicos y convertirlos a enteros
    max_frontal_left = int(datos['Max Frontal Left'])
    max_frontal_right = int(datos['Max Frontal Right'])
    min_frontal_left = int(datos['Max Frontal Left'])
    min_frontal_right = int(datos['Max Frontal Right'])
    

    # Ahora enviamos los tres valores al servidor para la predicción
    data_predecir = {
        'max_frontal_left': max_frontal_left,
        'max_frontal_right': max_frontal_right,
        'min_frontal_left': min_frontal_left,
        'min_frontal_right': min_frontal_right
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