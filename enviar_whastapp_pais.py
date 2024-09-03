import time
import pandas as pd
import pywhatkit as kit
import json
import requests
import time
import os
from datetime import datetime


print(f"#####################################################################################")
print(f"## Enviar WhatsApp para os Pais dos Catequizandos que Faltaram no Enconro de hoje! ##")
print(f"#####################################################################################")


url = input("Digite a URL da API: ")
api_key = input("Digite a API Key: ")

# Dados do cabeçalho (headers)
headers = {
    "Content-Type": "application/json",
    "apikey": api_key
}

# Carregar as planilhas
frequencia_df = pd.read_excel('Frequencia.xlsx')
pais_df = pd.read_excel('Catequizandos.xlsx')

# Captura a data atual
data_atual = datetime.now().strftime("%d/%m/%y")

# Identificar alunos que faltaram
alunos_faltaram = frequencia_df[frequencia_df[data_atual] == 0]

# Configuração do logging
logging.basicConfig(filename='error.log', level=logging.ERROR, format='%(asctime)s - %(levelname)s - %(message)s')

# Enviar mensagem para os pais
for index, aluno in alunos_faltaram.iterrows():
    nome_aluno = aluno['Nome'].split()[0]
    contato_mae = pais_df.loc[pais_df['Nome'] == nome_aluno, 'Contato1'].values[0]
    
   

    if pd.notna(contato_mae):
        nome = pais_df.loc[pais_df['Nome'] == nome_aluno, 'Mãe'].values[0]
        telefone = contato_mae
    else:
        nome = pais_df.loc[pais_df['Nome'] == nome_aluno, 'Pai'].values[0]
        telefone = pais_df.loc[pais_df['Nome'] == nome_aluno, 'Contato2'].values[0]
       
    mensagem = (f"Olá {nome.split()[0]}, paz e Bem!\n\n"
                 f"Sentimos a falta do(a) {nome_aluno} no encontro de hoje. Aconteceu alguma coisa?\n\n"
                 f"Esperaremos ver o(a) {nome_aluno} no próximo encontro e estamos à disposição para qualquer necessidade.\n\n"
                 f"Agradecemos pela colaboração.\n"
                 f"Atenciosamente, \n"
                 f"Catequista Pedro.")

    # Enviar mensagem pelo WhatsApp
    #kit.sendwhatmsg_instantly(f"+{telefone}", mensagem)

    #print(f"Mensagens enviadas com sucesso!")

    # Dados do corpo da requisição (body)
    postData = {
        "number": telefone,
        "textMessage": {
        "text": mensagem
            }
    }

    # Converte os dados em JSON
    postDataJson = json.dumps(postData)

    # Define as opções da requisição
    headers["Content-Length"] = str(len(postDataJson))

    try:
        # Executa a requisição e obtém a resposta
        response = requests.post(url, data=postDataJson, headers=headers)
        response.raise_for_status()

        # Add delay para enviar próxima mensagem
        time.sleep(10)

    except requests.exceptions.HTTPError as errh:
        logging.error(f"Erro ao enviar mensagem para o(a) Mãe/Pai do(a) {nome_aluno}: {errh}")
    except (ValueError, TypeError) as err:
        logging.error(f"Erro de dados para o(a) Mãe/Pai do(a) {nome_aluno}: {err}")
    except Exception as e:
        logging.error(f"Erro inesperado para o(a) Mãe/Pai do(a){nome_aluno}: {e}")
