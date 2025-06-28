import socket

HOST = '0.0.0.0'
PORT = 45000

def run_client():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        try:
            s.connect((HOST, PORT))
            print(f"Berhasil terhubung ke server {HOST}:{PORT}")
            print("Bisa mengirim command sekarang.")
            print("Ketik 'TIME' untuk get current time, ketik 'QUIT', untuk keluar")
            print("-" * 25)

        except ConnectionRefusedError:
            print(f"Koneksi gagal. Apakah server sedang berjalan di {HOST}:{PORT}?")
            return

        while True:
            message = input("> ")
            
            if not message:
                continue

            formatted_message = message.strip().upper()
            command_to_send = f"{formatted_message}\r\n"
            
            s.sendall(command_to_send.encode('utf-8'))

            if formatted_message == "QUIT":
                print("Mengirim command QUIT. Menutup koneksi.")
                break

            try:
                data = s.recv(1024)
                response = data.decode('utf-8').strip()
                print(f"Server: {response}")
            except ConnectionError:
                print("Koneksi terputus")
                break

if __name__ == "__main__":
    run_client()
