from threading import Thread
from os import urandom
from random import randint
from hashlib import sha256
from random import choice
import socket
import pickle


'''
    Host y port de facil acceso
'''
HOST = "192.168.1.181"
PORT = 12336


class Server:
    '''Base de material de clases
    '''
    def __init__(self, port, host):
        # Inicializar socket principal del servidor.
        self.host = host
        self.port = port
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.bind_and_listen()
        self.accept_connections()

        self.connected = dict()  # {id: {"socket": socket, "username": username}}
        self.in_common_game = list()  # jugadores en la sala comun

    # El método bind_and_listen() enlazará el socket creado con el host y puerto
    # indicado. Primero se enlaza el socket y luego que esperando por conexiones
    # entrantes, con un máximo de 5 clientes en espera.
    def bind_and_listen(self):
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen(5)
        print("Servidor escuchando en {}:{}...".format(self.host, self.port))

    # El método accept_connections() inicia el thread que aceptará clientes.
    # Aunque podríamos aceptar clientes en el thread principal de la instancia,
    # resulta útil hacerlo en un thread aparte que nos permitirá realizar la
    # lógica en la parte del servidor sin dejar de aceptar clientes. Por ejemplo,
    # seguir procesando archivos.
    def accept_connections(self):
        thread = Thread(target=self.accept_connections_thread)
        thread.start()

    # El método accept_connections_thread() será arrancado como thread para
    # aceptar clientes. Cada vez que aceptamos un nuevo cliente, iniciamos un
    # thread nuevo encargado de manejar el socket para ese cliente.
    def accept_connections_thread(self):
        print("Servidor aceptando conexiones...")

        while True:
            client_socket, _ = self.server_socket.accept()
            listening_client_thread = Thread(
                target=self.listen_client_thread,
                args=(client_socket,),
                daemon=True
            )
            listening_client_thread.start()

    # Usaremos el método send() para enviar mensajes hacia algún socket cliente.
    # Debemos implementar en este método el protocolo de comunicación donde los
    # primeros 4 bytes indicarán el largo del mensaje.
    @staticmethod
    def send(value, socket):
        if type(value) is bytes:  # pickle
            msg_length = len(value).to_bytes(4, byteorder="big")
            socket.send(msg_length + value)
        elif value == "exit":
            socket.close()
        else:
            stringified_value = str(value)
            msg_bytes = stringified_value.encode()
            msg_length = len(msg_bytes).to_bytes(4, byteorder="big")
            socket.send(msg_length + msg_bytes)

    # El método listen_client_thread() sera ejecutado como thread que escuchará a un
    # cliente en particular. Implementa las funcionalidades del protocolo de comunicación
    # que permiten recuperar la informacion enviada.
    def listen_client_thread(self, client_socket):
        print("Servidor conectado a un nuevo cliente...")
        all_sockets = [value["socket"] for (key, value) in self.connected.items()]

        if client_socket not in all_sockets:
            new_id = len(self.connected)
            self.connected[new_id] = {"socket": client_socket, "username": None}

        while True:
            try:
                response_bytes_length = client_socket.recv(4)
                response_length = int.from_bytes(response_bytes_length,
                                                 byteorder="big")
                response = b""

                while len(response) < response_length:
                    response += client_socket.recv(256)

                received = response.decode()

                if received != "":
                    # El método `self.handle_command()` debe ser definido. Este realizará
                    # toda la lógica asociado a los mensajes que llegan al servidor desde
                    # un cliente en particular. Se espera que retorne la respuesta que el
                    # servidor debe enviar hacia el cliente.
                    response = self.handle_command(received, client_socket)

                    if response is None:
                        return

                    if type(response) is not tuple:
                        self.send(response, client_socket)
                    else:  # respuesta multiusuario
                        resp = response[0]
                        extra = response[1]

                        all_sockets = [value["socket"] for (key, value) in
                                       self.connected.items()]

                        if "added" in extra:
                            self.send(resp, client_socket)
                            for client in all_sockets:
                                self.send(extra, client)

                        else:
                            try:
                                aux = resp.split(";")

                                if aux[0] == "success":
                                    if aux[1] == "game":
                                        i = aux.index("messages")
                                        participants = aux[3:i]
                                        messages = aux[i + 1:]
                                        to_send = [dicc['socket'] for dicc in self.connected.values()
                                                   if dicc['username'] in participants]

                                        rep = ";".join(aux[:i])
                                        all_messages = ";".join(messages)

                                        for socket in to_send:
                                            self.send(rep, socket)
                                            self.send("game;send;{}".format(all_messages),
                                                      socket)

                                elif aux[0] == "game":
                                    if aux[1] == "close":
                                        username = aux[2]
                                        participants = extra
                                        if username in participants:
                                            participants.remove(username)

                                        # elimino game_online
                                        self.send(resp, client_socket)

                                        # muestro como offline RR
                                        to_send = [dicc['socket'] for dicc in self.connected.values()
                                                   if dicc['username'] in participants]

                                        for socket in to_send:
                                            self.send("game;offline;{}".format(username),
                                                      socket)

                                    elif aux[1] == "add":
                                        participants = aux[2:]
                                        to_send = [dicc['socket'] for dicc in self.connected.values()
                                                   if dicc['username'] in participants]

                                        for socket in to_send:
                                            self.send(resp, socket)

                                    elif aux[1] == "send":
                                        participants = aux[3:]

                                        to_send = [dicc['socket'] for dicc in self.connected.values()
                                                   if dicc['username'] in participants]

                                        for socket in to_send:
                                            self.send(";".join(aux[:3]), socket)

                                    elif aux[1] == "start_round":
                                        participants = aux[2:-2]

                                        to_send = [dicc['socket'] for dicc in self.connected.values()
                                                   if dicc['username'] in participants]

                                        for socket in to_send:
                                            self.send(resp, socket)

                                    elif aux[1] == "guess":
                                        user = aux[2]
                                        participants = aux[3:]

                                        to_send = [dicc['socket'] for dicc in self.connected.values()
                                                   if dicc['username'] in participants]

                                        for socket in to_send:
                                            self.send(resp, socket)

                                else:
                                    for client in all_sockets:
                                        self.send(resp, client)

                            except TypeError:
                                for client in all_sockets:
                                    self.send(resp, client)

            except ConnectionResetError:
                break

            except OSError:
                break

    def handle_command(self, received, client_socket):
        aux = received.split(";")

        if "chat" == aux[0]:
            if aux[1] == "start":
                path = received[11:]  # sin chat ni start
                participants = received.split(";")[2:]
                try:
                    with open("db/chats/{}.txt".format(path), "r") as file:
                        all_messages = [text.strip() for text in file]

                except FileNotFoundError:
                    with open("db/chats/{}.txt".format(path), "x") as file:
                        all_messages = list()

                to_send = ["chat"] + all_messages + ["friends"] + participants

                encoded = pickle.dumps(to_send)
                return (encoded, participants)

            elif aux[1] == "send":
                user_sending = aux[2]
                message = aux[3]
                participants = aux[4:]

                format_friends = ";".join(participants)
                resp = "CHAT;{};{}".format(message, format_friends)

                with open("db/chats/{}.txt".format(format_friends), "a") as file:
                    file.write("{}\n".format(message))

                return (resp, participants)

            elif aux[1] == "close":
                i = aux.index("messages")
                friends = ";".join(aux[3:i])

                return "chat;close;{}".format(friends)

        elif "signup" == aux[0]:
            aux = received.split(";")
            username = aux[1]
            password = aux[2]
            try:
                with open("db/users.txt", "rb") as file:
                    dicc_data = pickle.load(file)
                    if username in dicc_data:  # keys
                        return "error;signup"

            except EOFError:  # no hay usuarios
                encoded, sal = encoder("iv")
                dicc_data = {"isidora": [encoded, sal]}

                with open("db/users.txt", "wb") as file:
                    pickle.dump(dicc_data, file)

                if username in dicc_data:  # keys
                    return "error;signup"

            # signup
            with open("db/users.txt", "wb") as file:
                encoded_password, sal = encoder(password)
                user_info = {username: [encoded_password, sal]}
                dicc_data.update(user_info)
                pickle.dump(dicc_data, file)

                for (key, value) in self.connected.items():
                    if value['socket'] == client_socket:
                        self.connected[key]['username'] = username

                return "success;signup;{}".format(username)

        elif "login" == aux[0]:
            aux = received.split(";")
            username = aux[1]
            password = aux[2]

            success = False
            with open("db/users.txt", "rb") as file:
                dicc_data = pickle.load(file)

                for user in dicc_data:
                    if user == username:
                        sal = dicc_data[user][1]
                        decoded_password = decoder(password, sal)
                        if decoded_password == dicc_data[user][0]:
                            success = True
                            break

                if success:

                    for (key, value) in self.connected.items():
                        if value['socket'] == client_socket:
                            self.connected[key]['username'] = username

                    return "success;login;{}".format(username)
                else:
                    return "error;login"

        elif "info" == aux[0]:
            if aux[2] == "friends":
                username = aux[1]

                try:
                    with open("db/friends/{}.txt".format(username), "r") as file:
                        friends_data = [x.strip() for x in file.readlines()]

                except FileNotFoundError:
                    with open("db/friends/{}.txt".format(username), "w"):
                        # creates file
                        friends_data = list()

                try:
                    with open("db/games/{}.txt".format(username), "r") as file:
                        games_data = [x.strip() for x in file.readlines()]

                except FileNotFoundError:
                    with open("db/games/{}.txt".format(username), "w"):
                        # creates file
                        games_data = list()

                to_send = pickle.dumps(["friends"] + friends_data + ["games"] + games_data)
                return to_send

        elif "indata" == aux[0]:
            if "friend" in received:
                aux = received.split(";")
                friend = aux[2]
                username = aux[3]

                with open("db/users.txt", "rb") as file:
                    all_users = pickle.load(file)
                    if friend in all_users:  # keys
                        with open("db/friends/{}.txt".format(username), "a") as file:
                            file.write("{}\n".format(friend))
                        # amigos mutuos
                        with open("db/friends/{}.txt".format(friend), "a") as file:
                            file.write("{}\n".format(username))

                        return ("success;friend;{}".format(friend),
                                "added;{};{}".format(friend, username))
                    else:
                        return "error;friend;{}".format(friend)

        elif "game" == aux[0]:
            if aux[1] == "add":
                participants = aux[3:]
                str_participants = ";".join(participants)

                for user in participants:
                    repeated = False
                    try:
                        with open("db/games/{}.txt".format(user), "r") as file:
                            all_games = [x.strip() for x in file.readlines()]
                            if str_participants in all_games:
                                repeated = True

                    except FileNotFoundError:
                        with open("db/games/{}.txt".format(user), "w"):
                            pass


                    if not repeated:
                        with open("db/games/{}.txt".format(user), "a") as file:
                                file.write("{}\n".format(str_participants))

                return ("game;add;{}".format(str_participants), participants)

            elif aux[1] == "start":
                participants = aux[2:]
                all_users = [v["username"] for v in self.connected.values()]

                for participant in participants:
                    if participant not in all_users:
                        return "error;game;start"

                path = "db/games_record/{}.txt".format(";".join(participants))
                text1 = " ~ Inicio de la partida ~ "
                text2 = " > Participantes:"
                text3 = ", ".join(participants)

                try:
                    with open(path, "a") as file:
                        file.write("{}\n".format(text1))
                        file.write("{}\n".format(text2))
                        file.write("{}\n".format(text3))

                except FileNotFoundError:
                    with open(path, "w") as file:
                        file.write("{}\n".format(text1))
                        file.write("{}\n".format(text2))
                        file.write("{}\n".format(text3))

                with open(path, "r") as file:
                    all_messages = ";".join([x.strip() for x in file.readlines()])

                str_participants = ";".join(participants)
                return ("success;game;start;{};messages;{}".format(str_participants, all_messages),
                        participants)

            elif aux[1] == "send":
                message = aux[2]
                participants = aux[3:]

                path = "db/games_record/{}.txt".format(";".join(participants))

                try:
                    with open(path, "a") as file:
                        file.write("{}\n".format(message))
                except FileNotFoundError:
                    with open(path, "w") as file:
                        file.write("{}\n".format(message))
                except ValueError as err:
                    print(err)

                return (received, [])

            elif aux[1] == "start_round":
                with open("db/words.txt", "r") as file:
                    all_words = file.readlines()
                    selected = choice(all_words).strip()

                aux.append(selected)
                return (";".join(aux), [])

            elif aux[1] == "close":
                participants = aux[3:]
                return (received, participants)

            elif aux[1] == "guess":
                return (received, [])

        elif received == "exit":
            to_remove = None
            for (key, value) in self.connected.items():
                if value["socket"] == client_socket:
                    to_remove = key

            del self.connected[to_remove]
            return "exit"

def encoder(password):
    sal = urandom(randint(32, 64))
    code = password.encode("ascii")

    to_encode = sal + code
    encoded = sha256(to_encode).digest()
    return encoded, sal


def decoder(password, sal):
    aux = password.encode('ascii')
    to_decode = sal + aux
    decoded = sha256(to_decode).digest()
    return decoded


if __name__ == "__main__":
    port = PORT
    host = HOST
    server = Server(port, host)