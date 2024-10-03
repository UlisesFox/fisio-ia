import time
import subprocess

servers = [
    {"name": "de funciones", "path": "./servidor_consultas_calculadores.py", "port": 5000},
    {"name": "de ia de flexion de rodilla", "path": "./Rodilla_IAs/ia_flexion_rodilla_angulo.py", "port": 5001},
    {"name": "de ia de extension de rodilla", "path": "./Rodilla_IAs/ia_extension_rodilla_angulo.py", "port": 5002},
    {"name": "de ia de curvatura de piernas", "path": "./Piernas_IAs/ia_curvatura_piernas_angulo.py", "port": 5003},
    {"name": "de ia de flexion de hombro", "path": "./Hombro_IAs/ia_flexion_hombro_distancia.py", "port": 5004},
    {"name": "de ia de extension de hombro", "path": "./Hombro_IAs/ia_extension_hombro_distancia.py", "port": 5005},
    {"name": "de ia de aduccion de hombro por distancia", "path": "./Hombro_IAs/ia_aduccion_hombro_distancia.py", "port": 5006},
    {"name": "de ia de aduccion de hombro por angulo", "path": "./Hombro_IAs/ia_aduccion_hombro_angulo.py", "port": 5007},
    {"name": "de ia de curvatura de espalda", "path": "./Espalda_IAs/ia_curvatura_espalda_angulo.py", "port": 5008},
    {"name": "de ia de flexion de codo", "path": "./Codo_IAs/ia_flexion_codo_angulo.py", "port": 5009},
    {"name": "de ia de extension de codo", "path": "./Codo_IAs/ia_extension_codo_angulo.py", "port": 5010},
    {"name": "de ia de flexion de cadera", "path": "./Cadera_IAs/ia_flexion_cadera_angulo.py", "port": 5011},
    {"name": "de ia de extension de cadera", "path": "./Cadera_IAs/ia_extension_cadera_distancia.py", "port": 5012},
    {"name": "de ia de aduccion de cadera por distancia", "path": "./Cadera_IAs/ia_extension_cadera_distancia.py", "port": 5013},
    {"name": "de ia de aduccion de cadera por angulo", "path": "./Cadera_IAs/ia_aduccion_cadera_angulo.py", "port": 5014}
]

processes = []

for server in servers:
    process = subprocess.Popen(
        ["python", server["path"]], 
        stdout=subprocess.PIPE,  
        stderr=subprocess.STDOUT,  
        text=True
    )
    processes.append({"process": process, "name": server["name"], "port": server["port"], "ready": False})

def check_server_ready(output, server):
    if "Running on" in output:
        server["ready"] = True
        return True
    return False

def terminate_processes():
    print("Terminando servidores...")
    for server_info in processes:
        process = server_info["process"]
        if process.poll() is None:
            process.terminate()
    print("Todos los servidores han sido cerrados.")

def terminate_processes_not_mensaje():
    for server_info in processes:
        process = server_info["process"]
        if process.poll() is None:
            process.terminate()

try:
    print("Los servidores estaran completamente cargados cuando no aparescan mas lineas de texto (10s)")
    print("Presione Ctrl + C para terminar el programa")
    print("")
    all_ready = False
    while not all_ready:
        all_ready = True
        for server_info in processes:
            process = server_info["process"]
            
            if process.poll() is None:
                output = process.stdout.readline()

                if output:
                    if check_server_ready(output, server_info):
                        print(f"El servidor {server_info['name']} se está cargando, espere...")
                    else:
                        all_ready = False
                        print(f"El servidor {server_info['name']} se está cargando, espere...")
            else:
                all_ready = False
                print(f"Error: El servidor {server_info['name']} se ha detenido inesperadamente.")
        
        if not all_ready:
            print("")
            time.sleep(10)

except KeyboardInterrupt:
    terminate_processes()

finally:
    terminate_processes_not_mensaje()