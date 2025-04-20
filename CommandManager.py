from UserRegistry import UserRegistry
from Messenger import Messenger


class CommandManager:

    def __init__(self):
        self.user_registry = UserRegistry()

    def parse(self, sender, command):
        segments = command.split(" ")
        if not segments:
            return None

        root = segments[0]

        match root.lower():
            case "/msg" | "/m":
                self.handle_message(sender, segments[1:])
            case "/name" | "/n":
                self.handle_name(sender, segments[1:])
            case "/list" | "/l":
                self.handle_list(sender)
            case "/quit" | "/q":
                self.handle_quit(sender)

    def handle_message(self, sender, segments):
        if len(segments) < 2:
            Messenger.server_send(sender, "Invalid command format.")
            return
        if not self.user_registry.socket_exists(sender):
            Messenger.server_send(
                sender, "You must register a name before sending messages."
            )
            return

        recipients, *message = segments
        message = " ".join(message)

        if recipients == "*":
            Messenger.send_multiple(
                self.user_registry.socket_to_name[sender],
                self.user_registry.get_all_sockets(),
                message,
            )
            return

        names = recipients.split(",")

        for name in names:
            if not self.user_registry.name_exists(name):
                Messenger.server_send(
                    sender, "One or more of your recipients do not exist."
                )
                return

        if len(names) == 1:
            Messenger.send(
                self.user_registry.socket_to_name[sender],
                self.user_registry.name_to_socket[names[0]],
                message,
            )
            return

        Messenger.send_multiple(
            self.user_registry.socket_to_name[sender],
            self.user_registry.get_sockets(recipients),
            message,
        )

    def handle_name(self, sender, segments):
        if len(segments) < 1:
            Messenger.server_send(sender, "Invalid command format.")
            return

        name = segments[0]
        if len(name) < 1:
            Messenger.server_send(sender, "Name cannot be empty.")

        if self.user_registry.name_exists(name):
            Messenger.server_send(sender, "Name already taken. Please try again.")
            return

        self.user_registry.register(name, sender)
        Messenger.server_send(sender, "Successfully registered name.")

    def handle_list(self, sender):
        Messenger.server_send(sender, self.user_registry.get_all_names())

    def handle_quit(self, sender):
        self.user_registry.unregister(sender)
