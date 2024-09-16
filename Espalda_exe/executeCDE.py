import requests

url = 'http://192.168.100.125:1000/procesarCDE'
file_path = "C:/Users/Dark6/Downloads/pendiente por entregar/curva2.jpeg"

with open(file_path, 'rb') as file:
    files = {'file': file}
    response = requests.post(url, files=files)
if response.status_code == 200:
    response_json = response.json()
    Angulo = response_json.get('Angulo')
    if Angulo is not None:
        print(f"{{'Angulo': {Angulo}}}")

url = 'http://192.168.100.125:9000/predecirCDE'
data = {'Angulo': Angulo}
response = requests.post(url, json=data)
resultado = response.json().get('resultado')
print(resultado)

