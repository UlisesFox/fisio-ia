import requests

url = 'http://192.168.100.125:2000/procesarCDP'
file_path = "C:/Users/Dark6/Downloads/pendiente por entregar/pie.jpeg"

with open(file_path, 'rb') as file:
    files = {'file': file}
    response = requests.post(url, files=files)
if response.status_code == 200:
    response_json = response.json()
    Angulos = response_json.get('Angulos')
    if Angulos is not None:
        print(f"{{'Angulos': {Angulos}}}")

url2 = 'http://192.168.100.125:4000/predecirCDP'
data = {'Angulos': Angulos}
response = requests.post(url2, json=data)
resultado = response.json().get('resultado')
print(resultado)