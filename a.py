import sys

from textual.app import App, ComposeResult
from textual.binding import Binding
from textual.widgets import Footer, Static, ProgressBar, Header
from textual.containers import Horizontal, Vertical, Container, ScrollableContainer


class ClientGui(App):
    CSS = """
        Screen {
            scrollbar-size: 1 1;
        }

        .title {
            text-style: bold;
        }

        .card {
            background: red 20%;
            color: red;
            border: solid red;
            height: 150%;
        }
    """

    BINDINGS = [
        Binding(key="q", action="quit_app", description="Quit the app"),
    ]

    def compose(self) -> ComposeResult:
        a = Container(
                Static("System Information"),
                Static("OS: Ubuntu 22.04 LTS"),
                Static("Kernel: 5.15.0-58-generic"),
                Static("Architecture: x86_64"),
                Static("Uptime: 12 days, 4 hours"),
                Static("CPU: Intel Core i7-10750H"),
                Static("RAM: 32 GB"),
                Static("Storage: 1 TB SSD"),
                classes="card",
            )
        a.border_title = "< Left"
        b = Header(show_clock=True)
    
        yield ScrollableContainer(
            b,
            Horizontal(
                a,
                Container(
                    Static("System Information"),
                    Static("OS: Ubuntu 22.04 LTS"),
                    Static("Kernel: 5.15.0-58-generic"),
                    Static("Architecture: x86_64"),
                    Static("Uptime: 12 days, 4 hours"),
                    Static("CPU: Intel Core i7-10750H"),
                    Static("RAM: 32 GB"),
                    Static("Storage: 1 TB SSD"),
                    classes="card",
                ),
                Container(
                    Static("Resource Utilization"),
                    Static("CPU Usage:"),
                    Static("Memory Usage:"),
                    Static("Disk Usage:"),
                    Static("Network Usage:"),
                    ProgressBar(),  # Adjust value as needed
                    ProgressBar(),  
                    ProgressBar(),  
                    classes="card",
                ),
                Container(
                    Static("Logs"),
                    Static("System Logs: 1,234"),
                    Static("Application Logs: 567"),
                    Static("Security Logs: 89"),
                    Static("Last Updated: 2 minutes ago"),
                    classes="card",
                ),
                classes="dashboard-grid",
            ),
            classes="main-container",
        )

        yield Footer()

    def on_mount(self) -> None:
        self.title = "Header Application"
        self.sub_title = "With title and sub-title"

    def action_quit_app(self):
        sys.exit(0)
        

if __name__ == "__main__":
    app = ClientGui()
    app.run()
