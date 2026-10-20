import pandas as pd

df = pd.read_csv("datos_crudos/clima_historico_provincias.csv")

# Convertimos la columna de fecha a tipo fecha real
df["time"] = pd.to_datetime(df["time"])
df["anio"] = df["time"].dt.year
df["mes"] = df["time"].dt.month

# Promedios mensuales por provincia
promedios_mensuales = df.groupby(["provincia", "anio", "mes"]).agg(
    temp_max_promedio=("temperature_2m_max", "mean"),
    temp_min_promedio=("temperature_2m_min", "mean"),
    viento_promedio=("wind_speed_10m_max", "mean")
).reset_index()

promedios_mensuales.to_csv("datos_procesados/clima_mensual_provincias.csv", index=False)

# Promedios anuales por provincia
promedios_anuales = df.groupby(["provincia", "anio"]).agg(
    temp_max_promedio=("temperature_2m_max", "mean"),
    temp_min_promedio=("temperature_2m_min", "mean"),
    viento_promedio=("wind_speed_10m_max", "mean")
).reset_index()

promedios_anuales.to_csv("datos_procesados/clima_anual_provincias.csv", index=False)

print("Listo, archivos mensual y anual guardados.")