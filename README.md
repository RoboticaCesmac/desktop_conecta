# Inteligência da Robô Conecta

Essa aplicação permite que você faça uma pergunta à Conecta após falar a palavra "Conecta". Perguntas como quem é a conecta, sobre o que é o núcleo de robótica, como ela está, que horas são, o que é o submarino rov, entre outras. A aplicação responde a pergunta e apresenta na tela uma animação representando as expressões de seus olhos, de acordo com seu status (ausente, aguardando pergunta e respondendo).

## Tecnologia

Esse projeto foi desenvolvido com [Python](https://www.python.org/downloads/) e faz uso das dependências listadas abaixo: <br/>

### `pip install SpeechRecognition`
"SpeechRecognition" para reconhecer a voz e transformá-la em texto

### `pip install pyaudio`
"pyaudio" possibilita a captura de sons através do microfone

### `pip install pyttsx3`
"pyttsx3" para transformar texto em audio

### `pip install pillow`
"pillow" foi utilizado na interface gráfica

## Configuração

Em breve explicação sobre como colocar para iniciar automaticamente ao ligar a raspberry.

## Scripts disponíveis

No diretório do projeto, você pode rodar:

### `python main.py`

Para iniciar a aplicação.

## O que falta?

- Otimizar a interface gráfica (Qualidade da animação do GIF e troca de expressões) <br/>
- Otimizar a ação de escutar. Talvez tentar colocar um timeout para que ele não espere acabar de falar pra poder tentar entender a pergunta, porque às vezes fica travado quando tá muito barulho <br/>
- Adicionar mamis perguntas

## Links que podem ser úteis

[Playlist: Python Voice Assistant](https://www.youtube.com/watch?v=-AzGZ_CHzJk&list=PLzMcBGfZo4-mBungzp4GO4fswxO8wTEFx) <br/>
[Explicação em português sobre o speech_recognition](https://letscode.com.br/blog/speech-recognition-com-python)
