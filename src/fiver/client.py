import sys
import socket
import json
from textual.app import App, ComposeResult
from textual.binding import Binding
from textual.widget import Widget
from textual.widgets import Header, Footer, Static, ProgressBar, Input, Button, Log
from textual import work
from textual.containers import Horizontal, Container, HorizontalScroll, VerticalScroll
from textual.worker import Worker, get_current_worker
from textual.reactive import reactive


class Info(Widget):
    a = reactive("0")  

  
    def render(self):
        return Horizontal(
            Static("OS:", classes="info_item_name"),
            Static(self.a, classes="info_item_vaule")
        )

class ClientGui(App):
    CSS = """
        Screen {
            scrollbar-size: 1 1;
            overflow-x: scroll;
        }

        .info_area {
            padding-top: 1;
            height: auto;
        }

        .info_item {
            color: white;
            border: solid white;
            padding: 1 2;
            margin-left: 1;
            height: 10;
            width: 40;
        }

        .info_item_name {
            width: 10;
        }

        .info_item_value {
            width: 30;
        }

        .send_file {
            color: white;
            border: solid white;
            padding: 1 2;
            margin: 1;
            height: auto;
        }

        .send_file_button {
            margin-top: 1;
        }

        .terminal {
            color: white;
            border: solid white;
            padding: 1 2;
            margin: 1;
            height: auto;
        }

        .terminal_note {
            margin-bottom: 1;
        }

        .terminal_log {
            background: black;
            padding-left: 1;
            padding-top: 1;
            height: 20;
        }
    """

    BINDINGS = [
        Binding(key="q", action="quit_app", description="Quit the app"),
    ]

    def __init__(self, sock):
        super().__init__()
        self.sock = sock
        self.quit = False

    def compose(self) -> ComposeResult:
        info_item_one = Container(
            Horizontal(
                Static("OS:", classes="info_item_name"),
                Static("dd", classes="info_item_vaule")
            ),
            Info(),
            Static("OS: Ubuntu 22.04 LTS"),
            Static("Kernel: 5.15.0-58-generic"),
            Static("Architecture: x86_64"),
            Static("Uptime: 12 days, 4 hours"),
            Static("CPU: Intel Core i7-10750H"),
            Static("RAM: 32 GB"),
            Static("Storage: 1 TB SSD"),
            classes="info_item",
        )
        info_item_one.border_title = "System Information"

        info_item_two = Container(
            Static("CPU Usage:"),
            Static("Memory Usage:"),
            Static("Disk Usage:"),
            Horizontal(
                Static("Network Usage:", classes="a2"),
                ProgressBar(show_eta=False, show_percentage=False, classes="a1"),  # Adjust value as 
                classes="a3",
            ),    
            classes="info_item",             
        )
        info_item_two.border_title = "Resource Utilization"
        
        send_file = Container(
            Input(placeholder="File path to send"),
            Input(placeholder="Folder path to receive"),
            Static("[bold red][/]", id="send_file_error"),
            Static("[bold green][/]", id="send_file_success"),
            Button("Send", variant="primary", classes="send_file_button"),
            classes="send_file"
        )
        send_file.border_title = "Send file"

        terminal = Container(
            Input(placeholder="Enter command to execute"),
            Static("Enter to send", classes="terminal_note"),
            Log(auto_scroll=True, classes="terminal_log"),
            classes="terminal"
        )
        terminal.border_title = "Terminal"

        yield Header(show_clock=True)
        yield VerticalScroll(
            HorizontalScroll(
                info_item_one,
                info_item_two,
                classes="info_area",
            ),
            send_file,
            terminal,
        )
        yield Footer()

    def on_mount(self) -> None:
        self.title = "Fiver"
        self.update_data()
        log = self.query_one(Log)
        log.write_line("sss")

    @work(exclusive=True, thread=True)
    def update_data(self):
        worker = get_current_worker()
        
        maxBytes = 4096
        data = 0
        while True:
            if self.quit:
                break
            data += 1
            self.sock.send(str(data).encode())
            modifiedMessage = self.sock.recv(maxBytes)
            # modifiedMessage = json.loads(modifiedMessage.decode())
            modifiedMessage = modifiedMessage.decode()
            self.b = str(data)
            print(modifiedMessage)
           

    def action_quit_app(self):
        self.quit = True
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
    
 


    