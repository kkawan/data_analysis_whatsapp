# Importando bibliotecas
import re
import pandas as pd
from collections import Counter
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import emoji
from datetime import datetime
from textblob import TextBlob

# Função para carregar o arquivo de texto
def carregar_mensagens(arquivo):
    with open(arquivo, 'r', encoding='utf-8') as f:
        dados = f.readlines()
    return dados

# Função para processar e limpar os dados (removendo datas, horas, etc.)
def processar_mensagens(dados):
    mensagens = []
    # Regex para capturar data, hora, usuário e mensagem
    padrao_mensagem = re.compile(r'\[(\d{2}/\d{2}/\d{4}), (\d{2}:\d{2}:\d{2})\] (.*?): (.*)')

    # Lista de palavras-chave que indicam mensagens do sistema ou metadados
    ignorar_mensagens = [
        "protegidas com a criptografia de ponta a ponta",
        "criou o grupo",
        "mudou a descrição do grupo",
        "adicionou",
        "anexado"
    ]

    for linha in dados:
        resultado = padrao_mensagem.match(linha)
        if resultado:
            data = resultado.group(1)
            hora = resultado.group(2)
            usuario = resultado.group(3)
            mensagem = resultado.group(4)
            
            # Ignorar mensagens que contenham palavras-chave de metadados
            if any(frase in mensagem.lower() for frase in ignorar_mensagens):
                continue

            # Adicionar as mensagens processadas
            mensagens.append([data, hora, usuario, mensagem])

    return pd.DataFrame(mensagens, columns=['Data', 'Hora', 'Usuário', 'Mensagem'])

# Função para contar as palavras mais usadas
def palavras_mais_usadas(df, top_n=10):
    todas_palavras = ' '.join(df['Mensagem']).lower()
    todas_palavras = re.findall(r'\b\w{4,}\b', todas_palavras)
    contagem = Counter(todas_palavras)
    return contagem.most_common(top_n)

# Função para criar uma nuvem de palavras
def gerar_nuvem_palavras(df):
    todas_palavras = ' '.join(df['Mensagem']).lower()
    
    if todas_palavras.strip():  # Verifica se há palavras para gerar a nuvem
        wordcloud = WordCloud(width=800, height=400, background_color='white').generate(todas_palavras)
        
        plt.figure(figsize=(10, 5))
        plt.imshow(wordcloud, interpolation='bilinear')
        plt.axis('off')
        plt.show()
    else:
        print("Nenhuma palavra encontrada para gerar a nuvem de palavras.")

# Função para contar mensagens por usuário
def mensagens_por_usuario(df):
    return df['Usuário'].value_counts()

# Função para contar emojis
def contar_emojis(df):
    # Usar emoji.is_emoji para detectar emojis corretamente
    todos_emojis = ''.join([char for mensagem in df['Mensagem'] for char in mensagem if emoji.is_emoji(char)])
    contagem = Counter(todos_emojis)
    return contagem.most_common(10)


# Função para contar as mensagens por horário
def analisar_horarios(df):
    df['Hora'] = pd.to_datetime(df['Hora'], format='%H:%M:%S')
    df['Faixa_Horaria'] = pd.cut(df['Hora'].dt.hour, bins=[0, 6, 12, 18, 24], labels=['Madrugada', 'Manhã', 'Tarde', 'Noite'], include_lowest=True)
    return df['Faixa_Horaria'].value_counts()

# Função para contar mensagens por dia da semana
def analisar_dias_semana(df):
    df['Data'] = pd.to_datetime(df['Data'], format='%d/%m/%Y')
    df['Dia_Semana'] = df['Data'].dt.day_name()
    return df['Dia_Semana'].value_counts()

# Função para contar mensagens por mês
def analisar_mensagens_por_mes(df):
    df['Data'] = pd.to_datetime(df['Data'], format='%d/%m/%Y')
    df['Mes'] = df['Data'].dt.month_name()
    return df['Mes'].value_counts()

# Função para calcular a média de palavras por mensagem por usuário
def media_palavras_por_usuario(df):
    df['Contagem_Palavras'] = df['Mensagem'].apply(lambda x: len(re.findall(r'\b\w+\b', x)))
    return df.groupby('Usuário')['Contagem_Palavras'].mean()

# Função para identificar quem manda a primeira e última mensagem do dia
def primeira_e_ultima_mensagem(df):
    df['Data'] = pd.to_datetime(df['Data'], format='%d/%m/%Y')
    df['Hora'] = pd.to_datetime(df['Hora'], format='%H:%M:%S').dt.time
    primeira_mensagem = df.groupby('Data').first()['Usuário'].value_counts()
    ultima_mensagem = df.groupby('Data').last()['Usuário'].value_counts()
    return primeira_mensagem, ultima_mensagem

# Função para análise de sentimento com TextBlob
def analisar_sentimento(df):
    def calcular_sentimento(mensagem):
        blob = TextBlob(mensagem)
        return blob.sentiment.polarity  # Retorna a polaridade: -1 (negativo), 0 (neutro), 1 (positivo)

    df['Sentimento'] = df['Mensagem'].apply(calcular_sentimento)
    
    # Classificar o sentimento em positivo, negativo ou neutro
    df['Classificacao_Sentimento'] = df['Sentimento'].apply(lambda x: 'Positivo' if x > 0 else ('Negativo' if x < 0 else 'Neutro'))
    
    return df['Classificacao_Sentimento'].value_counts()

# Carregando e processando as mensagens
arquivo = ''  # Coloque o caminho para o arquivo exportado
dados = carregar_mensagens(arquivo)
df_mensagens = processar_mensagens(dados)

# Exibindo as primeiras linhas do DataFrame para garantir que foi processado corretamente
print("Primeiras linhas do DataFrame processado:")
print(df_mensagens.head())

# Exibir análises no console
print("Palavras mais usadas:")
print(palavras_mais_usadas(df_mensagens, top_n=10))

print("Mensagens por usuário:")
print(mensagens_por_usuario(df_mensagens))

print("Emojis mais usados:")
print(contar_emojis(df_mensagens))

print("Mensagens por faixa horária:")
print(analisar_horarios(df_mensagens))

print("Mensagens por dia da semana:")
print(analisar_dias_semana(df_mensagens))

print("Mensagens por mês:")
print(analisar_mensagens_por_mes(df_mensagens))

print("Média de palavras por mensagem por usuário:")
print(media_palavras_por_usuario(df_mensagens))

primeira_mensagem, ultima_mensagem = primeira_e_ultima_mensagem(df_mensagens)
print("Quem manda a primeira mensagem do dia:")
print(primeira_mensagem)
print("Quem manda a última mensagem do dia:")
print(ultima_mensagem)

print("Classificação de sentimentos (Positivo, Neutro, Negativo):")
print(analisar_sentimento(df_mensagens))
