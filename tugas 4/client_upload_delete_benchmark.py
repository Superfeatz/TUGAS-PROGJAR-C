import socket
import time
import uuid
from concurrent.futures import ThreadPoolExecutor
import argparse

def send_request(method, host, port, path, body="", id=0, timeout=3):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(timeout)
        sock.connect((host, port))

        if method == "POST":
            content_length = len(body)
            request = f"POST {path} HTTP/1.0\r\nHost: {host}\r\nContent-Length: {content_length}\r\n\r\n{body}"
        else:
            request = f"GET {path} HTTP/1.0\r\nHost: {host}\r\n\r\n"

        sock.sendall(request.encode())

        response = b""
        while True:
            try:
                data = sock.recv(1024)
                if not data:
                    break
                response += data
            except socket.timeout:
                # print(f"[{id}] Read timeout after {timeout}s")
                break

        sock.close()
        return True
    except socket.timeout:
        # print(f"[{id}] Timeout after {timeout}s")
        return False
    except Exception as e:
        # print(f"[{id}] {method} failed: {e}")
        return False

def run_upload_delete_benchmark(n, c, host, port, mode, timeout):
    print(f"\nRunning {mode.upper()} benchmark: {n} ops with {c} concurrent threads")
    start_time = time.time()

    def worker(i):
        if mode == "upload":
            content = f"Benchmark upload {i} - {uuid.uuid4()}"
            return send_request("POST", host, port, "/upload", body=content, id=i, timeout=timeout)
        elif mode == "delete":
            fname = filenames[i]
            return send_request("GET", host, port, f"/delete/{fname}", id=i, timeout=timeout)

    success_count = 0
    global filenames
    filenames = []

    # PRE-UPLOAD jika mode delete
    if mode == "delete":
        print(">> Pre-uploading files for deletion...")
        for i in range(n):
            content = f"To be deleted {i} - {uuid.uuid4()}"
            fname = f"{uuid.uuid4().hex}.upload"
            filenames.append(fname)
            send_request("POST", host, port, "/upload", body=content, id=i, timeout=timeout)

    with ThreadPoolExecutor(max_workers=c) as executor:
        futures = [executor.submit(worker, i) for i in range(n)]
        for f in futures:
            if f.result():
                success_count += 1

    total_time = time.time() - start_time
    print(f"\n=== Benchmark Result ===")
    print(f"Target         : http://{host}:{port}")
    print(f"Operation      : {mode.upper()}")
    print(f"Total Requests : {n}")
    print(f"Concurrency    : {c}")
    print(f"Success        : {success_count}")
    print(f"Failed         : {n - success_count}")
    print(f"Time Taken     : {total_time:.2f} sec")
    print(f"Requests/sec   : {n / total_time:.2f} req/s")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--host', default='localhost')
    parser.add_argument('--port', type=int, default=8887)
    parser.add_argument('--mode', choices=['upload', 'delete'], required=True)
    parser.add_argument('-n', type=int, default=10, help='Number of operations')
    parser.add_argument('-c', type=int, default=5, help='Concurrent threads')
    parser.add_argument('--timeout', type=int, default=3, help='Timeout per request (seconds)')
    args = parser.parse_args()

    run_upload_delete_benchmark(args.n, args.c, args.host, args.port, args.mode, args.timeout)

