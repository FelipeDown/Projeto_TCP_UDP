import socket
import pyaudio
import time

# ============ Configuração UDP ============
UDP_IP = "127.0.0.1"    
UDP_PORT = 1229

# ============ Configuração de áudio ============
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
CHUNK = 1024

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# ============ PyAudio (captura do microfone) ============
audio = pyaudio.PyAudio()
stream = audio.open(
    format=FORMAT,
    channels=CHANNELS,
    rate=RATE,
    input=True,
    frames_per_buffer=CHUNK
)

# ============ Contador ============
enviados = 0
inicio = time.time()
ultimo_print = time.time()

print(f"Enviando áudio para {UDP_IP}:{UDP_PORT}")
print("Pressione Ctrl+C para encerrar.\n")

try:
    while True:
        data = stream.read(CHUNK, exception_on_overflow=False)
        sock.sendto(data, (UDP_IP, UDP_PORT))
        enviados += 1

        # Log a cada 1 segundo
        agora = time.time()
        if agora - ultimo_print >= 1.0:
            duracao = enviados * CHUNK / RATE
            print(f"Pacotes enviados: {enviados} | Duração: {duracao:.1f}s")
            ultimo_print = agora

except KeyboardInterrupt:
    print("\n\nEncerrando cliente...")

finally:
    stream.stop_stream()
    stream.close()
    audio.terminate()
    sock.close()

    duracao_total = time.time() - inicio
    print(f"\n--- Relatório ---")
    print(f"Pacotes enviados: {enviados}")
    print(f"Tempo total: {duracao_total:.2f} segundos")
    print(f"Taxa: {enviados/duracao_total:.1f} pacotes/s")