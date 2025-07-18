from textual.app import App, ComposeResult
from textual.containers import ScrollableContainer
from textual.widgets import Footer, Header, Static, Button

class StopwatchApp(App):

    BINDINGS = [("d", "toggle_theme", "Toggle dark mode")]
    CSS_PATH = "style.css"

    def compose(self) -> ComposeResult:
        yield Header()
        yield Footer()
        with ScrollableContainer(id="stopwatches"):
            yield Stopwatch()
            yield Stopwatch()
            yield Stopwatch()

    def action_toggle_theme(self) -> None:
        self.theme = "textual-dark" if self.theme == "textual-light" else "textual-light"


class Stopwatch(Static):
    def compose(self):

        yield Button("Start", variant="success", id="start")
        yield Button("Stop", variant= "error", id="stop")
        yield Button("Reset", id="reset")
        yield TimeDisplay("00:00:00.00")


class TimeDisplay(Static):
    pass
    # def compose(self):
    #     yield Static("00:00:00")

if __name__ == "__main__":
    app = StopwatchApp()
    app.run()