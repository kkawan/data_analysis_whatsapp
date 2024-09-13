import os

# Função para encontrar os N arquivos de áudio .opus mais longos em uma pasta com base no tamanho do arquivo
def encontrar_audios_maiores(pasta, quantidade=10):
    audios = []

    # Verificar se a pasta existe
    if not os.path.exists(pasta):
        print(f"A pasta '{pasta}' não existe.")
        return

    # Percorrer todos os arquivos na pasta
    for arquivo in os.listdir(pasta):
        caminho_arquivo = os.path.join(pasta, arquivo)

        # Verificar se o arquivo é de áudio no formato .opus
        if arquivo.lower().endswith('.opus'):
            try:
                # Obter o tamanho do arquivo
                tamanho = os.path.getsize(caminho_arquivo)  # Tamanho em bytes

                # Adicionar o arquivo e seu tamanho à lista
                audios.append((arquivo, tamanho))

            except Exception as e:
                print(f"Erro ao processar {arquivo}: {e}")
        else:
            # Ignorar arquivos que não são .opus
            print(f"Ignorado: {arquivo} (não é um arquivo .opus)")

    # Ordenar a lista de áudios pelo tamanho (do maior para o menor)
    audios_ordenados = sorted(audios, key=lambda x: x[1], reverse=True)

    # Exibir os arquivos maiores, conforme a quantidade solicitada
    for i, (arquivo, tamanho) in enumerate(audios_ordenados[:quantidade], start=1):
        tamanho_kb = tamanho / 1024  # Converter para KB
        print(f"{i}. O arquivo de áudio '{arquivo}' tem tamanho de {tamanho_kb:.2f} KB.")
    
    if len(audios_ordenados) == 0:
        print("Nenhum arquivo .opus encontrado.")

# Exemplo de uso
pasta_audio = ''  # Substitua pelo caminho da sua pasta de áudios
encontrar_audios_maiores(pasta_audio, quantidade=10)
