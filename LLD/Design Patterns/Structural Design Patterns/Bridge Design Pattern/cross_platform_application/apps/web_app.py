from .app import App
from responses.response import Response


class WebApp(App):

    """ Handles Web UI """

    def __init__(self, response: Response) -> None:
        super().__init__(response=response)

    def render_ui(self) -> str:
        web_ui_response: Response = super().get_response()
        web_ui_html_str: str = f"WEB_UI_HTML -> {web_ui_response.generate_response()}"
        return web_ui_html_str
