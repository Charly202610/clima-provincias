import requests
import pandas as pd
import time

# ---- CAMBIO AGREGADO: función que pide los datos y reintenta si la respuesta no es válida ----
def pedir_con_reintentos(url, parametros, intentos=5, espera_base=30):
    """Pide datos a Open-Meteo y reintenta con espera creciente si no llega un JSON válido.
    Devuelve el diccionario 'daily' o None si fallan todos los intentos."""
    for intento in range(1, intentos + 1):
        respuesta = requests.get(url, params=parametros, timeout=60)
        if respuesta.status_code == 200:
            try:
                return respuesta.json()["daily"]
            except (ValueError, KeyError):
                pass  # código 200 pero cuerpo vacío o sin JSON válido
        espera = espera_base * intento
        print(f"  Respuesta inválida (código {respuesta.status_code}). "
              f"Reintento {intento}/{intentos} en {espera} s...")
        time.sleep(espera)
    return None
# ---- FIN DEL CAMBIO ----

df_provincias = pd.read_csv("datos_crudos/provincias_coordenadas.csv")

fecha_inicio = "2016-10-19"
fecha_fin = "2026-10-18"

todos_los_datos = []
provincias_fallidas = []  # CAMBIO AGREGADO: para avisar al final cuáles no se pudieron traer

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

    # ---- CAMBIO AGREGADO: se reemplaza el requests.get y el chequeo de código por la función ----
    datos = pedir_con_reintentos(url, parametros)

    if datos is not None:
        df_provincia = pd.DataFrame(datos)
        df_provincia["provincia"] = fila["provincia"]
        todos_los_datos.append(df_provincia)
    else:
        print(f"Error con {fila['provincia']}: no se pudieron obtener datos")
        provincias_fallidas.append(fila["provincia"])
    # ---- FIN DEL CAMBIO ----

    time.sleep(6)

df_final = pd.concat(todos_los_datos, ignore_index=True)
df_final.to_csv("datos_crudos/clima_historico_provincias.csv", index=False)

# ---- CAMBIO AGREGADO: aviso final si quedó alguna provincia afuera ----
if provincias_fallidas:
    print(f"ATENCIÓN: faltan datos de {len(provincias_fallidas)} provincias: {provincias_fallidas}")
else:
    print("Listo, guardado el archivo completo con las 24 provincias.")
# ---- FIN DEL CAMBIO ----