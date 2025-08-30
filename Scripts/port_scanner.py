import socket

def scan_target(host, ports):
    print(f"Scanning {host} ...")
    for port in ports:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        socket.setdefaulttimeout(1)
        result = sock.connect_ex((host, port))
        if result == 0:
            print(f"[+] Port {port} is OPEN")
        else:
            print(f"[-] Port {port} is CLOSED")
        sock.close()

if __name__ == "__main__":
    target = input("Enter target IP: ")
    ports = [21, 22, 23, 25, 53, 80, 110, 139, 443, 445, 3389]
    scan_target(target, ports)
