import os
import time
import threading

import speech_recognition
import pyttsx3
from tkinter import *
from PIL import Image

# Palavra que é necessário falar antes de dar inicio a uma pergunta
wake_word = "conecta"

"""
Reproduz em audio o texto passado por parâmetro
"""
def falar(texto):
    pytts = pyttsx3.init("sapi5")
    pytts.setProperty("voice", "brazil")
    pytts.say(texto)
    pytts.runAndWait()
    print("Eu falei: "+texto)


"""
Fica escutando o microfone e chama a função de entender o que foi falado quando é reconhecido algum som
"""
def escutarMicrofone():
    print("Escutando microfone...")
    textoFalado = ""
    recognizer = speech_recognition.Recognizer()

    while textoFalado == "":
        with speech_recognition.Microphone() as origemAudio:
            audioEscutado = recognizer.listen(origemAudio)

        try:
            # Transforma o audio escutado em texto
            textoFalado = recognizer.recognize_google(audioEscutado, language="pt-BR")
        except speech_recognition.UnknownValueError as erro:
            if(str(erro) != ""):
                print("Erro: "+str(erro))

    print("Eu escutei: "+textoFalado)
    return textoFalado.lower()

"""
Checa o texto por meio das condições para tentar entender o que foi falado. Se enteder algo, dá uma resposta em audio
"""
def main():
    while True:
        setarExpressao("ausente")
        textoFalado = escutarMicrofone()
        resposta = ""

        # Se a palavra definida na variável wake_word tiver aparecido no texto audioEscutado, então aguarda que o usuário faça uma pergunta
        if (textoFalado.count(wake_word) > 0):
            setarExpressao("aguardando")
            falar("Ao seu dispor")
            textoFalado = escutarMicrofone()

            frasesBoasVindas = ["olá", "bom dia", "boa tarde", "boa noite", "quem é"]
            for frase in frasesBoasVindas:
                if frase in textoFalado:
                    setarExpressao("respondendo")
                    falar("Olá! Eu sou a conecta, fui desenvolvida pelo núcleo de robótica do cesmac e tenho esse lindo chapéu de guerreiro na minha cabeça representando a nossa cultura. Seu nome é?")
                    setarExpressao("aguardando")
                    nomeFalado = escutarMicrofone()
                    resposta = "Prazer em te conhecer "+nomeFalado

            # Se não tiver entendido o que foi falado
            if(resposta == ""):
                resposta = "Desculpa, não entendi o que você falou"
            
            setarExpressao("respondendo")
            falar(resposta)

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
    global animacaoGIF

    frame = framesGIF[contadorFrame]
    labelExpressao.configure(image=frame)   # Edita o frame apresentado no label

    contadorFrame += 1
    if contadorFrame == len(framesGIF):
        contadorFrame = 0

    # Para manter o GIF animado por meio de um loop (50 Milissegundos por repetição)
    animacaoGIF = janela.after(50, lambda :animarGIFExpressao(framesGIF, contadorFrame))

'''
Função que para qualquer animação que esteja em andamento para poder inicializar a animação da expressão
passada por parâmetro
'''
def setarExpressao(nomeExpressao):
    if(animacaoGIF != None):
        janela.after_cancel(animacaoGIF) # Parar gif que já está sendo reproduzido
        print("Animação antiga parada")

    if nomeExpressao == "aguardando":
        animarGIFExpressao(expressaoAguardando)
    elif nomeExpressao == "respondendo":
        animarGIFExpressao(expressaoRespondendo)
    else:
        animarGIFExpressao(expressaoAusente)

    print("Expressão "+nomeExpressao+" definida")



"""
# # # # Inicialização da Conecta # # # #
"""
falar("Inicializando expressões. Isso pode levar alguns minutos.")

janela = Tk()
janela.title("Conecta")

expressaoAusente = carregarFramesGIF("expressoes/expressao-ausente.gif")
expressaoAguardando = carregarFramesGIF("expressoes/expressao-aguardando.gif")
expressaoRespondendo = carregarFramesGIF("expressoes/expressao-respondendo.gif")

labelExpressao = Label(janela)
labelExpressao.config(bg="black")
labelExpressao.pack()

animacaoGIF = None  # Pra poder parar a animação do GIF posteriormente

falar("Estou pronta")

# Inicia a função main em uma Thread, para que fique rodando ao  mesmo tempo que as funções responsáveis pelas expressões.
threadMain = threading.Thread(target=main, args=())
threadMain.daemon = True    # https://stackoverflow.com/questions/11815947/cannot-kill-python-script-with-ctrl-c
threadMain.start()

janela.mainloop()