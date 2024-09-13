
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
    padrao_mensagem = re.compile(r'\[(\d{2}/\d{2}/\d{4}), (\d{2}:\d{2}:\d{2})\] (.*?): (.*)')
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
            
            if any(frase in mensagem.lower() for frase in ignorar_mensagens):
                continue

            mensagens.append([data, hora, usuario, mensagem])

    return pd.DataFrame(mensagens, columns=['Data', 'Hora', 'Usuário', 'Mensagem'])

# Função para criar gráficos
def criar_grafico_barras(titulo, dados, xlabel, ylabel, cor='blue'):
    plt.figure(figsize=(10, 6))
    dados.plot(kind='bar', color=cor)
    plt.title(titulo)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.show()

# Função para criar gráfico de linhas
def criar_grafico_linhas(titulo, dados, xlabel, ylabel, cor='green'):
    plt.figure(figsize=(10, 6))
    dados.plot(kind='line', color=cor, marker='o')
    plt.title(titulo)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.grid(True)
    plt.tight_layout()
    plt.show()

# Função para contar as palavras mais usadas
def palavras_mais_usadas(df, top_n=10):
    todas_palavras = ' '.join(df['Mensagem']).lower()
    todas_palavras = re.findall(r'\b\w+\b', todas_palavras)
    contagem = Counter(todas_palavras)
    return contagem.most_common(top_n)

# Função para contar mensagens por usuário
def mensagens_por_usuario(df):
    return df['Usuário'].value_counts()

# Função para contar emojis
def contar_emojis(df):
    todos_emojis = ''.join([char for mensagem in df['Mensagem'] for char in mensagem if emoji.is_emoji(char)])
    contagem = Counter(todos_emojis)
    return contagem.most_common(10)

# Função para contar as mensagens por horário
def analisar_horarios(df):
    df['Hora'] = pd.to_datetime(df['Hora'], format='%H:%M:%S')
    df['Faixa_Horaria'] = pd.cut(df['Hora'].dt.hour, bins=[0, 6, 12, 18, 24], labels=['Madrugada', 'Manhã', 'Tarde', 'Noite'], include_lowest=True)
    return df['Faixa_Horaria'].value_counts()

# Função para contar mensagens por mês
def analisar_mensagens_por_mes(df):
    df['Data'] = pd.to_datetime(df['Data'], format='%d/%m/%Y')
    df['Mes'] = df['Data'].dt.month_name()
    return df['Mes'].value_counts()

# Carregando e processando as mensagens
arquivo = ''  # Coloque o caminho para o arquivo exportado
dados = carregar_mensagens(arquivo)
df_mensagens = processar_mensagens(dados)

# Visualização 1: Gráfico de barras - Mensagens por usuário
mensagens_usuario = mensagens_por_usuario(df_mensagens)
criar_grafico_barras('Mensagens por Usuário', mensagens_usuario[:10], 'Usuário', 'Número de Mensagens', cor='orange')

# Visualização 2: Gráfico de barras - Emojis mais usados
emojis_mais_usados = contar_emojis(df_mensagens)
emojis_df = pd.DataFrame(emojis_mais_usados, columns=['Emoji', 'Frequência']).set_index('Emoji')
criar_grafico_barras('Emojis Mais Usados', emojis_df['Frequência'], 'Emoji', 'Frequência', cor='purple')

# Visualização 3: Gráfico de barras - Mensagens por faixa horária
mensagens_horario = analisar_horarios(df_mensagens)
criar_grafico_barras('Mensagens por Faixa Horária', mensagens_horario, 'Faixa Horária', 'Número de Mensagens', cor='blue')

# Visualização 4: Gráfico de linhas - Mensagens por mês
mensagens_mes = analisar_mensagens_por_mes(df_mensagens)
criar_grafico_linhas('Mensagens por Mês', mensagens_mes, 'Mês', 'Número de Mensagens', cor='green')
