import socket, threading
from ClientThread import ClientThread
from CommandManager import CommandManager


class Server:

    def __init__(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.PORT = 80
        self.HOST = "10.0.0.196"
        self.max_connections = 10

        self.client_threads = []
        self.command_manager = CommandManager()

        self.lock = threading.Lock()

        self.socket.bind((self.HOST, self.PORT))
        self.socket.listen(self.max_connections)

    def run(self):
        print("Server started.")

        try:
            self.accept_connections()
        except KeyboardInterrupt:
            print("\nKeyboard interrupt detected.")
        finally:
            self.shutdown()

    def accept_connections(self):
        while True:
            (client_socket, (ip, port)) = self.socket.accept()
            client_thread = ClientThread(client_socket, ip, port, self.command_manager)
            client_thread.start()

            with self.lock:
                self.client_threads.append(client_thread)

    def shutdown(self):
        # Close all client threads
        for thread in self.client_threads:
            thread.socket.close()
            thread.join()

        # Close the server socket
        self.socket.close()
        print("Server closed.")
