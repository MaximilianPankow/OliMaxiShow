import cv2
import numpy as np

class SquatAnalyzer:
    def __init__(self):
        # Initialisiere das ArUco-Dictionary und die Detektor-Parameter
        self.aruco_dict = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_4X4_250)
        self.parameters = cv2.aruco.DetectorParameters()

        # Squat-Counter und Status-Flag
        self.squat_counter = 0
        self.squat_in_progress = False  # Flag, um zu erkennen, ob sich der Athlet in einem Squat befindet

    def calculate_angle(self, pointA, pointB, pointC):
        """
        Berechnet den Winkel zwischen drei Punkten (in Grad).
        """
        BA = pointA - pointB
        BC = pointC - pointB

        cosine_angle = np.dot(BA, BC) / (np.linalg.norm(BA) * np.linalg.norm(BC))
        angle = np.degrees(np.arccos(cosine_angle))
        return angle

    def calculate_femur_angle(self, hip_position, knee_position):
        """
        Berechnet den Femur-Winkel basierend auf der vertikalen Position von Hüfte und Knie.
        - 0°: Wenn Hüfte und Knie auf derselben Höhe sind.
        - Positiver Winkel: Wenn die Hüfte höher als das Knie ist.
        - Negativer Winkel: Wenn die Hüfte tiefer als das Knie ist.
        """
        # Berechne die Differenz in der y-Koordinate
        y_diff = knee_position[1] - hip_position[1] 
        
        # Der Winkel ist einfach die Differenz in der y-Achse
        return y_diff

    def analyze_frame(self, frame):
        # Bild in Graustufen umwandeln für die Marker-Erkennung
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # ArUco-Detektor erstellen
        detector = cv2.aruco.ArucoDetector(self.aruco_dict, self.parameters)
        corners, ids, rejected = detector.detectMarkers(gray)

        knee_angle = None
        femur_angle = None

        # Wenn Marker erkannt werden, berechne die Winkel und zeichne Linien
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
                    hip_position = np.mean(corners[i][0], axis=0).astype(int)
                elif marker_id == knee_marker_id:
                    knee_position = np.mean(corners[i][0], axis=0).astype(int)
                elif marker_id == ankle_marker_id:
                    ankle_position = np.mean(corners[i][0], axis=0).astype(int)

            # Berechne die Winkel und zeichne Linien, wenn alle Marker erkannt werden
            if hip_position is not None and knee_position is not None and ankle_position is not None:
                # Femur-Winkel korrekt berechnen
                femur_angle = self.calculate_femur_angle(hip_position, knee_position)

                # Knie-Winkel (zwischen Hüfte, Knie und Knöchel)
                knee_angle = self.calculate_angle(hip_position, knee_position, ankle_position)

                # Zeichne eine rote Linie zwischen Hüfte und Knie
                cv2.line(frame, tuple(hip_position), tuple(knee_position), (0, 0, 255), 3)

                # Zeichne eine rote Linie zwischen Knie und Knöchel
                cv2.line(frame, tuple(knee_position), tuple(ankle_position), (0, 0, 255), 3)

                # Squat-Logik: Zählen, wenn der Femur-Winkel 0° oder weniger beträgt
                if femur_angle <= 0:
                    if not self.squat_in_progress:
                        self.squat_counter += 1  # Zähle nur, wenn ein neuer Squat beginnt
                        self.squat_in_progress = True  # Setze das Flag, um mehrfaches Zählen zu verhindern
                else:
                    self.squat_in_progress = False  # Setze das Flag zurück, wenn der Athlet aufsteht

        # Rückgabe von drei Werten sicherstellen, auch wenn keine Marker erkannt wurden
        return knee_angle, femur_angle, frame
