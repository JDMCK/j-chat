class Messenger:

    @staticmethod
    def send_multiple(sender_name, sockets, message):
        for socket in sockets:
            socket.sendall(f"[{sender_name}*] {message}\n".encode())

    @staticmethod
    def send(sender_name, socket, message):
        socket.sendall(f"[{sender_name}] {message}".encode())

    @staticmethod
    def server_send(socket, message):
        Messenger.send("SERVER", socket, message)
