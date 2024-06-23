import requests

url = 'http://127.0.0.1:5000/server/autodoc_movimiento'
file_path = "C:/Users/Dark6/Downloads/pendiente por entregar/pie.jpeg"
with open(file_path, 'rb') as file:
    files = {'file': file}
    response = requests.post(url, files=files)
if response.status_code == 200:
    response_json = response.json()
    angle = response_json.get('angle')
    if angle is not None:
        print(f"{angle}")

url = 'http://127.0.0.1:7000/predecir'
data = {'angulos': angle}
response = requests.post(url, json=data)
resultado = response.json().get('resultados')
print(resultado)
