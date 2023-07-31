import pandas as pd
import chardet


def detectar_encoding_arquivo(nome_arquivo):
    with open(nome_arquivo, "rb") as f:
        resultado = chardet.detect(f.read())
    return resultado["encoding"]


def converter_arquivo_para_utf8(nome_arquivo, encoding_origem):
    try:
        df = pd.read_csv(nome_arquivo, encoding=encoding_origem, delimiter='"')
        # df.to_csv("temp.csv", encoding="utf-8", index=False, delimiter=False)
        return True
    except Exception as e:
        print(f"Erro ao converter o arquivo: {e}")
        return False


# Exemplo para um arquivo CSV
nome_arquivo_csv = "RJ_Municipios_2022/roubos.csv"
# nome_arquivo_csv = "temp.csv"
encoding_origem_csv = detectar_encoding_arquivo(nome_arquivo_csv)
print(f"Encoding original do arquivo CSV: {encoding_origem_csv}")
if converter_arquivo_para_utf8(nome_arquivo_csv, encoding_origem_csv):
    print("Arquivo CSV convertido para UTF-8 com sucesso!")

# # Exemplo para um arquivo XLSX
# nome_arquivo_xlsx = "arquivo.xlsx"
# encoding_origem_xlsx = detectar_encoding_arquivo(nome_arquivo_xlsx)
# print(f"Encoding original do arquivo XLSX: {encoding_origem_xlsx}")
# if converter_arquivo_para_utf8(nome_arquivo_xlsx, encoding_origem_xlsx):
#     print("Arquivo XLSX convertido para UTF-8 com sucesso!")
