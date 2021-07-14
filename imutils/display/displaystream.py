# author:    SIANA Systems
# website:   https://www.siana-systems.com

from .weboutput import WebOutput
from .screenoutput import ScreenOutput

class DisplayStream:
    
    def __init__(self, screen: bool = True, port: int = 8080):
        """Creates a frame-streamer instance.
        
        Args:
            screen (bool): true = gstreamer (default), false = web/http on localhost
            port (int): http server port, default = 8080
        """
        self._display = WebOutput(port=port) if not screen else ScreenOutput()

    def show(self, name, frame):
        """Displays an image on the display

        Args:
            frame (array): Image bitmap
        """
        self._display.show(name, frame)

    def stream(self, name: str, frame):
        """Sends image to the frame-streamer

        Args:
            name (str): Stream identifier name
            frame (array): Current frame that needs to be enqueued
        """
        self._display.stream(name, frame)

    def waitForKey(self, delay: int = 0):
        """Blocks until a key is pressed
        """
        self._display.waitForKey(delay)

    def clear(self):
        """Removes the display content
        """
        self._display.clear()