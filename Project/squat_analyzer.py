import cv2
import numpy as np

class SquatAnalyzer:
    def __init__(self):
        # Initialisiere das ArUco-Dictionary und die Parameter
        self.aruco_dict = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_4X4_250)
        self.parameters = cv2.aruco.DetectorParameters()

    def analyze_frame(self, frame):
        # Umwandeln des Bildes in Graustufen für die Marker-Erkennung
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Erkennung der Marker im Bild
        detector = cv2.aruco.ArucoDetector(self.aruco_dict, self.parameters)
        corners, ids, rejected = detector.detectMarkers(gray)

        # Zeichne erkannte Marker auf dem Frame (nur Rahmen und IDs)
        if ids is not None:
            cv2.aruco.drawDetectedMarkers(frame, corners, ids)  # Dies zeichnet den Markerrahmen und die ID automatisch
        else:
            print("No markers detected.")  # Debug-Ausgabe falls keine Marker erkannt wurden

        return frame
