from socket import *

TCP_IP = '127.0.0.1'
TCP_PORT = 1229

client_socket = socket(AF_INET, SOCK_STREAM)
client_socket.connect((TCP_IP, TCP_PORT))

try:
    message = input("Digite a mensagem para enviar ao servidor: ").strip()
    if not message:
        print("Mensagem vazia. Encerrando o cliente.")

    client_socket.sendall(message.encode())
    print("Mensagem enviada:", message)

    client_socket.settimeout(10.0)

    response = client_socket.recv(1024)
    print("Resposta recebida:", response.decode())
except timeout:
    print("Tempo limite de resposta atingido. Nenhuma resposta recebida do servidor.")

except ConnectionAbortedError:
        print("⚠  O servidor encerrou a conexão antes de responder (timeout do lado dele).")

finally:
    client_socket.close()
    print("Conexão com o servidor encerrada.")