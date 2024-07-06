import socket
import time

addr = ("127.0.0.1", 1024)
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
counter = 0

try:
    while True:
        message = str(counter).encode('utf-8')
        sock.sendto(message, addr)
        print(f"Sent {counter} to {addr[0]}:{addr[1]}")
        counter += 1
        time.sleep(0.1)

except KeyboardInterrupt:
    print("Ctrl+C")
finally:
    sock.close()
