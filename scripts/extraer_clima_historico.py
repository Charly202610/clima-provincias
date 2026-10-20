import requests
import pandas as pd
import time

df_provincias = pd.read_csv("datos_crudos/provincias_coordenadas.csv")

fecha_inicio = "2016-10-19"
fecha_fin = "2026-10-18"

todos_los_datos = []

for _, fila in df_provincias.iterrows():
    print(f"Pidiendo datos de {fila['provincia']}...")
    url = "https://archive-api.open-meteo.com/v1/archive"
    parametros = {
        "latitude": fila["lat"],
        "longitude": fila["lon"],
        "start_date": fecha_inicio,
        "end_date": fecha_fin,
        "daily": "temperature_2m_max,temperature_2m_min,wind_speed_10m_max,wind_direction_10m_dominant",
        "timezone": "America/Argentina/Buenos_Aires"
    }
    respuesta = requests.get(url, params=parametros)

    if respuesta.status_code == 200:
        datos = respuesta.json()["daily"]
        df_provincia = pd.DataFrame(datos)
        df_provincia["provincia"] = fila["provincia"]
        todos_los_datos.append(df_provincia)
    else:
        print(f"Error con {fila['provincia']}: {respuesta.status_code}")

    time.sleep(6)

df_final = pd.concat(todos_los_datos, ignore_index=True)
df_final.to_csv("datos_crudos/clima_historico_provincias.csv", index=False)
print("Listo, guardado el archivo completo.")