import socket
import threading
import mysql.connector

HOST = "0.0.0.0"
PORT = 8080

def handle_client(client_socket):
    try:
        message = client_socket.recv(1024).decode()
        print("[클라이언트 요청]", message)

        if message == "get_users":
            db = mysql.connector.connect(
                host="localhost",
                user="root",
                password="0000",
                database="carot"
            )
            cursor = db.cursor()
            cursor.execute("SELECT * FROM user")
            rows = cursor.fetchall()
            result = "\n".join(str(row) for row in rows)

            client_socket.sendall(result.encode())
        else:
            client_socket.sendall("알 수 없는 명령입니다.".encode())
    except Exception as e:
        print("에러:", e)
    finally:
        client_socket.close()

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen()
print(f"[서버 시작] {HOST}:{PORT}")

while True:
    client_socket, addr = server.accept()
    print(f"[접속됨] {addr}")
    threading.Thread(target=handle_client, args=(client_socket,)).start()
