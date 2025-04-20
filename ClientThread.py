import threading
from Messenger import Messenger


"""
Handle TCP connections on their own thread.
"""


class ClientThread(threading.Thread):

    def __init__(self, socket, ip, port, command_manager):
        super().__init__()
        self.socket = socket
        self.ip = ip
        self.port = port

        self.command_manager = command_manager
        print(f"Connection from {ip}:{port}")

    def run(self):
        try:
            while True:
                msg = self.recv_until_newline()
                if msg:
                    print(f"Received message: {msg}")
                    self.command_manager.parse(self.socket, msg)
                else:
                    break
        except Exception as e:
            print(f"Error in thread for {self.ip}:{self.port}: {e}")
        finally:
            Messenger.server_send(
                self.socket,
                f"{self.command_manager.user_registry.socket_to_name[self.socket]} has left the server.",
            )
            self.command_manager.handle_quit(self.socket)
            self.socket.close()
            print(f"Connection with {self.ip}:{self.port} closed.")

    def recv_until_newline(self):
        buffer = b""
        while True:
            chunk = self.socket.recv(1024)
            if not chunk:
                return None
            buffer += chunk
            if b"\n" in buffer:
                line = buffer.split(b"\n", 1)[0]
                return line.decode("utf-8")  # Decode the bytes to string
