import sys
import socket
import json
import logging
import ssl
import os
import argparse

server_address = ('0.0.0.0',8899)
#server_address = ('0.0.0.0',8885)



def make_socket(destination_address='localhost', port=12000):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_address = (destination_address, port)
        logging.warning(f"connecting to {server_address}")
        sock.connect(server_address)
        return sock
    except Exception as ee:
        logging.warning(f"error {str(ee)}")


def make_secure_socket(destination_address='localhost', port=10000):
    try:
        # get it from https://curl.se/docs/caextract.html

        context = ssl.create_default_context()
        context.check_hostname = False
        context.verify_mode = ssl.CERT_NONE
        context.load_verify_locations(os.getcwd() + '/domain.crt')

        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_address = (destination_address, port)
        logging.warning(f"connecting to {server_address}")
        sock.connect(server_address)
        secure_socket = context.wrap_socket(sock, server_hostname=destination_address)
        logging.warning(secure_socket.getpeercert())
        return secure_socket
    except Exception as ee:
        logging.warning(f"error {str(ee)}")



def send_command(command_str, is_secure=False):
    alamat_server = server_address[0]
    port_server = server_address[1]
    #    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # gunakan fungsi diatas
    if is_secure == True:
        sock = make_secure_socket(alamat_server, port_server)
    else:
        sock = make_socket(alamat_server, port_server)

    logging.warning(f"connecting to {server_address}")
    try:
        logging.warning(f"sending message ")
        sock.sendall(command_str.encode())
        logging.warning(command_str)
        # Look for the response, waiting until socket is done (no more data)
        data_received = ""  # empty string
        while True:
            # socket does not receive all data at once, data comes in part, need to be concatenated at the end of process
            data = sock.recv(2048)
            if data:
                # data is not empty, concat with previous content
                data_received += data.decode()
                if "\r\n\r\n" in data_received:
                    break
            else:
                # no more data, stop the process by break
                break
        # at this point, data_received (string) will contain all data coming from the socket
        # to be able to use the data_received as a dict, need to load it using json.loads()
        hasil = data_received
        logging.warning("data received from server:")
        return hasil
    except Exception as ee:
        logging.warning(f"error during data receiving {str(ee)}")
        return False

def upload_file(content):
    cmd = f"""POST /upload HTTP/1.0\r\nContent-Length: {len(content)}\r\n\r\n{content}"""
    print(send_command(cmd))

def list_files():
    cmd = "GET /list HTTP/1.0\r\n\r\n"
    print(send_command(cmd))

def delete_file(fname):
    cmd = f"GET /delete/{fname} HTTP/1.0\r\n\r\n"
    print(send_command(cmd))

#> GET / HTTP/1.1
#> Host: www.its.ac.id
#> User-Agent: curl/8.7.1
#> Accept: */*
#>

if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('--list', action='store_true', help='List files in server directory')
    parser.add_argument('--upload', type=str, help='Upload string content as file')
    parser.add_argument('--delete', type=str, help='Delete a file on the server')

    args = parser.parse_args()

    if args.list:
        print(">> Listing files on server")
        print(send_command("GET /list HTTP/1.0\r\n\r\n"))
    
    if args.upload:
        content = args.upload
        cmd = f"""POST /upload HTTP/1.0\r\nContent-Length: {len(content)}\r\n\r\n{content}"""
        print(">> Uploading file...")
        print(send_command(cmd))
    
    if args.delete:
        filename = args.delete
        cmd = f"GET /delete/{filename} HTTP/1.0\r\n\r\n"
        print(f">> Deleting file: {filename}")
        print(send_command(cmd))
    
    if not any(vars(args).values()):
        print(">> Default: Listing files")
        print(send_command("GET /list HTTP/1.0\r\n\r\n"))

