# Include libraries
import tkinter as tk
from tkinter import filedialog, messagebox
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt

# View class
class View:

    # Class initialization
    def __init__(self, root, controller):
        """
        Initialize the GUI view for the audio analysis application.
        """

        # Set instance variables
        self.root = root
        self.controller = controller

        # Title
        tk.Label(root, text="SPIDAM Audio Analysis Tool", font=("Arial", 20, "bold")).pack(pady=10)

        # File import selection
        self.file_label = tk.Label(root, text="No file selected", fg="gray", font=("Arial", 12))
        self.file_label.pack()

        self.import_button = tk.Button(root, text="Import Audio File", command=self.load_file, font=("Arial", 12))
        self.import_button.pack(pady=10)

        # Cleaning tools selection
        self.clean_button = tk.Button(root, text="Clean Data", command=self.clean_data, font=("Arial", 12), state="disabled")
        self.clean_button.pack(pady=10)

        # Visualization selection
        tk.Label(root, text="Visualizations", font=("Arial", 16, "bold")).pack(pady=10)

        self.fig, self.ax = plt.subplots(figsize=(8, 4))
        self.ax.set_title("Audio Data Visualization")
        self.ax.set_xlabel("Time")
        self.ax.set_ylabel("Amplitude")
        self.canvas = FigureCanvasTkAgg(self.fig, master=root)
        self.canvas_widget = self.canvas.get_tk_widget()
        self.canvas_widget.pack()

        # Analysis Results section
        self.results_frame = tk.Frame(root)
        self.results_frame.pack(pady=10)

        self.length_label = tk.Label(self.results_frame, text="Length: --- seconds", font=("Arial", 12))
        self.length_label.grid(row=0, column=0, padx=10)

        self.rt60_label = tk.Label(self.results_frame, text="RT60: -- seconds", font=("Arial", 12))
        self.rt60_label.grid(row=0, column=1, padx=10)

        self.resonant_label = tk.Label(self.results_frame, text="Resonant Frequency: -- Hz", font=("Arial", 12))
        self.resonant_label.grid(row=0, column=2, padx=10)

        # Action buttons
        self.analyze_button = tk.Button(root, text="Analyze Audio", command=self.controller.analyze_data, font=("Arial", 12), state="disabled")
        self.analyze_button.pack(pady=10)

    # Load file
    def load_file(self):
        """
        Handles the file import process. Calls the controller to load the file and updates the view.
        """

        filepath = filedialog.askopenfilename(filetypes=[("Audio Files", "*.wav *.mp3 *.m4a"), ("All Files", "*.*")])

        if filepath:

            try:  # attempt to do

                self.controller.load_file(filepath)
                self.file_label.config(text=f"File: {filepath.split('/')[-1]}", fg="black")
                self.clean_button.config(state="normal")
                self.analyze_button.config(state="normal")
            
            except FileNotFoundError as error:

                messagebox.showerror(f"Error: {str(error)}")

    # Clean data
    def clean_data(self):
        """
        Handles data cleaning via the controller.
        """

        try:  # attempt to do
            
            self.controller.clean_data()
            results = self.controller.analyze_data()
            self.update_results(results)
            self.update_visualization(results["waveform"])

        except Exception as error:  # except if an exception arises

            messagebox.showerror(f"Error: {error}")

    # Update results
    def update_results(self, results):
        """
        Updates the displayes analysis results.
        """

        self.length_label.config(text=f"Length: {results['length']:.2f} seconds")
        self.rt60_label.config(text=f"RT60: {results['rt60']:.2f} seconds")
        self.resonant_label.config(text=f"Resonant Frequency: {results['resonant_frequency']:.2f} Hz")

    # Update visualization
    def update_visualization(self, waveform):
        """
        Updates the waveform visualization.
        """

        self.ax.clear()
        self.ax.plot(waveform, label="Waveform")
        self.ax.legend()
        self.ax.set_title("Audio Waveform")
        self.ax.set_xlabel("Time")
        self.ax.set_ylabel("Amplitude")
        self.canvas.draw()