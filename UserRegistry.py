class UserRegistry:

    def __init__(self):
        self.name_to_socket = {}
        self.socket_to_name = {}

    def register(self, name, socket):
        if socket in self.socket_to_name:
            self.unregister(socket)
        self.name_to_socket[name] = socket
        self.socket_to_name[socket] = name

    def unregister(self, socket):
        if self.socket_exists(socket):
            name = self.socket_to_name[socket]
            del self.socket_to_name[socket]
            del self.name_to_socket[name]

    def get_sockets(self, names):
        return [self.name_to_socket[name] for name in names]

    def socket_exists(self, socket):
        return socket in self.socket_to_name

    def name_exists(self, name):
        return name in self.name_to_socket

    def get_all_names(self):
        return ", ".join(self.name_to_socket.keys())

    def get_all_sockets(self):
        return self.socket_to_name.keys()
