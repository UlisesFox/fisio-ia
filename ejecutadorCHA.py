import requests

url = 'http://192.168.100.125:2000/procesarCHA'
url2 = 'http://192.168.100.125:6000/predecir'
#video_front_path = 'C:/Users/Dark6/Downloads/pendiente por entregar/HombroDF.mp4'

video_front_path = 'C:/Users/Dark6/Downloads/pendiente por entregar/HombroIF.mp4'

data = {
    "video_front_path": video_front_path
}

response = requests.post(url, json=data)
if response.status_code == 200:
    # Extraer los datos como diccionario
    print(response.json())
    datos = response.json()
    
    # Extraer los valores específicos y convertirlos a enteros
    frontal_max = int(datos['Frontal max'])
    frontal_min = int(datos['Frontal min'])

    # Ahora enviamos los tres valores al servidor para la predicción
    data_predecir = {
        'frontal_max': frontal_max,
        'frontal_min': frontal_min
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