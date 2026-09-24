import socket
import pyaudio
import wave
import os
import time

# ============ Configuração UDP ============
UDP_IP = "127.0.0.1"      
UDP_PORT = 1229

# ============ Configuração de áudio ============
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
CHUNK = 1024

ARQUIVO_SAIDA = "gravacao.wav"

# ============ Socket UDP ============
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((UDP_IP, UDP_PORT))
sock.settimeout(0.5)   # permite capturar Ctrl+C

# ============ PyAudio (reprodução ao vivo) ============
audio = pyaudio.PyAudio()
stream = audio.open(
    format=FORMAT,
    channels=CHANNELS,
    rate=RATE,
    output=True,
    frames_per_buffer=CHUNK
)

# ============ Arquivo WAV ============
wf = wave.open(ARQUIVO_SAIDA, "wb")
wf.setnchannels(CHANNELS)
wf.setsampwidth(audio.get_sample_size(FORMAT))   # 2 bytes para paInt16
wf.setframerate(RATE)

# ============ Contadores ============
contador = 0
inicio = None
ultimo_print = time.time()

print(f"Servidor ouvindo em {UDP_IP}:{UDP_PORT}")
print(f"Salvando em: {ARQUIVO_SAIDA}")
print("Pressione Ctrl+C para encerrar.\n")

try:
    while True:
        try:
            data, addr = sock.recvfrom(65507) # Tamanho máximo do pacote UDP

            if inicio is None:
                inicio = time.time()
                print(f"Primeiro pacote recebido de {addr}")

            stream.write(data)      # reproduz ao vivo
            wf.writeframes(data)    # salva no arquivo
            contador += 1

            # Log a cada 1 segundo
            agora = time.time()
            if agora - ultimo_print >= 1.0:
                duracao = contador * CHUNK / RATE
                print(f"Pacotes: {contador} | Duração acumulada: {duracao:.1f}s")
                ultimo_print = agora

        except socket.timeout:
            continue

except KeyboardInterrupt:
    print("\n\nEncerrando servidor...")

finally:
    wf.close()
    stream.stop_stream()
    stream.close()
    audio.terminate()
    sock.close()

    # ============ Relatório final ============
    if os.path.exists(ARQUIVO_SAIDA):
        tamanho = os.path.getsize(ARQUIVO_SAIDA)
        duracao = tamanho / (RATE * 2 * CHANNELS)
        print(f"\n--- Relatório ---")
        print(f"Arquivo: {ARQUIVO_SAIDA}")
        print(f"Tamanho: {tamanho} bytes ({tamanho/1024:.1f} KB)")
        print(f"Duração: {duracao:.2f} segundos")
        print(f"Pacotes recebidos: {contador}")
    else:
        print("Nenhum áudio foi recebido — arquivo não foi criado.")