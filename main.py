import os
import time
import speech_recognition
import pyttsx3
from tkinter import *
from PIL import Image

# Palavra que é necessário falar antes de dar inicio a uma pergunta
wake_word = "conecta"
status = "ausente"

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
    recognizer = speech_recognition.Recognizer()
    microfone = speech_recognition.Microphone()
    with microfone as origemAudio:
        recognizer.adjust_for_ambient_noise(origemAudio)

    print("Escutando microfone...")
    global parar_escutar
    ## O listen_in_background é responsável pelo loop do reconhecimento de voz
    parar_escutar = recognizer.listen_in_background(origemAudio, entenderTextoFalado)
        

"""
Transforma o audio em texto e retorna o resultado
"""
def audioParaTexto(recognizer, audioEscutado):
    textoFalado = ""

    try:
        # Transforma o audio escutado em texto
        textoFalado = recognizer.recognize_google(audioEscutado, language="pt-BR")
    except speech_recognition.UnknownValueError as erro:
        print("Erro: "+str(erro))

    print("Eu escutei: "+textoFalado)
    return textoFalado.lower()

"""
Checa o texto por meio das condições para tentar entender o que foi falado. Se enteder algo, dá uma resposta em audio
"""
def entenderTextoFalado(recognizer, audioEscutado):
    textoFalado = audioParaTexto(recognizer, audioEscutado)
    global status
    global setarExpressao
    resposta = ""

    # Se a palavra definida na variável wake_word tiver aparecido no texto audioEscutado, então aguarda que o usuário faça uma pergunta
    if (status == "ausente" and textoFalado.count(wake_word) > 0):
        setarExpressao("aguardando")
        status = "aguardando"
        resposta = "Ao seu dispor"
    elif (status == "aguardando"):
        status = "respondendo"

        frasesBoasVindas = ["olá", "bom dia", "boa tarde", "boa noite", "quem é"]
        for frase in frasesBoasVindas:
            if frase in textoFalado:
                resposta = "Olá! Eu sou a conecta, fui desenvolvida pelo núcleo de robótica do cesmac e tenho esse lindo chapéu de guerreiro na minha cabeça representando a nossa cultura."

        
    # Responde de acordo com o que foi falado
    if(resposta == "" and status != "ausente"): # Se estivesse aguardando a pergunta mas não entendeu o que foi falado
        resposta = "Desculpa, não entendi o que você falou"
        status = "ausente"
    elif(resposta != "" and status == "respondendo"):   # Se estiver respondendo a pergunta
        setarExpressao("respondendo")
        falar(resposta)
        status = "ausente"
        setarExpressao("ausente")
    elif(resposta != ""):   # Se estiver aguardando a pergunta
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

animacaoGIF = None
setarExpressao("ausente")

escutarMicrofone()

falar("Estou pronta")

janela.mainloop()