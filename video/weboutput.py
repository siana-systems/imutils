from socketserver import ThreadingMixIn
from queue import Queue
from threading import Thread
from http import HTTPStatus
from http.server import (
    BaseHTTPRequestHandler,
    HTTPServer
)
import numpy, cv2, time, urllib

class CameraHandler(BaseHTTPRequestHandler):
    """Handles HTTP requests from the clients. For this particular case,
    server will return an image stream (.mjpg) when a client sends a GET
    request
    """
    image_queue = {}
    stream_queue = {}

    def do_GET(self):
        """Function called when the web browser generates a GET request
        """
        decoded_path = urllib.parse.unquote(self.path)

        if(decoded_path == '/'):
            # Root path. Shows a list of all files
            self.send_response(HTTPStatus.OK)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(CameraHandler.populate_files().encode('utf-8'))

        if decoded_path[1:] in CameraHandler.image_queue:
            # Selected an existing picture
            self.send_response(HTTPStatus.OK)
            self.send_header('Content-type', 'image/jpeg')
            self.end_headers()

            _, jpg = cv2.imencode('.jpg', CameraHandler.image_queue[decoded_path[1:]])
            self.wfile.write(jpg.tobytes())

        if decoded_path[1:] in CameraHandler.stream_queue:
            # Start mjpg stream
            self.send_response(200)
            self.send_header('Content-type', 'multipart/x-mixed-replace; boundary=--jpgboundary')
            self.end_headers()
            
            previous_image = numpy.zeros((640, 480, 3), numpy.uint8)
            
            while True:
                try:
                    dequeued_image = CameraHandler.stream_queue[decoded_path[1:]].get_nowait()
                except:
                    dequeued_image = previous_image

                _, jpg = cv2.imencode('.jpg', dequeued_image)
                self.wfile.write("--jpgboundary".encode("utf-8"))
                self.send_header('Content-type', 'image/jpeg')
                self.send_header('Content-length', str(jpg.size))
                self.end_headers()
                self.wfile.write(jpg.tostring())

                previous_image = dequeued_image

    def populate_files():
        """Creates an HTML list where each element corresponds to an
        image or video output

        Returns:
            HTML formatted string with the list with elements
        """
        image_list_html = "<ul>"

        for frame in CameraHandler.image_queue:
            image_list_html += "<li><a href=\"/{}\">{}</a></li>".format(
                frame,
                frame
            )

        for stream in CameraHandler.stream_queue:
            image_list_html += "<li><a href=\"/{}\">{}</a></li>".format(
                stream,
                stream
            )

        image_list_html += "</ul>"

        return image_list_html

    def put_image(name, image):
        """Enqueues a frame that will be shown on the HTTP server

        Args:
            frame (array): Bitmap image
        """
        CameraHandler.image_queue[name] = image

    def stream_images(name, image):
        """Enqueues a frame in the video stream that will be shown
        on the HTTP server

        Args:
            name (str): Title of the stream to show
            frame (array): Bitmap image
        """
        if name not in CameraHandler.stream_queue:
            CameraHandler.stream_queue[name] = Queue()


        if(CameraHandler.stream_queue[name].qsize() > 10):
            CameraHandler.stream_queue[name].get_nowait()

        CameraHandler.stream_queue[name].put_nowait(image)

class ThreadedHTTPServer(ThreadingMixIn, HTTPServer):
	"""ThreadedHTTPServer integrates the Threading mixin, meaning
    that now the HTTP server can serve multiple clients, each one
    handled by a separated thread from the pool."""

class HttpStreamOutput:
    """Helper class that implements a HTTP server. It wraps
    methods around the CameraHandler static class to ease the interaction
    between the WebOutput and the static class
    """
    DEFAULT_HOST_ADDRESS = '0.0.0.0'
    DEFAULT_PORT = 8080

    def __init__(self,
                 address: str = DEFAULT_HOST_ADDRESS,
                 port: int = DEFAULT_PORT
                 ):
        """Initializes the server thread

        Args:
            address (str, optional): [description]. Defaults to HttpStreamOutput.DEFAULT_HOST_ADDRESS.
            port (int, optional): [description]. Defaults to HttpStreamOutput.DEFAULT_PORT.
        """
        self._server = ThreadedHTTPServer(
            (address, port),
            CameraHandler
        )
        self._server_thread = Thread(
            target=lambda: self._server.serve_forever()
        )
        self._server_thread.setDaemon(True)
        
    def startServer(self):
        """Starts serving
        """
        self._server_thread.start()

    def stopServer(self):
        """Stops serving
        """
        self._server.socket.close()

    def putImage(self, name, frame):
        """Sends a frame to the HTTP image display

        Args:
            name (str): Title of the frame to show
            frame (array): Bitmap image
        """
        self._server.RequestHandlerClass.put_image(name, frame)

    def streamImage(self, name, frame):
        """Sends a frame to the HTTP video stream

        Args:
            name (str): Title of the stream to show
            frame (array): Bitmap image
        """
        self._server.RequestHandlerClass.stream_images(name, frame)

class WebOutput(HttpStreamOutput):
    """Concrete class that implements a media output for devices that
    doesn't support visual screen output, but count with LAN connection.
    For this purpose, the WebOutput class uses an HTTP server that renders
    both, images and video stream using a fixed address and port.
    """
    def __init__(self, port: int):
        """Initializes the HTTP server

        Args:
            port (int): HTTP server port
        """
        HttpStreamOutput.__init__(self, port=port)

        self.startServer()

    def show(self, name: str, frame):
        """Displays on server the frame. This method creates a new
        list entry that can be accesed in the HTTP server. By clicking
        in this list entry, the image will be displayed in the web browser.

        Args:
            name (str): Title of the frame to show
            frame (array): Bitmap image
        """
        self.putImage(name, frame)

    def stream(self, name: str, frame):
        """Sends a frame to the web server video stream. This method creates
        a new list entry that can be accesed in the HTTP server. The name will
        serve as a reference to the video stream queue, and the frames will
        be enqueued to the video stream queue.

        Args:
            name (str): Title of the stream to show
            frame (array): Bitmap image
        """
        self.streamImage(name, frame)

    def __del__(self):
        """Destroys and finishes all the resources asociated with 
        the screen output. In this case, finish the serving
        """
        self.stopServer()

    def waitForKey(self, delay: int = 0):
        """Waits for a pressed key. Waits indefinitely when delay is = 0, 
        and it waits delay millseconds


        Args:
            delay (int): Delay in milliseconds. 0 is the special value
            that means "forever". 
        """
        if not delay:
            input()
        else:
            time.sleep(delay/1000)

    def clear(self):
        """Remove all images and video stream entries on the webserver
        """
        CameraHandler.image_queue.clear()