import socket
import struct
import os

serverName = '127.0.0.1'
serverPort = 1229
PASTA_UPLOAD = 'uploads'

os.makedirs(PASTA_UPLOAD, exist_ok=True)

def recv_exato(conn, n):
    """Lê exatamente n bytes do socket conn."""
    dados = b''
    while len(dados) < n:
        pacote = conn.recv(n - len(dados))
        if not pacote:
            return None
        dados += pacote
    return dados


def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as srv:
        srv.bind((serverName, serverPort))
        srv.listen(1)
        print(f"[Servidor] Escutando em {serverName}:{serverPort}")

        conn, addr = srv.accept()
        with conn:
            print(f"[Servidor] Conectado com {addr}")

            # 1) tamanho do nome do arquivo (4 bytes)
            nome_len= struct.unpack('!I', recv_exato(conn, 4))[0]

            # 2) nome do arquivo
            nome_arquivo = recv_exato(conn, nome_len).decode('utf-8')

            # 3) tamanho do imagem (8 bytes)
            img_len = struct.unpack('!Q', recv_exato(conn, 8))[0]

            # 4) bytes da imagem
            dados = recv_exato(conn, img_len)

            # 5) salva
            caminho = os.path.join(PASTA_UPLOAD, nome_arquivo)
            with open(caminho, 'wb') as f:
                f.write(dados)

            print(f"[Servidor] {nome_arquivo} salvo com sucesso em {caminho} com {img_len} bytes.")

            # 6) confirmação de recebimento
            conn.sendall(b'Arquivo recebido com sucesso!')

            print(f"[Servidor] Conexão com {addr} encerrada.")

if __name__ == "__main__":
    main()
