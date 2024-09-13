# Data Analysis WhatsApp

Este projeto realiza uma análise automatizada de conversas exportadas do WhatsApp, com foco em estatísticas sobre o comportamento dos usuários e uso de emojis, além de identificar figurinhas duplicadas e áudios maiores. O código inclui funções para processar as mensagens, gerar gráficos e fazer análises de sentimento. 

Estou aberto a quaisquer sugestões e implementações de novas funcionalidades ou melhorias no código. Sinta-se à vontade para:

- Abrir issues: Se encontrar bugs ou tiver sugestões de melhorias.
- Enviar pull requests: Para novas funcionalidades ou correções de bugs.

## Funcionalidades

- **Análise de conversas do WhatsApp**:
  - Processamento de mensagens exportadas de chats em formato `.txt`.
  - Contagem das palavras mais usadas nas conversas.
  - Identificação de emojis mais frequentes.
  - Análise de horários das mensagens.
  - Análise de mensagens por mês e dia da semana.
  - Geração de gráficos e nuvens de palavras.
  - Análise de sentimento das mensagens (positivo, negativo ou neutro).

- **Identificação de arquivos de áudio e figurinhas**:
  - Listagem dos arquivos de áudio `.opus` mais longos em uma pasta. (pode-se alterar para a verificação de áudios mp3 também se desejar)
  - Identificação da figurinha `.webp` mais recorrente com base no hash dos arquivos.

## Requisitos

Os pacotes necessários para rodar o projeto estão listados no arquivo `requirements.txt`. Para instalá-los, use o comando abaixo:

```bash
pip install -r requirements.txt
```
obs: Necessária a alteração do regex dependendo do aparelho que exportar as mensagens.
