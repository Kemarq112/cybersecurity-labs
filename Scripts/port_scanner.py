#!/usr/bin/env python3
import argparse
import socket

def parse_ports(port_spec: str):
    """Accepts '22,80,443' or '1-1024' (or a mix) and returns a sorted list of ports."""
    ports = []
    for part in port_spec.split(","):
        part = part.strip()
        if not part:
            continue
        if "-" in part:
            start, end = part.split("-", 1)
            start, end = int(start), int(end)
            ports.extend(range(start, end + 1))
        else:
            ports.append(int(part))
    # keep only valid port numbers and dedupe
    ports = sorted({p for p in ports if 1 <= p <= 65535})
    return ports

def scan(host: str, ports, timeout: float = 1.0):
    open_ports = []
    for p in ports:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.settimeout(timeout)
            try:
                # connect_ex returns 0 on success (open port)
                if sock.connect_ex((host, p)) == 0:
                    open_ports.append(p)
            except Exception:
                # ignore DNS/timeouts/other transient errors per port
                pass
    return open_ports

def main():
    parser = argparse.ArgumentParser(
        description="Simple TCP port scanner (educational use)."
    )
    parser.add_argument(
        "target",
        help="Target IP or hostname (e.g., 192.168.1.10 or example.com)",
    )
    parser.add_argument(
        "-p",
        "--ports",
        default="21,22,23,25,53,80,110,139,443,445,3389",
        help='Ports to scan. Use "22,80,443" or a range like "1-1024".',
    )
    parser.add_argument(
        "-t", "--timeout", type=float, default=1.0, help="Timeout per port in seconds."
    )
    args = parser.parse_args()

    try:
        target_ip = socket.gethostbyname(args.target)
    except socket.gaierror:
        print(f"[!] Could not resolve target: {args.target}")
        return

    ports = parse_ports(args.ports)
    if not ports:
        print("[!] No valid ports to scan.")
        return

    print(f"Scanning {args.target} ({target_ip}) on {len(ports)} port(s)...")
    open_ports = scan(target_ip, ports, timeout=args.timeout)

    if open_ports:
        print("\nOpen ports:")
        for p in open_ports:
            print(f"  - {p}")
    else:
        print("No open ports found in the selected range.")

if __name__ == "__main__":
    main()
