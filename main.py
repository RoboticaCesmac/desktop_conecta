import os
import time
import speech_recognition
import pyttsx3
from tkinter import *
from PIL import Image

# Palavra que é necessário falar antes de dar inicio a uma pergunta
wake_word = "conecta"


# Reproduz em audio o texto passado por parâmetro
def falar(texto):
    pytts = pyttsx3.init("sapi5")
    pytts.setProperty("voice", "brazil")
    pytts.say(texto)
    pytts.runAndWait()
    print("Eu falei: "+texto)


# Transforma em texto o que foi escutado do microfone
def escutar():
    recognizer = speech_recognition.Recognizer() 
    with speech_recognition.Microphone() as origemAudio:
        # Guarda o audio escutado do microphone
        audioEscutado = recognizer.listen(origemAudio)
        textoFalado = ""
        
        try:
            # Transforma o audio escutado em texto
            textoFalado = recognizer.recognize_google(audioEscutado, language="pt-BR")
            print("Eu escutei: "+textoFalado)
        except Exception as excecao:
            print("Erro: "+str(excecao))
    
    return textoFalado.lower()


# Função principal (a primeira que inicia)
# def main():
#     print("Programa iniciado")
#     falar("Olá! Eu sou a conecta")

#     while True:
#         print("Escutando o microfone")
#         audioEscutado = escutar()

#         # Se a palavra definida na variável wake_word tiver aparecido no texto audioEscutado, então aguarda que o usuário faça uma pergunta
#         if audioEscutado.count(wake_word) > 0:
#             print("Palavra de despertar encontrada")
#             falar("Ao seu dispor")

#             audioEscutado = escutar()
#             resposta = ""

#             # Tenta entender a pergunta
#             frasesBoasVindas = ["olá", "bom dia", "boa tarde", "boa noite", "quem é"]
#             for frase in frasesBoasVindas:
#                 if frase in audioEscutado:
#                     falar("Olá! Eu sou a conecta, fui desenvolvida pelo núcleo de robótica do cesmac e tenho esse lindo chapéu de guerreiro na minha cabeça representando a nossa cultura. Qual o seu nome?")
#                     nome_pessoa = escutar()
#                     resposta = "Prazer em te conhecer "+nome_pessoa

#             # Responde de acordo com o que foi perguntado
#             if(resposta == ""):
#                 resposta = "Desculpa, não entendi o que você falou"

#             falar(resposta)


def main():
    print("Escutando o microfone")
    # setarExpressao("ausente")
    audioEscutado = escutar()

    # Se a palavra definida na variável wake_word tiver aparecido no texto audioEscutado, então aguarda que o usuário faça uma pergunta
    if audioEscutado.count(wake_word) > 0:
        print("Palavra de despertar encontrada")
        # setarExpressao("aguardando")
        falar("Ao seu dispor")

        audioEscutado = escutar()
        # setarExpressao("respondendo")
        resposta = ""

        # Tenta entender a pergunta
        frasesBoasVindas = ["olá", "bom dia", "boa tarde", "boa noite", "quem é"]
        for frase in frasesBoasVindas:
            if frase in audioEscutado:
                falar("Olá! Eu sou a conecta, fui desenvolvida pelo núcleo de robótica do cesmac e tenho esse lindo chapéu de guerreiro na minha cabeça representando a nossa cultura. Qual o seu nome?")
                nome_pessoa = escutar()
                resposta = "Prazer em te conhecer "+nome_pessoa

        # Responde de acordo com o que foi perguntado
        if(resposta == ""):
            resposta = "Desculpa, não entendi o que você falou"

        falar(resposta)
    
    ## Após 50 milissegundos a função main é chamada novamente
    janela.after(50, main)



# Chama a função principal (inicio)
# main()

'''
Função recebe por parâmetro o caminho de uma imagem animada GIF e retorna um array com cada frame da animação
que pode ser usado para animá-lo na janela da interface gráfica
'''
def carregarFramesGIF(caminhoImagem):
    imagem = Image.open(caminhoImagem)
    quantidadeFrames = imagem.n_frames
    return [PhotoImage(file=caminhoImagem, format = f'gif -index {i}') for i in range(quantidadeFrames)]

'''
Função que recebe um array com os frames da imagem animada GIF e fica responsável por mantê-la animada
no label presente na janela da interface gráfica
'''
def animarGIFExpressao(framesGIF, contadorFrame = 0):
    frame = framesGIF[contadorFrame]
    labelExpressao.configure(image=frame)

    contadorFrame += 1
    if contadorFrame == len(framesGIF):
        contadorFrame = 0

    animacaoGIF = janela.after(50, lambda :animarGIFExpressao(framesGIF, contadorFrame))

'''
Função que para qualquer animação que esteja em andamento para poder inicializar a animação da expressão
passada por parâmetro
'''
def setarExpressao(nomeExpressao):
    if(animacaoGIF != None):
        janela.after_cancel(animacaoGIF)

    if nomeExpressao == "aguardando":
        animarGIFExpressao(expressaoAguardando)
    elif nomeExpressao == "respondendo":
        animarGIFExpressao(expressaoRespondendo)
    else:
        animarGIFExpressao(expressaoAusente)

    print("Expressão "+nomeExpressao+" definida")



falar("Inicializando Conecta")

janela = Tk()
janela.title("Conecta")

expressaoAusente = carregarFramesGIF("expressoes/expressao-ausente.gif")
# expressaoAguardando = carregarFramesGIF("expressoes/expressao-aguardando.gif")
# expressaoRespondendo = carregarFramesGIF("expressoes/expressao-respondendo.gif")

labelExpressao = Label(janela)
labelExpressao.pack()

animacaoGIF = None
# setarExpressao("ausente")
# animarGIFExpressao(expressaoAusente)

## Após 50 milissegundos a função main é chamada
janela.after(50, main)

falar("Conecta inicializada")

janela.mainloop()

