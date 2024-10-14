import cv2

class Camera:
    def __init__(self, camera_index=0):  # Hier nehmen wir standardmäßig Kamera 0
        self.cap = cv2.VideoCapture(camera_index)
        if not self.cap.isOpened():
            raise ValueError("Kamera konnte nicht geöffnet werden")

    def read_frame(self):
        ret, frame = self.cap.read()
        if not ret:
            print("Kein Frame von der Kamera gelesen")
        return ret, frame

    def release(self):
        # Freigeben der Kamera
        self.cap.release()
