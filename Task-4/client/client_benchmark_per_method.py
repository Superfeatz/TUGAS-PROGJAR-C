import socket
import time
import argparse
import base64
from concurrent.futures import ThreadPoolExecutor

FILES = [
    "files/testing.txt",
    "files/donalbebek.jpg",
    "files/pokijan.jpg",
    "files/resources.txt",
    "files/rfc2616.pdf"
]

def send_request(request_bytes, host, port, timeout=3):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(timeout)
        sock.connect((host, port))
        sock.sendall(request_bytes)

        response = b""
        while True:
            data = sock.recv(1024)
            if not data:
                break
            response += data
        sock.close()
        return response
    except Exception as e:
        return str(e).encode()

def benchmark_get_list(n, concurrency, host, port):
    def worker(_):
        request = b"GET /list HTTP/1.0\r\nHost: %s\r\n\r\n" % host.encode()
        return send_request(request, host, port)

    print(f"\n[GET /list] Benchmarking {n} requests @ {host}:{port} ...")
    start = time.time()
    with ThreadPoolExecutor(max_workers=concurrency) as exec:
        results = list(exec.map(worker, range(n)))
    elapsed = time.time() - start
    print(f"Completed {n} requests in {elapsed:.2f}s ({n/elapsed:.2f} req/s)")

def benchmark_upload(n, concurrency, host, port):
    def worker(i):
        filepath = FILES[i % len(FILES)]
        with open(filepath, 'rb') as f:
            encoded = base64.b64encode(f.read())
        filename = filepath.split("/")[-1]
        request = f"POST /upload HTTP/1.0\r\nHost: {host}\r\nX-Filename: {filename}\r\nContent-Length: {len(encoded)}\r\n\r\n"
        return send_request(request.encode() + encoded, host, port)

    print(f"\n[POST /upload] Benchmarking {n} uploads @ {host}:{port} ...")
    start = time.time()
    with ThreadPoolExecutor(max_workers=concurrency) as exec:
        results = list(exec.map(worker, range(n)))
    elapsed = time.time() - start
    print(f"Uploaded {n} files in {elapsed:.2f}s ({n/elapsed:.2f} req/s)")

def benchmark_delete(n, concurrency, host, port):
    filenames = [f.split("/")[-1] for f in FILES]
    def worker(i):
        fname = filenames[i % len(filenames)]
        request = f"GET /delete/{fname} HTTP/1.0\r\nHost: {host}\r\n\r\n"
        return send_request(request.encode(), host, port)

    print(f"\n[GET /delete/<filename>] Benchmarking {n} deletes @ {host}:{port} ...")
    start = time.time()
    with ThreadPoolExecutor(max_workers=concurrency) as exec:
        results = list(exec.map(worker, range(n)))
    elapsed = time.time() - start
    print(f"Deleted {n} files in {elapsed:.2f}s ({n/elapsed:.2f} req/s)")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--method", choices=["get", "upload", "delete"], required=True)
    parser.add_argument("-n", type=int, default=50, help="Jumlah request total")
    parser.add_argument("-c", type=int, default=10, help="Jumlah concurrency")
    parser.add_argument("--host", type=str, default="localhost", help="Target host")
    parser.add_argument("--port", type=int, default=8885, help="Target port")
    args = parser.parse_args()

    if args.method == "get":
        benchmark_get_list(args.n, args.c, args.host, args.port)
    elif args.method == "upload":
        benchmark_upload(args.n, args.c, args.host, args.port)
    elif args.method == "delete":
        benchmark_delete(args.n, args.c, args.host, args.port)

