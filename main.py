import socket
import RadioControlProtocolPy.rcLib as rcLib

sock = socket.socket(socket.AF_INET, socket.SOCK_RAW, 253)
while True:
    data = sock.recv(1024)

    pkg = rcLib.Package(0, 0)

    for d in data:
        if pkg.decode(d):
            print(pkg.channel_data)
