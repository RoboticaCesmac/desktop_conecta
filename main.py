import os
import time
import playsound
import speech_recognition
import pyttsx3

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
            print(textoFalado)
        except Exception as excecao:
            print("Erro: "+str(excecao))
    
    print("Eu escutei: "+textoFalado)
    return textoFalado.lower()


# Função principal (a primeira que inicia)
def main():
    print("Programa iniciado")
    falar("Olá! Eu sou a conecta")

    while True:
        window.read(timeout = 25)

        print("Escutando o microfone")
        audioEscutado = escutar()

        # Se a palavra definida na variável wake_word tiver aparecido no texto audioEscutado, então aguarda que o usuário faça uma pergunta
        if audioEscutado.count(wake_word) > 0:
            print("Palavra de despertar encontrada")
            falar("Ao seu dispor")

            audioEscutado = escutar()
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

# Chama a função principal (inicio)
main()

