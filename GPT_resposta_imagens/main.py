# instale pip install openai para importa-lo
import openai

# Sua Key da API aqui:
openai.api_key= "sua_key_aqui"


# função de resposta do Chat GPT
def gerar_resposta(mensagem):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=mensagem,
        max_tokens=50,
        temperature=0.5
    )
    return [response.choices[0].message.content, response.usage]

 # Pedido de geração de imagem ao chat GPT
def gerar_imagem(imagem):
    response = openai.Image.create(
      prompt=imagem,
      n=1,
      size="256x256",
    )
    return response['data'][0]['url']



while True:
    # preparando pra envio de pergunta
    # esse modelo usa um array para perguntas e respostas
    mensagem = []

    # input para a pergunta
    pergunta = input("Digite uma pergunta (ou sair):")

    if pergunta != "sair":
        # adiciona a pergunta ao array
        mensagem.append({"role": "user", "content": str(pergunta)})

        #chama função para gerar a resposta GPT
        resposta = gerar_resposta(mensagem)
        print("Resposta GPT: ", resposta[0])
    print("------------------------------------------------------")




    # Exemplo de uso da função resposta
    imagem = input('Digite a imagem que você quer (ou sair): ')

    if imagem != "sair":
        try:
            link_pra_imagem = gerar_imagem(imagem)
            print(link_pra_imagem)
        except:
            print("Se pedir coisas absurdas ou não aceitáveis GPT treme na base!")
    print("------------------------------------------------------")