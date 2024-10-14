import cv2

class SquatAnalyzer:
    def __init__(self):
        # Initialisierung des ArUco-Dictionaries und der Detektorparameter
        self.aruco_dict = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_4X4_250)
        self.parameters = cv2.aruco.DetectorParameters()

    def analyze_frame(self, frame):
        # Umwandeln des Bildes in Graustufen für die Marker-Erkennung
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        
        # Erstellen eines ArUco-Detektors
        detector = cv2.aruco.ArucoDetector(self.aruco_dict, self.parameters)
        
        # Erkennung der Marker im Bild
        corners, ids, rejected = detector.detectMarkers(gray)
        
        if ids is not None:
            # Beispielhafte Berechnung der Knie- und Femurwinkel (Platzhalter)
            knee_angle = 90  # Dieser Wert muss durch echte Berechnungen ersetzt werden
            femur_angle = 45  # Dieser Wert muss durch echte Berechnungen ersetzt werden
            return knee_angle, femur_angle
        
        return None, None

    def is_valid_squat(self, knee_angle, femur_angle):
        """Überprüfung, ob die Kniebeuge basierend auf den Winkeln gültig ist."""
        MIN_KNEE_ANGLE = 80  # Minimaler Winkel für eine gültige Kniebeuge
        MAX_KNEE_ANGLE = 100  # Maximaler Winkel für eine gültige Kniebeuge
        MIN_FEMUR_ANGLE = 40  # Minimaler Femurwinkel
        MAX_FEMUR_ANGLE = 50  # Maximaler Femurwinkel

        # Überprüfung, ob die Winkel innerhalb des gültigen Bereichs liegen
        if MIN_KNEE_ANGLE <= knee_angle <= MAX_KNEE_ANGLE and MIN_FEMUR_ANGLE <= femur_angle <= MAX_FEMUR_ANGLE:
            return True
        return False
