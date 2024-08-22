import sys
import socket
from textual.app import App, ComposeResult
from textual.binding import Binding
from textual.widgets import Header, Footer
from textual import work
from textual.worker import Worker, get_current_worker


class ClientGui(App):
    BINDINGS = [
        Binding(key="q", action="quit_app", description="Quit the app"),
    ]

    def __init__(self, sock):
        super().__init__()
        self.sock = sock

    def compose(self) -> ComposeResult:
        yield Header()
        yield Footer()

    def on_mount(self) -> None:
        self.title = "Fiver"
        self.update_data()

    @work(exclusive=True, thread=True)
    def update_data(self):
        worker = get_current_worker()
        
        print('dd')
        maxBytes = 4096
        data = 0
        while True:
            data += 1
            self.sock.send(str(data).encode())
            modifiedMessage = self.sock.recv(maxBytes)
            modifiedMessage = modifiedMessage.decode()
            print(modifiedMessage)
           

    def action_quit_app(self):
        sys.exit(0)
        
    

def client_app(address):
    try:
        serverIP, serverPort = address.split(':')
    except:
        return print("[error] Ip server is incorrect")
    
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((serverIP, int(serverPort)))
    except socket.error as e:
        return print(f"[error] {e}")

    app = ClientGui(sock)
    app.run()
    
 


    