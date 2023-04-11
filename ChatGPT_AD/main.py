import pandas as pd
import numpy as np
import openai
import os
from dotenv import load_dotenv #pip install python-dotenv


# carrega variaveis de ambiente
load_dotenv()

# abaixo substitua (os.getenv("MY_API_KEY")) pela sua key da openai
openai.api_key= os.getenv("MY_API_KEY")

# nome do dataframe com extensao
arquivo = "vendas.xlsx"

# Lendo o arquivo CSV
# df = pd.read_csv(arquivo)

# lendo arquivo Excel
df = pd.read_excel(arquivo)

# coloca todas as colunas em uma string separado por ","
colunas = ', '.join(df.columns)
print("Colunas: ", colunas)

# exibir código fonte do Chat GPT?
exibir_cod = True

# msg ao chat
prompt = f"crie um codigo python que leia o arquivo {arquivo} que possui as colunas ({colunas}) e me retone "

# função de resposta do Chat GPT
def gerar_resposta(mensagem):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=mensagem,
        max_tokens=2024,
        temperature=0.5
    )
    return [response.choices[0].message.content, response.usage]

while True:
    # esse modelo usa um array para perguntas e respostas
    mensagem = []

    # input para a pergunta
    pergunta = prompt + input("Solicite a análise (ou sair): ") + "(mostre o código)"

    # se digitar a palavra desligar para a execução
    if "desligar" not in pergunta:
        # adiciona a pergunta ao array
        mensagem.append({"role": "user", "content": str(pergunta)})

        #chama função para gerar a resposta GPT
        resposta = gerar_resposta(mensagem)
        retorno = resposta[0]
        #print("Resposta GPT: ", retorno)
        try:
            codigo = retorno.replace("python", "")
            codigo = codigo.split("```")[1]

            if exibir_cod:
                print("------------------CÓDIGO DO CHAT GPT-------------------")
                print(codigo)
                print("----------------FIM DO CÓDIGO DO CHAT GPT--------------")
            exec(codigo)

        except:
            print("Erro na execução, refaça a consulta e tente novamente!")
            continue
    else:
        print("Tchau!")
        break
    print("-------------------------------------------------------")
