'''
Sugestão de receita com ingredientes disponíveis usando IA
Autor: Daniel Amorim
'''

import openai # instale pip install
from dotenv import load_dotenv # pip install python-dotenv
import os
import tkinter as tk
from tkinter import scrolledtext
import threading #chama openai em segundo plano para nao travar a janela do tkinter
load_dotenv()

# Substitua (os.getenv("MY_API_KEY")) pela chave da sua API
openai.api_key= os.getenv("MY_API_KEY")

## --INICIO DAS FUNÇÕES

# Função de resposta do Chat GPT
def gerar_resposta(mensagem):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=mensagem,
        max_tokens=2048,
        temperature=0.7
    )
    return [response.choices[0].message.content, response.usage]

# Função para criar uma nova receita
def criar_receita():
    # bloqueia botao enquanto executa
    botao_criar.configure(state="disabled")
    # Limpa painel
    caixa_texto.delete(1.0, tk.END)
    # Obtém o texto do campo de entrada
    ingredientes = campo_entrada.get()
    # Pega radio selecionado
    tipo_receita = opcao.get()
    # Limpa o campo de entrada
    campo_entrada.delete(0, tk.END)
    # Mensagem de solicitação
    solicitacao = f"Crie uma receita {tipo_receita} com somente {ingredientes} e no" \
               f" máximo com alguns temperos comuns"
    mensagem = [{"role": "user", "content": str(solicitacao)}]
    print(solicitacao)
    # Chama função para gerar a resposta GPT
    receita = gerar_resposta(mensagem)
    # Exibe o nome da receita na caixa de texto
    caixa_texto.insert(tk.END, f"Menu: {receita[0]}\n")
    # Desbloqueia botao
    botao_criar.configure(state="normal")

## --FIM DAS FUNÇÕES

## --JANELA DO TKINTER

# Cria a janela principal
janela = tk.Tk()
janela.title("Chat GPT Culinário - Daniel Amorim")
janela.geometry("700x700")

# Texto do input
texto = tk.Label(janela, text="Digite os ingredientes separados por virgula:")
texto.pack()

# Cria o campo de input
campo_entrada = tk.Entry(janela, width=100)
campo_entrada.pack()

# Chama função "Criar Receita"
botao_criar = tk.Button(janela, width=40, text="Criar Receita", command=lambda: threading.Thread(target=criar_receita).start())
botao_criar.pack(pady=10)

# Cria a variável para armazenar o valor selecionado
opcao = tk.StringVar(value="básica")

# Cria três botões de seleção
botao1 = tk.Radiobutton(janela, text="Básica", variable=opcao, value="básica")
botao2 = tk.Radiobutton(janela, text="Saudável", variable=opcao, value="saudável")
botao3 = tk.Radiobutton(janela, text="Vegana", variable=opcao, value="vegana")
botao4 = tk.Radiobutton(janela, text="Doce", variable=opcao, value="doce")

# Organiza os botões de seleção na janela
botao1.pack()
botao2.pack()
botao3.pack()
botao4.pack()

# Label de obs
texto_obs = tk.Label(janela, text="OBS: A IA pode adicionar à receita ingredientes e temperos que são comuns ter nas cozinhas!")
texto_obs.pack()

# Cria a caixa de texto com rolagem
caixa_texto = scrolledtext.ScrolledText(janela, width=80, height=28)
caixa_texto.pack()

# Cria o botão "Sair"
botao_sair = tk.Button(janela, width=40, text="Sair", command=janela.destroy)
botao_sair.pack(pady=10)

# Inicia o loop principal da janela
janela.mainloop()

## --FIM DA JANELA DO TKINTER