import socket
import struct
import os

serverName = '127.0.0.1'
serverPort = 1229

def main():
    caminho = input("Digite o caminho do arquivo a ser enviado: ".strip())
    if not os.path.isfile(caminho):
        print(f"[Cliente] O arquivo '{caminho}' não existe.")
        return

    nome_arquivo = os.path.basename(caminho)
    nome_bytes = nome_arquivo.encode('utf-8')

    with open(caminho, 'rb') as f:
        dados = f.read()

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as cli:
        cli.connect((serverName, serverPort))

        # monta tudo e envia
        pacote = (
            struct.pack('!I', len(nome_bytes)) + nome_bytes +
            struct.pack('!Q', len(dados)) + dados
        )
        cli.sendall(pacote)
        print(f"[Cliente] Arquivo '{nome_arquivo}' enviado com sucesso. com {len(dados)} bytes.")

        resposta = cli.recv(1024).decode('utf-8')
        print(f"[Cliente] Resposta do servidor: {resposta}")

if __name__ == "__main__":
    main()
