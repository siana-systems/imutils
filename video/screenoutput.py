import cv2

class ScreenOutput:
    """Concrete class that implements a multimedia output that 
    requires a screen. For this purpose, the ScreenOutput class
    uses the OpenCV API to display windows, which is already
    based on GTK (or Qt, depending on how OpenCV is built)
    """
    def show(self, name: str, frame):
        """Displays on screen the frame. Subsequent calls of this
        method results in a window refresh. It can be used to display
        motion video

        Args:
            name (str): Title of the frame to show
            frame (array): Bitmap image
        """
        cv2.imshow(name, frame)

    def stream(self, name: str, frame):
        """Sends a frame to screen. Subsequent calls of this method 
        results in a video stream. For this concrete implementation of
        the ScreenOutput, a stream can be achieved by calling the show
        method

        Args:
            name (str): Title of the frame to show
            frame (array): Bitmap image
        """
        self.show(name, frame)

    def __del__(self):
        """Destroys and finishes all the resources asociated with 
        the screen output. Currently there are no resources to destroy
        """
        pass

    def waitForKey(self, delay: int = 0):
        """Waits for a pressed key. Waits indefinitely when delay is <= 0, 
        and it waits delay millseconds


        Args:
            delay (int): Delay in milliseconds. 0 is the special value
            that means "forever". 
        """
        cv2.waitKey(delay)

    def clear(self):
        """Closes all images and streams that are visible during the
        runtime
        """
        cv2.destroyAllWindows()