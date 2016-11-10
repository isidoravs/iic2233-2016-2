import socket
import sys
import threading
import socket
import pickle


class Server:
	
	def __init__(self, port, host):
		print("Inicializando servidor...")

		# Inicializar socket principal del servidor.
		self.host = host
		self.port = port
		self.socket_servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.bind_and_listen()
		self.accept_connections()
		self.lista_conectados = []


	# El método bind_and_listen() enlazará el socket creado con el host y puerto
	# indicado. Primero se enlaza el socket y luego que esperando por conexiones 
	# entrantes, con un máximo de 5 clientes en espera.
	def bind_and_listen(self):
		self.socket_servidor.bind((self.host, self.port))
		self.socket_servidor.listen(5)  
		print("Servidor escuchando en {}:{}...".format(self.host, self.port))
		
	# El método accept_connections() inicia el thread que aceptará clientes. 
	# Aunque podríamos aceptar clientes en el thread principal de la instancia, 
	# resulta útil hacerlo en un thread aparte que nos permitirá realizar la
	# lógica en la parte del servidor sin dejar de aceptar clientes. Por ejemplo,
	# seguir procesando archivos.
	def accept_connections(self):
		thread = threading.Thread(target=self.accept_connections_thread)
		thread.start()
		
	# El método accept_connections_thread() será arrancado como thread para 
	# aceptar clientes. Cada vez que aceptamos un nuevo cliente, iniciamos un 
	# thread nuevo encargado de manejar el socket para ese cliente.
	def accept_connections_thread(self):
		print("Servidor aceptando conexiones...")

		while True:
			client_socket, _ = self.socket_servidor.accept()
			listening_client_thread = threading.Thread(
				target=self.listen_client_thread,
				args=(client_socket,),
				daemon=True
			)
			self.send(b"nombre", client_socket)
			self.lista_conectados.append(client_socket)
			listening_client_thread.start()

	# Usaremos el método send() para enviar mensajes hacia algún socket cliente. 
	# Debemos implementar en este método el protocolo de comunicación donde los 
	# primeros 4 bytes indicarán el largo del mensaje.
	@staticmethod
	def send(value, socket):
		stringified_value = str(value)
		msg_bytes = pickle.dumps(stringified_value)
		msg_length = len(msg_bytes).to_bytes(4, byteorder="big")
		socket.send(msg_length + msg_bytes)


	# El método listen_client_thread() sera ejecutado como thread que escuchará a un 
	# cliente en particular. Implementa las funcionalidades del protocolo de comunicación
	# que permiten recuperar la informacion enviada.
	def listen_client_thread(self, client_socket):
		print("Servidor conectado a un nuevo cliente...")

		while True:
			response_bytes_length = client_socket.recv(4)
			response_length = int.from_bytes(response_bytes_length, byteorder="big")
			response = b""
			
			while len(response) < response_length:
				response += client_socket.recv(256)

			received = pickle.loads(response)

			
			if received != "":

				if not(isinstance(received, Mensaje)):
					tipo = self.lista_conectados[-1]
					self.lista_conectados.pop()
					tupla = (received, tipo)
					self.lista_conectados.append(tupla)
			
				else:
					for i in received.receptores:
						destinatario = list(filter(lambda x: i == x[0], self.lista_conectados))
						msje = Mensaje(received.row, received.emisor, i, received.mensaje, received.asunto)
						aux = pickle.dump(msje)
						self.send(aux,destinatario[0][1])

				# El método `self.handle_command()` debe ser definido. Este realizará 
				# toda la lógica asociado a los mensajes que llegan al servidor desde 
				# un cliente en particular. Se espera que retorne la respuesta que el 
				# servidor debe enviar hacia el cliente.

			   
	# def handle_command(received, client_socket):
		 
class Mensaje:

	def __init__(self, row, emisor, receptores, mensaje, asunto):
		self.asunto = asunto
		self.row = row
		self.emisor = emisor
		self.mensaje = mensaje
		self.receptores = receptores
				
if __name__ == "__main__":

	port = 10001
	host = socket.gethostname()

	server = Server(port, host)