from socket import *

TCP_IP = '127.0.0.1'
TCP_PORT = 1229

server_socket = socket(AF_INET, SOCK_STREAM)
server_socket.bind((TCP_IP, TCP_PORT))
server_socket.listen(1)
print("Server está ouvindo em {}:{}".format(TCP_IP, TCP_PORT))
try:
    while True:
        conn, addr = server_socket.accept()

        print("Conexão estabelecida com:", addr)

        with conn:

            conn.settimeout(10.0)
            try:  
                data = conn.recv(1024)
                if not data:
                    print(f"Cliente {addr} desconectou sem enviar dados.")
                    continue

                print("Recebido:", data.decode(errors='ignore'))

                resposta = "Mensagem recebida"
                conn.sendall(resposta.encode())

                print("Resposta enviada:", resposta)
            except timeout:
                print(f"Tempo limite de conexão atingido para o cliente {addr}.")
finally:
    server_socket.close()