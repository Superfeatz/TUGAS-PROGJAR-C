import socket
import json
import base64
import logging
import os
import base64
server_address = ('localhost', 6677)  # Default ke IP localhost dan port 6677


def upload(file_path):
    """Automatically encode any file to base64 before upload"""
    try:
        with open(file_path, 'rb') as f:
            file_content = f.read()

        # Auto-convert to base64
        b64_content = base64.b64encode(file_content).decode('utf-8')

        # Send to server
        response = self.client.send_request(
            f"UPLOAD {os.path.basename(file_path)} {b64_content}")

        return response

    except Exception as e:
        return {'status': 'ERROR', 'data': str(e)}

def send_command(command_str=""):
    global server_address
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        logging.warning(f"connecting to {server_address}")
        sock.connect(server_address)
        
        logging.warning(f"sending message: {command_str}")
        sock.sendall((command_str + "\r\n\r\n").encode())
        
        # Menerima data dari server
        data_received = ""
        while True:
            data = sock.recv(1024)  # Memperbesar buffer untuk efisiensi
            if data:
                data_received += data.decode()
                if "\r\n\r\n" in data_received:
                    break
            else:
                break
        
        # Memproses respons yang diterima
        json_response = data_received.split("\r\n\r\n")[0]
        hasil = json.loads(json_response)
        logging.warning(f"data received from server: {hasil}")
        return hasil
    except Exception as e:
        logging.warning(f"error during communication: {str(e)}")
        return {"status": "ERROR", "data": str(e)}
    finally:
        sock.close()  # Pastikan socket ditutup


def remote_list():
    command_str = f"LIST"
    hasil = send_command(command_str)
    if (hasil['status'] == 'OK'):
        print("daftar file : ")
        for nmfile in hasil['data']:
            print(f"- {nmfile}")
        return True
    else:
        print(f"Gagal: {hasil['data']}")
        return False


def remote_get(filename=""):
    command_str = f"GET {filename}"
    hasil = send_command(command_str)
    if (hasil['status'] == 'OK'):
        namafile = hasil['data_namafile']
        isifile = base64.b64decode(hasil['data_file'])
        fp = open(namafile, 'wb+')
        fp.write(isifile)
        fp.close()
        print(f"File {namafile} berhasil diunduh")
        return True
    else:
        print(f"Gagal: {hasil['data']}")
        return False


def remote_upload(filepath=""):
    if not os.path.exists(filepath):
        print(f"File {filepath} tidak ditemukan")
        return False
    
    try:
        filename = os.path.basename(filepath)  # Ambil nama file saja
        with open(filepath, 'rb') as fp:
            file_content = base64.b64encode(fp.read()).decode()
        command_str = f"UPLOAD {filename} {file_content}"
        hasil = send_command(command_str)
        if hasil['status'] == 'OK':
            print(f"File {filename} berhasil diupload")
            return True
        else:
            print(f"Gagal: {hasil['data']}")
            return False
    except FileNotFoundError:
        print("File tidak ditemukan")
        return False
    except Exception as e:
        logging.warning(f"Error: {str(e)}")
        return False


def remote_delete(filename=""):
    command_str = f"DELETE {filename}"
    hasil = send_command(command_str)
    if hasil['status'] == 'OK':
        print(f"File {filename} berhasil dihapus")
        return True
    else:
        print(f"Gagal: {hasil['data']}")
        return False


if __name__ == '__main__':
    # Konfigurasi alamat server
    host = input("Masukkan alamat server [default: localhost]: ").strip()
    if not host:
        host = 'localhost'
    
    port_str = input("Masukkan port server [default: 6677]: ").strip()
    if port_str:
        try:
            port = int(port_str)
        except ValueError:
            print("Port harus berupa angka, menggunakan port default 6677")
            port = 6677
    else:
        port = 6677
    
    server_address = (host, port)
    
    logging.basicConfig(level=logging.WARNING, format='%(asctime)s - %(levelname)s - %(message)s')
    logging.warning(f"Client started, connecting to {server_address}")
    
    while True:
        print("\n===== FILE CLIENT =====")
        print("Pilih perintah:")
        print("1. LIST")
        print("2. GET <filename>")
        print("3. UPLOAD <filepath>")
        print("4. DELETE <filename>")
        print("5. EXIT")
        
        command = input("Masukkan perintah: ").strip()
        
        if command == "1":
            remote_list()
        elif command.startswith("2 "):
            filename = command[2:].strip()
            remote_get(filename)
        elif command.startswith("3 "):
            filepath = command[2:].strip()
            remote_upload(filepath)
        elif command.startswith("4 "):
            filename = command[2:].strip()
            remote_delete(filename)
        elif command == "5":
            print("Terima kasih telah menggunakan File Client")
                    print("Perintah tidak valid")
