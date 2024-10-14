import tkinter as tk
from camera import Camera
from squat_analyzer import SquatAnalyzer
import cv2
import threading

class SquatAnalysisApp:
    def __init__(self):
        # GUI-Setup
        self.window = tk.Tk()
        self.window.title("Squat Analysis")

        # Kamera und Analyzer initialisieren
        self.camera = Camera(0)  # Kamera 0 verwenden
        self.analyzer = SquatAnalyzer()

        # Start-Button in der GUI
        self.start_button = tk.Button(self.window, text="Start Measurement", command=self.start_measurement)
        self.start_button.pack()

        self.window.protocol("WM_DELETE_WINDOW", self.on_closing)

    def start_measurement(self):
        # Starten der Messung in einem neuen Thread, um die GUI nicht zu blockieren
        threading.Thread(target=self.measure).start()

    def measure(self):
        while True:
            ret, frame = self.camera.read_frame()
            if not ret:
                break

            # Analyse des aktuellen Frames (Berechnung der Winkel)
            knee_angle, femur_angle = self.analyzer.analyze_frame(frame)

            if knee_angle is not None and femur_angle is not None:
                # Überprüfen, ob die Kniebeuge gültig ist
                if self.analyzer.is_valid_squat(knee_angle, femur_angle):
                    print(f"Gültige Kniebeuge: Kniewinkel = {knee_angle}, Femurwinkel = {femur_angle}")
                else:
                    print(f"Ungültige Kniebeuge: Kniewinkel = {knee_angle}, Femurwinkel = {femur_angle}")

            # Kamerabild im Fenster anzeigen
            cv2.imshow("Squat Analysis", frame)

            # Zum Beenden der Schleife 'q' drücken
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        # Freigabe der Kamera und Schließen der Fenster
        self.camera.release()
        cv2.destroyAllWindows()

    def on_closing(self):
        # Beenden der GUI
        self.camera.release()
        self.window.quit()

if __name__ == "__main__":
    app = SquatAnalysisApp()
    app.window.mainloop()
