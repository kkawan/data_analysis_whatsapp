import os
import hashlib
from collections import Counter

# Função para calcular o hash de um arquivo (usado para identificar figurinhas duplicadas)
def calcular_hash_arquivo(caminho_arquivo):
    hash_md5 = hashlib.md5()
    with open(caminho_arquivo, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()

# Função para encontrar a figurinha mais recorrente em uma pasta
def encontrar_figurinha_recorrente(pasta):
    figurinhas = []

    # Verificar se a pasta existe
    if not os.path.exists(pasta):
        print(f"A pasta '{pasta}' não existe.")
        return

    # Dicionário para mapear hash -> caminho do arquivo
    hash_para_arquivo = {}

    # Percorrer todos os arquivos na pasta
    for arquivo in os.listdir(pasta):
        caminho_arquivo = os.path.join(pasta, arquivo)

        # Verificar se o arquivo é uma figurinha no formato .webp
        if arquivo.lower().endswith('.webp'):
            try:
                # Calcular o hash do arquivo para identificar figurinhas iguais
                hash_arquivo = calcular_hash_arquivo(caminho_arquivo)

                # Adicionar o hash e o caminho à lista de figurinhas
                figurinhas.append(hash_arquivo)
                hash_para_arquivo[hash_arquivo] = caminho_arquivo  # Mapear o hash ao caminho do arquivo

            except Exception as e:
                print(f"Erro ao processar {arquivo}: {e}")
        else:
            # Ignorar arquivos que não são figurinhas
            print(f"Ignorado: {arquivo} (não é um arquivo .webp)")

    # Contar a recorrência de cada hash de figurinha
    contador_figurinhas = Counter(figurinhas)

    # Encontrar a figurinha mais recorrente
    if contador_figurinhas:
        hash_mais_recorrente, ocorrencias = contador_figurinhas.most_common(1)[0]
        caminho_da_figurinha = hash_para_arquivo[hash_mais_recorrente]
        print(f"A figurinha mais recorrente tem o hash '{hash_mais_recorrente}' e aparece {ocorrencias} vezes.")
        print(f"O arquivo correspondente à figurinha é: '{caminho_da_figurinha}'")
    else:
        print("Nenhuma figurinha encontrada.")

# Exemplo de uso
pasta_midia = ''  # Substitua pelo caminho da sua pasta de mídias exportadas
encontrar_figurinha_recorrente(pasta_midia)
