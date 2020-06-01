from sys import argv
import socket
import os
from os import listdir
from os.path import isfile

# client as server - 1st argv is "0"
if argv[1] == "0":
    # socket for the server
    as_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    dest_ip = argv[2]
    dest_port = int(argv[3])
    as_client.connect((dest_ip, dest_port))

    # set the names of the files in the py's dir as string
    files = ""
    path = os.path.dirname(os.path.abspath(__file__))
    for x in listdir(path):
        if isfile(x):
            files += x + ","
    files = files[:-1]

    # sending server port and files
    as_client.send("1 " + argv[4] + " " + files + "\n")
    as_client.close()

    # start listening
    as_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    as_server_ip = '0.0.0.0'
    as_server_port = int(argv[4])
    as_server.bind((as_server_ip, as_server_port))
    as_server.listen(5)
    while True:
        client_socket, client_address = as_server.accept()
        print client_address
        data = ""
        tmp = client_socket.recv(1024)
        while not tmp.endswith("\n"):
            data += tmp
            tmp = client_socket.recv(1024)
        data += tmp
        data = data[:-1]
        fptr = open(path + "/" + data, "rb")
        for line in fptr:
            client_socket.send(line)
        fptr.close()
        client_socket.shutdown(1)
        client_socket.close()

# client as client - 1st argv is "1"
while argv[1] == "1":
    # socket for the server
    as_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    dest_ip = argv[2]
    dest_port = int(argv[3])
    as_client.connect((dest_ip, dest_port))

    flag = 0

    # send the server "search" request
    msg = raw_input("Search: ")
    if msg != "":
        as_client.send("2 " + msg + "\n")
        # receive the answer
        data = ""
        tmp = as_client.recv(1024)
        while not tmp.endswith("\n"):
            data += tmp
            tmp = as_client.recv(1024)
        data += tmp
        data = data[:-1]
        # start downloading
        files_info = data.split(",")
        # sort the list
        files_info.sort()
        # print list with numbers
        for count, x in enumerate(files_info):
            if len(x.split(" ")) > 1:
                flag += 1
                print str(count + 1) + " " + x.split(" ")[0]
    else:
        files_info = []

    as_client.shutdown(1)
    as_client.close()
    msg = raw_input("Choose: ")

    if flag != 0:
        download = files_info[int(msg) - 1].split(" ")
        # socket for the server
        download_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        download_ip = download[1]
        download_port = int(download[2])
        download_socket.connect((download_ip, download_port))
        # sending file name
        download_socket.send(download[0] + "\n")
        # create the file
        f = open(download[0], 'wb')  # open in binary
        line = download_socket.recv(1024)
        while line != "":
            f.write(line)
            line = download_socket.recv(1024)
        f.close()
        download_socket.shutdown(1)
        download_socket.close()


