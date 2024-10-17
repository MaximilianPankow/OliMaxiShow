import cv2
import numpy as np

class SquatAnalyzer:
    def __init__(self):
        # Initialisiere das ArUco-Dictionary und die Detektor-Parameter
        self.aruco_dict = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_4X4_250)
        self.parameters = cv2.aruco.DetectorParameters()

    def calculate_angle(self, pointA, pointB, pointC):
        """
        Berechnet den Winkel zwischen drei Punkten (in Grad).
        """
        BA = pointA - pointB
        BC = pointC - pointB

        cosine_angle = np.dot(BA, BC) / (np.linalg.norm(BA) * np.linalg.norm(BC))
        angle = np.degrees(np.arccos(cosine_angle))
        return angle

    def analyze_frame(self, frame):
        # Bild in Graustufen umwandeln für die Marker-Erkennung
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # ArUco-Detektor erstellen
        detector = cv2.aruco.ArucoDetector(self.aruco_dict, self.parameters)
        corners, ids, rejected = detector.detectMarkers(gray)

        knee_angle = None
        femur_angle = None

        # Wenn Marker erkannt werden, berechne die Winkel
        if ids is not None:
            cv2.aruco.drawDetectedMarkers(frame, corners, ids)

            hip_marker_id = 1
            knee_marker_id = 12
            ankle_marker_id = 123

            hip_position = None
            knee_position = None
            ankle_position = None

            for i, marker_id in enumerate(ids.flatten()):
                if marker_id == hip_marker_id:
                    hip_position = np.mean(corners[i][0], axis=0)
                elif marker_id == knee_marker_id:
                    knee_position = np.mean(corners[i][0], axis=0)
                elif marker_id == ankle_marker_id:
                    ankle_position = np.mean(corners[i][0], axis=0)

            if hip_position is not None and knee_position is not None and ankle_position is not None:
                femur_angle = self.calculate_angle(hip_position, knee_position, np.array([knee_position[0] + 100, knee_position[1]]))
                knee_angle = self.calculate_angle(hip_position, knee_position, ankle_position)

        # Rückgabe von drei Werten sicherstellen, auch wenn keine Marker erkannt wurden
        return knee_angle, femur_angle, frame
