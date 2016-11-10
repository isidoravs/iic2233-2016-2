from gui import GUI, run
import threading
import socket
import pickle


class MiGUI(GUI):


    def on_signin_dialog_signin_button_click(self, username, password):
        self.nombre = "{}@uc.cl".format(username)
        port = 10001
        host = socket.gethostname()
        self.client = Client(port, host, self.nombre, self)
        return True

    def on_signup_dialog_signup_button_click(self, username, password, confirm_password):
        """Callback luego de presionar el botón `Registrarse` en diálogo de registro.
        Si es que no se está haciendo el BONUS, no se muestra el botón `Registrarse`.

        Retorna:
            bool -- si el registro es exitoso, es verdadero. En otro caso, falso.
        """
        return True

    def on_main_window_load(self):
        """Callback luego de cargarse la ventana principal.
        """
        try:
            with open("db/{}.txt".format(self.nombre), "rb") as file:
                for line in file:
                    msje = pickle.load(line, file)
                    self.add_mail_item(msje.row, msje.emisor, msje.receptores,
                                       msje.asunto)

        except FileNotFoundError:
            pass

    def on_main_window_inbox_button_click(self):
        """Callback luego de presionar el botón `Buzón de entrada` en ventana
        principal.
        """
        pass

    def on_main_window_outbox_button_click(self):
        """Callback luego de presionar el botón `Buzón de salida` en ventana
        principal.
        """
        pass

    def on_main_window_signout_button_click(self):
        """Callback luego de presionar el botón `Desconectarse` en ventana
        principal.
        """
        pass

    def on_main_window_item_double_click(self, row):
        """Callback luego de hacer click en alguna fila de la tabla de la
        ventana principal.

        Argumentos:
            int row -- el índice de la fila dónde se hizo click.
        """
        pass

    def on_compose_widget_send_button_click(self, recipients, subject, msg):
        """Callback luego de presionar el botón `Enviar` en la ventana de
        redacción de correos.

        Argumentos:
            str recipients -- destinatarios de correo.
            str subject    -- asunto del correo.
            str msg        -- cuerpo del correo.
        Retorna:
            bool           -- si el envío es exitoso, retorna verdadero. En
            otro caso, retorna falso.
        """

        resp = recipients.strip().split(";")
        try:
            with open("db/{}.txt".format(self.nombre), "rb") as file:
                row = len(file.readlines())
                msje = Mensaje(row, self.nombre, resp, msg, subject)


        except FileNotFoundError:
            msje = Mensaje(0, self.nombre, resp, msg, subject)

        to_send = pickle.dumps(msje)
        self.client.send(to_send)
        return True


class Mensaje:

    def __init__(self, row, emisor, receptores, mensaje, asunto):
        self.asunto = asunto
        self.row = row
        self.emisor = emisor
        self.mensaje = mensaje
        self.receptores = receptores


class Client:
    def __init__(self, port, host, nombre, gui):
        print("Inicializando cliente...")

        self.host = host
        self.port = port
        self.nombre = nombre
        self.gui = gui
        self.socket_cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        try:
            self.connect_to_server()
            self.listen()
            self.repl()
        except:
            print("Conexión terminada")
            self.socket_cliente.close()
            exit()

    def connect_to_server(self):
        self.socket_cliente.connect((self.host, self.port))
        print("Cliente conectado exitosamente al servidor...")

    def listen(self):
        thread = threading.Thread(target=self.listen_thread, daemon=True)
        thread.start()

    def send(self, msg):
        msg_length = len(msg).to_bytes(4, byteorder="big")
        self.socket_cliente.send(msg_length + msg)

    def listen_thread(self):
        while True:
            response_bytes_length = self.socket_cliente.recv(4)
            response_length = int.from_bytes(response_bytes_length,
                                             byteorder="big")
            response = b""

            # Recibimos datos hasta que alcancemos la totalidad de los datos
            # indicados en los primeros 4 bytes recibidos.
            while len(response) < response_length:
                response += self.socket_cliente.recv(256)

            if response == b"\x80\x03X\t\x00\x00\x00b'nombre'q\x00.":
                self.send(pickle.dumps(self.nombre))

            else:
                msje = pickle.loads(response)
                print(type(msje))
                recep = msje.receptores.strip().split(";")
                self.gui.add_mail_item(msje.row, msje.emisor, recep, msje.asunto)

                # mensaje
                try:
                    with open("db/{}.txt".format(self.nombre), "ab") as file:
                        file.write(response)

                except FileNotFoundError:
                    with open("db/{}.txt".format(self.nombre), "wb") as file:
                        file.write(response)

    # Usaremos este método para capturar input del usuario. Lee mensajes desde
    # el terminal y después se los pasa a `self.send()`.
    def repl(self):  # redactar
        # print("------ Consola ------\n>>> ", end="")
        #
        # while True:
        #     msg = input("")
        #     response = self.send(msg)
        pass


if __name__ == "__main__":
    run(MiGUI)
