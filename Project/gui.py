import tkinter as tk
from PIL import Image, ImageTk
import cv2

class SquatGUI:
    def __init__(self, start_callback, stop_callback, reset_callback):
        # Initialize Tkinter window
        self.window = tk.Tk()
        self.window.title("Squat Analysis")
        
        # Canvas for displaying video frames
        self.canvas = tk.Canvas(self.window, width=640, height=480)
        self.canvas.pack()

        # Status label for displaying current system state
        self.status_label = tk.Label(self.window, text="Idle", font=("Helvetica", 14))
        self.status_label.pack()

        # Squat count label
        self.counter_label = tk.Label(self.window, text="Squats: 0", font=("Helvetica", 14))
        self.counter_label.pack()

        # Buttons to start, stop, and reset the measurement process
        self.start_button = tk.Button(self.window, text="Start", command=start_callback)
        self.start_button.pack()
        
        self.stop_button = tk.Button(self.window, text="Stop", command=stop_callback)
        self.stop_button.pack()
        
        self.reset_button = tk.Button(self.window, text="Reset Counter", command=reset_callback)
        self.reset_button.pack()

        # Placeholder for holding the latest image (to prevent garbage collection)
        self.image_tk = None

    def update_status(self, status):
        """Update the status label with the given status."""
        self.status_label.config(text=status)

    def update_counter(self, count):
        """Update the squat counter label with the current count."""
        self.counter_label.config(text=f"Squats: {count}")

    def update_angles(self, knee_angle, femur_angle):
        """Update the status label with the current knee and femur angles."""
        self.status_label.config(text=f"Knee: {knee_angle:.2f}°, Femur: {femur_angle:.2f}°")

    def show_frame(self, frame):
        """Display a video frame in the Tkinter canvas."""
        # Convert the frame from BGR (OpenCV) to RGB (Tkinter compatible)
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        image = Image.fromarray(frame_rgb)
        self.image_tk = ImageTk.PhotoImage(image)
        self.canvas.create_image(0, 0, anchor=tk.NW, image=self.image_tk)

    def start(self):
        """Start the Tkinter main loop (blocking)."""
        self.window.mainloop()
