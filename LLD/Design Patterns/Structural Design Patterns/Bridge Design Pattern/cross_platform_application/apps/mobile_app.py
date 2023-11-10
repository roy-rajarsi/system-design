from .app import App
from responses.response import Response


class MobileApp(App):

    """ Handles Mobile UI """
    def __init__(self, response: Response) -> None:
        super().__init__(response=response)

    def render_ui(self) -> str:
        mobile_ui_response: Response = super().get_response()
        mobile_ui_html_str: str = f"MOBILE_UI_HTML -> {mobile_ui_response.generate_response()}"
        return mobile_ui_html_str
