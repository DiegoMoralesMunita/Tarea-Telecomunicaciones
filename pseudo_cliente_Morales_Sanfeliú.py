#!/usr/bin/env python
'''
--------------------------------------------------------------------------------------------------------------------------------------------------
El audio se envia al servidor usando un mensaje con la siguiente estructura
                                                                                                                                                  
mensaje=[Estado]XXX[Largo_audio]XXX[Bytes_Audio]XXX                                                                                                  
                                                                                                                                                  
La variable 'mensaje' es de tipo string. La descripcion de los campos del string es la siguiente:                                                                                          
[Estado]: Corresponde a una palabra clave que hace referencia a alguna configuracion que debe adoptar el ASR para hacer el reconocimiento.        
          En este caso usaremos como estado la palabra "principal".                                                                               
[Largo_audio]: Corresponde al tamanho en bytes que tiene el audio que sera enviado.                                                                
[Bytes_Audio]: Corresponde a los bytes del audio, donde cada byte se representa como un caracter.
			   (los bytes de audio se concatenan al string como si fueran caracteres)
			   
Un ejemplo de mensaje es el siguiente:

mensaje = "principalXXX16XXXRIFFx%&3#$%d4w&7XXX"

Notas:
- La mayoria de los caracteres que representan a los bytes del audio pueden ser especiales o no imprimibles. Por esta razon,
al tratar de imprimir el mensaje en pantalla pueden aparecer caracteres extranhos.
- Tanto los audios que se entregan como los que son grabados por ustedes estan en formato WAV PCM, por lo que tienen un encabezado particular
que se identifica con el substring "RIFF". Los primeros 4 bytes, al representarlos como caracteres, deben equivaler a la palabra RIFF, como
se muestra en el mensaje de ejemplo. De no ser asi, estan haciendo algo mal.

Una vez que el servidor ASR procese y reconozca el audio, respondera con un string que tiene el siguiente formato:

respuesta_asr= [Texto_reconocido]XXX[Texto_corregido]

Un ejemplo de respuesta del ASR es el siguiente:

respuesta_asr="Yarvis un defensaXXXYarvis defensa"

El string que se considera como resultado del reconocimiento corresponde al del campo [Texto_corregido], que en este caso seria "Yarvis defensa"
--------------------------------------------------------------------------------------------------------------------------------------------------
'''
import code
import socket
import soundfile as sf
import sys
import wave
import codecs as cd
import time as time
# socket.socket( )     #inicializa el socket, se debe especificar su familia y el tipo de socket en los argumentos
# socket.bind( )       #une un socket a algun puerto
# socket.listen( )     #pone al socket en modo de espera para realizar la conexion
# socket.accept( )     #acepta la solicitud de conexion de otro socket
# socket.connect( )    #conecta el socket a un servidor
# socket.send( )       #manda data al receptor
# socket.recv( )       #el emisor recibe la data

# socke.bind((host, puerto))
# socke.listen(5)
# clientsocket, address = socke.accept()
# print(f'conection from {address} has been established')


def escucha_yarvis(archivo):

    assert type(archivo) == str

    puerto = 4100 + 12
    host = "172.17.73.252"

    # inicializar string con el estado y el separador "XXX"

    mensaje = "principalXXX"

    #Abrir y leer audio
    data = open(archivo+'.wav', encoding='iso-8859-1')
    data_1 = str(data.read())

    #calcular tamanho del audio y concatenar al string
    size = len(data_1)
    mensaje = mensaje + str(size)

    #agregar separador "XXX" al string
    mensaje = mensaje + "XXX"

    #leer audio byte a byte y concatenar al string como si fueran caracteres
    mensaje = mensaje + data_1

    #terminar mensaje con separador "XXX"
    mensaje = mensaje + "XXX"

    #establecer conexion socket TCP al servidor en IP y puerto informados
    socke = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    socke.connect((host, puerto))

    #enviar mensaje
    socke.send(bytes(mensaje, 'iso-8859-1'))

    #recibir respuesta
    respuesta_asr = socke.recv(1024)

    #obtener textos reconocidos y corregidos.
    print(respuesta_asr.decode('utf-8'))

# Audio original
print('\n')
t = time.time()
escucha_yarvis('t109')
end = time.time() - t
print('Tiempo de ejecución: '+str(end)+' [s]')
print('\n')

# Audio "Yarvis"
t = time.time()
escucha_yarvis('a')
end = time.time() - t
print('Tiempo de ejecución: '+str(end)+' [s]')
print('\n')

# Audio "que te gusta hacer"
t = time.time()
escucha_yarvis('audio1.0')
end = time.time() - t
print('Tiempo de ejecución: '+str(end)+' [s]')
print('\n')

# Audio unido
t = time.time()
escucha_yarvis('audio1.1')
end = time.time() - t
print('Tiempo de ejecución: '+str(end)+' [s]')
print('\n')

# Audio con ruido de fondo
t = time.time()
escucha_yarvis('audio2.0')
end = time.time() - t
print('Tiempo de ejecución: '+str(end)+' [s]')
print('\n')

# Audio con ruido de fondo, acortado
t = time.time()
escucha_yarvis('audio2.1')
end = time.time() - t
print('Tiempo de ejecución: '+str(end)+' [s]')