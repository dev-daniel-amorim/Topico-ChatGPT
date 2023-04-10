'''
Para instalar as bibliotecas necessárias coloque o arquivo requirements.txt no mesmo
local deste projeto e execute o comando pip install -r requirements.txt no terminal.
'''

import openai
# reconhecimento de fala em texto
import speech_recognition as sr
# texto em fala
import pyttsx3

# Digite seu API do GPT aqui
openai.api_key = "seu_key_API_aqui"

# escolha perguntar por texto
entrada_por_texto = False

# nome da assistente td minusculo (nome que seja facilmente detectado e reconhecivel)
assistente = "paulo"

# seu nome para reconhece-lo
meu_nome = "Daniel"

# printa o custo da operação
pegar_custo = True

# valor pago pelo modelo preditivo usado("gpt-3.5-turbo" = 0,002 a cada 1000tk = 0,000002 por palavra)
valor_por_token = 2e-6

# imprime retorno da mensagem
pegar_retorno = False

# responde por fala
falar = True

# iniciando a mensagem com meu nome (pra armazenar no histórico da conversa)
mensagens = [{"role": "user", "content": f"Meu nome é {meu_nome}"}]

# função de resposta do Chat GPT
def gerar_resposta(messages):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",  # 0.002 dolar por palavra
        messages=messages,
        max_tokens=50,
        temperature=0.5
    )
    return [response.choices[0].message.content, response.usage]

# função para falar o texto pyttsx3
def fale(texto):
    engine.say(texto)
    engine.runAndWait()
    engine.stop()

# ajustes e comandos de voz
r = sr.Recognizer()

# pegando a lista de vozes disponíveis na biblioteca pyttsx3
engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('rate', 200)  #velocidade da voz 180 = normal
for indice, vozes in enumerate(voices):  # lista de vozes
    print(indice, vozes.name)
# escolha a opção de voz (lista será impressa no prompt)
voz = 0
engine.setProperty('voice', voices[voz].id)


#ajusta o ruido do ambiente
ajustar_ambiente_noise = True

while True:
    text = ""
    question = ""

    if entrada_por_texto:
        question = input("Escreva uma pergunta:")
    else:
        # fale uma pergunta
        with sr.Microphone() as mic:
            if ajustar_ambiente_noise:
                r.adjust_for_ambient_noise(mic,duration=1)
            try:
                print(f"Faça uma pergunta (iniciando por {assistente})")
                audio = r.listen(mic)
                print("Aguardando reconhecimento da voz...")

                # voz em texto colocando na variável question
                question = r.recognize_google(audio, language="pt-BR")
                print("Google entendeu:",question)
            except Exception as erro:
                print("Erro detectado:", erro)
                continue

    # Se comando iniciar por desligar ou sair para o programa
    if (question.startswith("desligar")) or (question.startswith("sair")):
        if falar:
            fale("Desligando")
        break
    elif question == "":
        print("Sem perguntas")
        continue

    # Se comando inicia por dona gorete
    elif question.startswith(f"{assistente}") or question.startswith(f"{assistente.capitalize()}") or entrada_por_texto:

        # removendo o nome da assistente da pergunta (iniciando em maisc ou não)
        question = question.replace(f"{assistente.capitalize()} ", "")
        question = question.replace(f"{assistente} ", "")

        print("A pergunta foi :", question)

        #concatena as perguntas para não esquecer as questões passadas como nome por exemplo
        mensagens.append({"role": "user", "content": str(question)})
        resposta = gerar_resposta(mensagens)

        # adiciona a resposta ao histórico de mensagens
        mensagens.append({"role": "assistant", "content": resposta[0]})

        print("Resposta ChatGPT:", resposta[0])

        # falar a resposta do chat GPT
        if falar:
            fale(resposta[0])

        # pegar custo com base nas palavras enviadas + recebidas
        if pegar_custo:
            gasto = float(resposta[1].total_tokens * valor_por_token)
            print("Voce gastou: USD ", f"{gasto:.10f}")
            print("----------------------------------------------------------")

    else:
        print("Sem comandos!")
        continue

    if pegar_retorno:
        print("Histórico de msgs: ", mensagens)


print("Sistema de voz desligado!")