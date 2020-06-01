import sys
import socket


def contain(file_name):
    s = ""
    for count, x in enumerate(clients_files):
        for y in x:
            if file_name in y:
                s += y + " " + clients_info[count][0] + " " + clients_info[count][1] + ","
    if s != "":
        s = s[:-1] + "\n"
    return s


# list of lists: each client has index which contain his msgs
clients_files = []
# list of tuples
clients_info = []

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_ip = '0.0.0.0'
server_port = int(sys.argv[1])
server.bind((server_ip, server_port))
server.listen(5)
while True:
    flag = True
    client_socket, client_address = server.accept()
    data = ""
    tmp = client_socket.recv(1024)
    while not tmp.endswith("\n"):
        data += tmp
        tmp = client_socket.recv(1024)
    data += tmp
    data = data[:-1]
    while flag and data != "":
        data1 = data.split(" ", 2)
        if len(data1) == 3 and data1[0] == "1":
            flag = False
            # save client ip and port
            info = (client_address[0], data1[1])
            clients_info.append(info)
            # save 
            files = data1[2].split(",")
            clients_files.append(files)

        elif len(data1) == 2 and data1[0] == "2":
            flag = False
            client_socket.send(contain(data1[1]) + "\n")

        else:
            data = ""
            tmp = client_socket.recv(1024)
            while not tmp.endswith("\n"):
                data += tmp
                tmp = client_socket.recv(1024)
            data += tmp
            data = data[:-1]

    client_socket.close()
