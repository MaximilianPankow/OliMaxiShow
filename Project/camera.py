import cv2

class Camera:
    def __init__(self, camera_index=0):
        self.camera_index = camera_index
        self.cap = None
        self.is_running = False

    def start(self):
        if self.cap is None:
            self.cap = cv2.VideoCapture(self.camera_index)
            self.is_running = True

    def get_frame(self):
        if self.is_running:
            ret, frame = self.cap.read()
            if ret:
                return frame
        return None

    def stop(self):
        if self.is_running:
            self.is_running = False
            self.cap.release()
            self.cap = None
