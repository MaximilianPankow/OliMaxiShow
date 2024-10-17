import tkinter as tk
from camera import Camera
from squat_analyzer import SquatAnalyzer
import cv2

class SquatAnalysisApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Squat Analysis")

        # Initialize the camera
        self.camera = Camera()  # Create an instance of Camera class
        self.analyzer = SquatAnalyzer()  # Create an instance of SquatAnalyzer class
        self.measurement_running = False  # Flag to control measurement state

        # Create buttons
        self.start_button = tk.Button(self.root, text="Start Measurement", command=self.start_measurement)
        self.start_button.pack(pady=10)

        self.stop_button = tk.Button(self.root, text="Stop Measurement", command=self.stop_measurement)
        self.stop_button.pack(pady=10)

        self.reset_button = tk.Button(self.root, text="Reset Counter", command=self.reset_counter)
        self.reset_button.pack(pady=10)

        self.squat_count_label = tk.Label(self.root, text="Squat Count: 0")
        self.squat_count_label.pack(pady=10)

        self.knee_angle_label = tk.Label(self.root, text="Knee Angle: N/A")
        self.knee_angle_label.pack(pady=10)

        self.femur_angle_label = tk.Label(self.root, text="Femur Angle: N/A")
        self.femur_angle_label.pack(pady=10)

        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)  # Handle window close event

    def start_measurement(self):
        self.measurement_running = True
        self.camera.start()  # Start the camera
        self.update_frame()  # Start the frame update loop

    def update_frame(self):
        if self.measurement_running:
            frame = self.camera.get_frame()  # Get the current frame from the camera
            if frame is not None:
                knee_angle, femur_angle, frame_with_markers = self.analyzer.analyze_frame(frame)

                if knee_angle is not None:
                    self.knee_angle_label.config(text=f"Knee Angle: {knee_angle:.2f}°")
                if femur_angle is not None:
                    self.femur_angle_label.config(text=f"Femur Angle: {femur_angle:.2f}°")

                cv2.imshow("Camera Feed", frame_with_markers)

            self.root.after(30, self.update_frame)

    def stop_measurement(self):
        self.measurement_running = False
        self.camera.stop()
        cv2.destroyAllWindows()

    def reset_counter(self):
        self.squat_count_label.config(text="Squat Count: 0")

    def on_closing(self):
        self.stop_measurement()
        self.root.destroy()

if __name__ == "__main__":
    app = SquatAnalysisApp()
    app.root.mainloop()
