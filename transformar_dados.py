import pandas as pd
import requests
from tqdm import tqdm
from time import sleep


def obter_coordenadas_municipio(municipio, cache):
    if municipio in cache:
        return cache[municipio]

    url = "https://nominatim.openstreetmap.org/search"
    parametros = {"q": municipio, "format": "json", "limit": 1}

    try:
        resposta = requests.get(url, params=parametros)
        dados = resposta.json()
        if dados:
            latitude = float(dados[0]["lat"])
            longitude = float(dados[0]["lon"])
            cache[municipio] = (latitude, longitude)
            return latitude, longitude
        else:
            cache[municipio] = None
            return None
    except requests.exceptions.RequestException:
        print("Erro ao fazer a solicitação à API.")
        return None


# Ler o arquivo XLSX
caminho_do_arquivo_xlsx = "RJ_Municipios_2022/roubos.csv"
df = pd.read_csv(caminho_do_arquivo_xlsx, encoding="ISO-8859-1", sep=';')
print(f"{len(df)} registros lidos do CSV.\n")
# Criar colunas para as coordenadas
df["latitude"] = None
df["longitude"] = None

# Usar um dicionário para armazenar as coordenadas já obtidas (cache)
coordenadas_cache = {}

# Iterar sobre os municípios e obter as coordenadas com tqdm
total_registros = len(df)
with tqdm(total=total_registros, desc="Progresso", unit="registro") as pbar:
    for indice, linha in df.iterrows():
        municipio = linha["munic"]
        # print(municipio)
        coordenadas = obter_coordenadas_municipio(municipio, coordenadas_cache)
        if coordenadas:
            latitude, longitude = coordenadas
            df.at[indice, "latitude"] = latitude
            df.at[indice, "longitude"] = longitude

        # Atualizar a barra de progresso a cada iteração
        pbar.update(1)

        # Adicionar um pequeno atraso para simular o tempo de consulta à API
        sleep(0.1)

# Salvar o DataFrame atualizado em um novo arquivo XLSX
df.to_excel("RJ_Municipios_2022/arquivo_atualizado.xlsx", index=False)

print("Coordenadas foram adicionadas ao arquivo com sucesso.")
