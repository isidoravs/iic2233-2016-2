from gui import GUI, run
from threading import Thread
from PyQt4.QtCore import QObject, SIGNAL
import socket
import pickle


'''
    Host y port de facil acceso
'''
HOST = "192.168.1.181"
PORT = 12336


class Client(QObject):
    '''Base de material de clases
    '''
    def __init__(self, port, host, username, gui):
        print("Inicializando cliente...")
        super().__init__()

        # Inicializamos el socket principal del cliente
        self.host = host
        self.port = port
        self.username = username
        self.gui = gui

        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        try:
            self.connect_to_server()
            self.listen()
        except:
            print("Conexion terminada")
            self.client_socket.close()
            exit()

    def connect_to_server(self):
        self.client_socket.connect((self.host, self.port))
        print("Cliente conectado exitosamente al servidor...")

    # El método listen() inicilizará el thread que escuchará los mensajes del
    # servidor. Es útil hacer un thread diferente para escuchar al servidor
    # ya que de esa forma podremos tener comunicación asíncrona con este, es decir,
    # el servidor nos podrá enviar mensajes sin necesidad de iniciar una solicitud
    # desde el lado del cliente.
    def listen(self):
        thread = Thread(target=self.listen_thread, daemon=True)
        thread.start()

    # El método send() enviará mensajes al servidor. Implementa el mismo
    # protocolo de comunicación que mencionamos, es decir, agregar 4 bytes
    # al principio de cada mensaje indicando el largo del mensaje enviado.
    def send(self, msg):
        msg_bytes = msg.encode()
        msg_length = len(msg_bytes).to_bytes(4, byteorder="big")
        self.client_socket.send(msg_length + msg_bytes)

    # La función listen_thread() será lanzada como thread el cual se encarga
    # de escuchar al servidor. Vemos como se encarga de recibir 4 bytes que
    # indicarán el largo de los mensajes. Posteriormente recibe en bloques de
    # 256 bytes el resto del mensaje hasta que éste se recibe totalmente.
    def listen_thread(self):
        while True:
            response_bytes_length = self.client_socket.recv(4)
            response_length = int.from_bytes(response_bytes_length,
                                             byteorder="big")
            response = b""

            # Recibimos datos hasta que alcancemos la totalidad de los datos
            # indicados en los primeros 4 bytes recibidos.
            while len(response) < response_length:
                response += self.client_socket.recv(256)

            try:
                self.handle_command(response.decode())
            except UnicodeDecodeError:  # pickle (lista)
                decoded = pickle.loads(response)
                if decoded[0] == "friends":
                    self.handle_command("gui;start", extra=decoded[1:])
                elif decoded[0] == "chat":
                    self.handle_command("chat;start", extra=decoded[1:])

    def handle_command(self, message, extra=None):
        aux = message.split(";")
        if aux[0] == "CHAT":
            chat = aux[1]
            participants = aux[2:]
            if self.username in participants:
                self.emit(SIGNAL("send_chat"), participants, chat)

        if aux[0] == "chat":
            if aux[1] == "start":
                print("Comenzando chat...")
                i = extra.index("friends")
                messages = extra[:i]
                participants = extra[i + 1:]

                # en caso de no pertenecer al chat
                if self.username not in participants:
                    return

                self.emit(SIGNAL("start_chat"), messages, participants)

            elif aux[1] == "close":
                participants = ";".join(aux[2:])
                self.emit(SIGNAL("close_chat"), participants)

        elif aux[0] == "error":
            if "signup" in message:
                self.gui.login.set_message("Username not available")
                self.gui.login.button_signup_done.hide()
                self.gui.login.button_aux.hide()

            elif "login" in message:
                self.gui.login.set_message("Incorrect username / password")
                self.gui.login.button_login_done.hide()
                self.gui.login.button_aux.hide()

            elif "friend" in message:  # usuario no encontrado
                self.gui.programillo.set_message("Usuario no encontrado")
                self.gui.programillo.label_find.setText("")

            elif aux[1] == "game":
                if aux[2] == "start":
                    self.emit(SIGNAL("start_game"), False)

        elif aux[0] == "success":
            if "signup" in message:
                username = message.split(";")[2]
                self.gui.username = username
                self.send("info;{};friends".format(self.gui.username))

            elif "login" in message:
                username = message.split(";")[2]
                self.gui.username = username
                self.send("info;{};friends".format(self.gui.username))

            elif aux[1] == "friend":
                self.emit(SIGNAL("add_friend"))

            elif aux[1] == "game":
                if aux[2] == "start":
                    participants = aux[3:]
                    self.emit(SIGNAL("start_game"), True, participants)

        elif aux[0] == "added":
            friend = message.split(";")[1]
            new_friend = message.split(";")[2]

            if friend == self.username:  # lo agrego new_friend
                self.gui.programillo.label_find.setText(new_friend)
                self.gui.programillo.add_friend()

        elif aux[0] == "gui":
            if "start" in message:
                i = extra.index("games")
                friends = extra[:i]
                games = extra[i + 1:]
                self.gui.friends = friends
                self.gui.games = games

        elif aux[0] == "game":
            if aux[1] == "add":
                participants = aux[2:]
                self.emit(SIGNAL("add_game"), ";".join(participants))

            elif aux[1] == "close":
                self.emit(SIGNAL("no_game"))

            elif aux[1] == "offline":
                user = aux[2]
                self.emit(SIGNAL("user_offline"), user)

            elif aux[1] == "send":
                chat = aux[2:]
                for c in chat:
                    self.emit(SIGNAL("send_game_chat"), c)

            elif aux[1] == "start_round":
                self.emit(SIGNAL("start_round"), aux[-1], aux[-2])

            elif aux[1] == "guess":
                self.emit(SIGNAL("game_guess"), aux[2])


class MiGUI(GUI):
    def __init__(self):
        super().__init__()

    def connect_login(self, username, password):  # password encoded
        self.login.button_aux.show()
        if self.client is None:
            self.client = Client(PORT, HOST, username, self)
        self.client.send("login;{};{}".format(username, password))

    def connect_signup(self, username, password):
        self.login.button_aux.show()
        if self.client is None:
            self.client = Client(PORT, HOST, username, self)
        self.client.send("signup;{};{}".format(username, password))


if __name__ == "__main__":
    run(MiGUI)
