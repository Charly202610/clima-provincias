import requests
import pandas as pd
import time

# Traer las 24 provincias con sus coordenadas desde la API georef
url_provincias = "https://apis.datos.gob.ar/georef/api/provincias"
respuesta = requests.get(url_provincias, params={"campos": "nombre,centroide", "max": 24})
datos = respuesta.json()["provincias"]

provincias = []
for p in datos:
    provincias.append({
        "provincia": p["nombre"],
        "lat": p["centroide"]["lat"],
        "lon": p["centroide"]["lon"]
    })

df_provincias = pd.DataFrame(provincias)
df_provincias.to_csv("datos_crudos/provincias_coordenadas.csv", index=False)
print(df_provincias)