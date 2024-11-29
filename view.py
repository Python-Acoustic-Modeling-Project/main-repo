# Include libraries
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog, messagebox
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import pygame

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
        self.is_playing = False

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

        # Tabs for data display
        self.tabControl = ttk.Notebook(root)
        self.tab1 = ttk.Frame(self.tabControl)
        self.tab2 = ttk.Frame(self.tabControl)
        self.tab3 = ttk.Frame(self.tabControl)
        self.tab4 = ttk.Frame(self.tabControl)
        self.tab5 = ttk.Frame(self.tabControl)
        self.tab6 = ttk.Frame(self.tabControl)

        self.tabControl.add(self.tab1, text='Waveform')
        self.tabControl.add(self.tab2, text='RT60 Low')
        self.tabControl.add(self.tab3, text='RT60 Mid')
        self.tabControl.add(self.tab4, text='RT60 High')
        self.tabControl.add(self.tab5, text='Combined RT60')
        self.tabControl.add(self.tab6, text='Tab 6')

        self.tabControl.pack(expand=1, fill="both")

        # Visualization selection: Waveform
        tk.Label(root, text="Visualizations", font=("Arial", 16, "bold")).pack(pady=10)

        self.fig, self.ax = plt.subplots(figsize=(8, 4))
        self.ax.set_title("Audio Data Visualization")
        self.ax.set_xlabel("Time")
        self.ax.set_ylabel("Amplitude")
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.tab1)
        self.canvas_widget = self.canvas.get_tk_widget()
        self.canvas_widget.pack()

        # Visualization selection: RT60 Low
        self.fig1, self.ax1 = plt.subplots(figsize=(8, 4))
        self.ax1.set_title("Audio Data Visualization")
        self.ax1.set_xlabel("Time")
        self.ax1.set_ylabel("Amplitude")
        self.canvas1 = FigureCanvasTkAgg(self.fig1, master=self.tab2)
        self.canvas_widget1 = self.canvas1.get_tk_widget()
        self.canvas_widget1.pack()

        # Visualization selection: RT60 Medium
        self.fig2, self.ax2 = plt.subplots(figsize=(8, 4))
        self.ax2.set_title("Audio Data Visualization")
        self.ax2.set_xlabel("Time")
        self.ax2.set_ylabel("Amplitude")
        self.canvas2 = FigureCanvasTkAgg(self.fig2, master=self.tab3)
        self.canvas_widget2 = self.canvas2.get_tk_widget()
        self.canvas_widget2.pack()

        # Visualization selection: RT60 High
        self.fig3, self.ax3 = plt.subplots(figsize=(8, 4))
        self.ax3.set_title("Audio Data Visualization")
        self.ax3.set_xlabel("Time")
        self.ax3.set_ylabel("Amplitude")
        self.canvas3 = FigureCanvasTkAgg(self.fig3, master=self.tab4)
        self.canvas_widget3 = self.canvas3.get_tk_widget()
        self.canvas_widget3.pack()

        # Visualization selection: RT60 High
        self.fig4, self.ax4 = plt.subplots(figsize=(8, 4))
        self.ax4.set_title("Audio Data Visualization")
        self.ax4.set_xlabel("Time")
        self.ax4.set_ylabel("Amplitude")
        self.canvas4 = FigureCanvasTkAgg(self.fig4, master=self.tab5)
        self.canvas_widget4 = self.canvas4.get_tk_widget()
        self.canvas_widget4.pack()

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

        # Play/stop button
        self.play_button = tk.Button(root, text="Play", command=self.toggle_play)
        self.play_button.pack(pady=10)


        # Initialize pygame mixer
        pygame.mixer.init()

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
                self.play_button.config(state="normal")
            
            except FileNotFoundError as error:

                messagebox.showerror(f"Error: {str(error)}")

    # Toggle play
    def toggle_play(self):
        """
        Calls the controller to play or stop the audio.
        """

        if self.play_button['text'] == 'Play':

            self.controller.play_audio()
            self.play_button.config(text="Stop")

        else:

            self.controller.stop_audio()
            self.play_button.config(text="Play")
    
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
            self.update_rt60_low(results["rt60_low"])
            self.update_rt60_mid(results["rt60_mid"])
            self.update_rt60_high(results["rt60_high"])
            self.update_combined_rt60(results["rt60_low"], results["rt60_mid"], results["rt60_high"])

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

    # Update visualization
    def update_rt60_low(self, rt60_low):
        """
        Updates the rt60_low visualization.
        """

        self.ax1.clear()
        self.ax1.plot(title = "RT60 Low")
        self.ax1.set_xlabel("Time: Seconds")
        self.ax1.set_ylabel("Power: dB")
        self.ax1.plot(rt60_low[0], rt60_low[1],linewidth=1, alpha=0.7, color='#004bc6')
        self.ax1.plot(rt60_low[2], rt60_low[5], 'ro')
        self.ax1.plot(rt60_low[3], rt60_low[6], 'go')
        self.ax1.plot(rt60_low[4], rt60_low[7], 'yo')
        self.canvas1.draw()

    def update_rt60_mid(self, rt60_mid):
        """
        Updates the rt60_mid visualization.
        """
        self.ax2.clear()
        self.ax2.plot(title = "RT60 Mid")
        self.ax2.set_xlabel("Time: Seconds")
        self.ax2.set_ylabel("Power: dB")
        self.ax2.plot(rt60_mid[0], rt60_mid[1],linewidth=1, alpha=0.7, color='#004bc6')
        self.ax2.plot(rt60_mid[2], rt60_mid[5], 'ro')
        self.ax2.plot(rt60_mid[3], rt60_mid[6], 'go')
        self.ax2.plot(rt60_mid[4], rt60_mid[7], 'yo')
        self.canvas2.draw()

    def update_rt60_high(self, rt60_high):
        """
        Updates the rt60_high visualization.
        """
        self.ax3.clear()
        self.ax3.plot(title = "RT60 High")
        self.ax3.set_xlabel("Time: Seconds")
        self.ax3.set_ylabel("Power: dB")
        self.ax3.plot(rt60_high[0], rt60_high[1],linewidth=1, alpha=0.7, color='#004bc6')
        self.ax3.plot(rt60_high[2], rt60_high[5], 'ro')
        self.ax3.plot(rt60_high[3], rt60_high[6], 'go')
        self.ax3.plot(rt60_high[4], rt60_high[7], 'yo')
        self.canvas3.draw()

    def update_combined_rt60(self, rt60_low, rt60_mid, rt60_high):
        self.ax4.clear()
        self.ax4.plot(title="Combined RT60")
        self.ax4.set_xlabel("Time: Seconds")
        self.ax4.set_ylabel("Power: dB")
        self.ax4.plot(rt60_low[0], rt60_low[1], linewidth=1, alpha=0.7)
        self.ax4.plot(rt60_low[2], rt60_low[5], 'ro')
        self.ax4.plot(rt60_low[3], rt60_low[6], 'go')
        self.ax4.plot(rt60_low[4], rt60_low[7], 'yo')
        self.ax4.plot(rt60_mid[0], rt60_mid[1], linewidth=1, alpha=0.7)
        self.ax4.plot(rt60_mid[2], rt60_mid[5], 'ro')
        self.ax4.plot(rt60_mid[3], rt60_mid[6], 'go')
        self.ax4.plot(rt60_mid[4], rt60_mid[7], 'yo')
        self.ax4.plot(rt60_high[0], rt60_high[1], linewidth=1, alpha=0.7)
        self.ax4.plot(rt60_high[2], rt60_high[5], 'ro')
        self.ax4.plot(rt60_high[3], rt60_high[6], 'go')
        self.ax4.plot(rt60_high[4], rt60_high[7], 'yo')

        self.canvas4.draw()
