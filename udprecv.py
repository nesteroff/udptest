import socket
import time

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(("0.0.0.0", 1024))
sock.settimeout(1.0)

received = 0
lost = 0
out_of_order = 0
stat_interval = 3

try:
    print("Receiving")
    expected_counter = 0
    last_stat_time = time.time()
    while True:
        try:
            data, addr = sock.recvfrom(1024)
        except socket.timeout:
            continue

        counter = int(data.decode('utf-8'))
        if expected_counter == 0:
             expected_counter = counter;
        received += 1

        if counter < expected_counter:
            print(f"Out of order {counter}, expected {expected_counter}")
            out_of_order += 1
        elif counter > expected_counter:
            print(f"Expected {expected_counter}, received {counter}")
            lost += counter - expected_counter
            print(f"Lost {lost}, out of order {out_of_order}")
            expected_counter = counter + 1
        else:
            #print(f"Received {counter} from {addr[0]}:{addr[1]}")
            expected_counter += 1

        now = time.time()
        if now - last_stat_time >= stat_interval:
            print(f"Received {received}, lost {lost}, out of order {out_of_order}")
            last_stat_time = now

except KeyboardInterrupt:
    print("Ctrl+C")
    print(f"Received {received}, lost {lost}, out of order {out_of_order}")
finally:
    sock.close()
