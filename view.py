# Include libraries
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog, messagebox
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from scipy.io import wavfile
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
        self.index = 0
        self.index = 0

        # Title
        tk.Label(root, text="SPIDAM Audio Analysis Tool", font=("Arial", 20, "bold")).pack(anchor=tk.CENTER)

        # File import selection
        self.file_label = tk.Label(root, text="No file selected", fg="gray", font=("Arial", 12))
        self.file_label.pack(anchor=tk.CENTER)

        self.import_button = tk.Button(root, text="Import Audio File", command=self.load_file, font=("Arial", 12))
        self.import_button.place(anchor=tk.W, y=630, x=210)

        # Cleaning tools selection
        self.clean_button = tk.Button(root, text="Analyze Audio", command=self.clean_data, font=("Arial", 12), state="disabled")
        self.clean_button.place(anchor=tk.W, y=630, x=400)

        # Tabs for data display
        self.tabControl = ttk.Notebook(root)
        self.tab1 = ttk.Frame(self.tabControl)
        self.tab2 = ttk.Frame(self.tabControl)
        self.tab6 = ttk.Frame(self.tabControl)

        self.tabControl.add(self.tab1, text='Waveform')
        self.tabControl.add(self.tab2, text='RT60 Cycle Graphs')
        self.tabControl.add(self.tab6, text='Intensity Graph')

        self.tabControl.place(x=15, y=100)

        # Visualization selection: Waveform
        tk.Label(root, text="Visualizations", font=("Arial", 16, "bold")).place(x=300, y=575)

        self.fig, self.ax = plt.subplots(figsize=(7, 4))
        self.ax.set_title("Audio Data Visualization")
        self.ax.set_xlabel("Time: Seconds")
        self.ax.set_ylabel("Amplitude")
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.tab1)
        self.canvas_widget = self.canvas.get_tk_widget()
        self.canvas_widget.grid(row = 1, column = 1)

        # Visualization selection: RT60 Cycle graph
        self.fig1, self.ax1 = plt.subplots(figsize=(7, 4))
        self.ax1.set_title("Audio Data Visualization")
        self.ax1.set_xlabel("Time: Seconds")
        self.ax1.set_ylabel("Amplitude")
        self.canvas1 = FigureCanvasTkAgg(self.fig1, master=self.tab2)
        self.canvas_widget1 = self.canvas1.get_tk_widget()
        self.canvas_widget1.pack()

        self.rt60_button = tk.Button(self.tab2, text="Cycle RT60 Graphs", command=self.cycle_rt60, font=("Arial", 10))
        self.rt60_button.place(x=225, y=409)

        # Combined RT60 graph button
        self.rt60_combined_button = tk.Button(self.tab2, text="Combined RT60 Graph", command=self.update_combined_rt60, font=("Arial", 10))
        self.rt60_combined_button.pack(side="right", padx=190, pady=8)

        # Visualization selection: Intensity
        self.fig5, self.ax5 = plt.subplots(figsize=(7, 4))
        self.ax5.set_title("Intensity")
        self.ax5.set_xlabel("Time: Seconds")
        self.ax5.set_ylabel("Frequency: Hertz")
        self.canvas5 = FigureCanvasTkAgg(self.fig5, master=self.tab6)
        self.canvas_widget5 = self.canvas5.get_tk_widget()
        self.canvas_widget5.pack()

        # Analysis Results section
        self.results_frame = tk.Frame(root)
        self.results_frame.pack(pady=10)

        self.length_label = tk.Label(self.root, text="Length: --- seconds", font=("Arial", 12))
        self.length_label.place(x=730, y=120)

        self.rt60_label = tk.Label(self.root, text="RT60: -- seconds", font=("Arial", 12))
        self.rt60_label.place(x=730, y=150)

        self.difference_label = tk.Label(self.root, text="RT60 .05 Difference: -- seconds", font=("Arial", 12))
        self.difference_label.place(x=730, y=180)

        self.resonant_label = tk.Label(self.root, text="Resonant Frequency: -- Hz", font=("Arial", 12))
        self.resonant_label.place(x=730, y=210)

        # Play/stop button
        self.play_button = tk.Button(root, text="Play", command=self.toggle_play, font=("Arial", 12))
        self.play_button.place(anchor=tk.W, y=670, x=210)


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
            self.results = self.controller.analyze_data()
            self.update_results(self.results)
            self.update_visualization(self.results["waveform"])
            self.cycle_rt60()
            self.update_combined_rt60()

        except Exception as error:  # except if an exception arises

            messagebox.showerror(f"Error: {error}")

    # Update results
    def update_results(self, results):
        """
        Updates the displayes analysis results.
        """

        self.length_label.config(text=f"Length: {results['length']:.2f} seconds")
        self.rt60_label.config(text=f"RT60: {results['rt60']:.2f} seconds")
        self.difference_label.config(text=f"RT60 .5 Difference: {results['rt60'] - 0.5:.2f} seconds")
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
        self.ax.set_xlabel("Time: Seconds")
        self.ax.set_ylabel("Amplitude")
        self.canvas.draw()


    def update_combined_rt60(self):
        self.ax1.clear()

        self.ax1.set_title("RT60 Combined")
        self.ax1.set_xlabel("Time: Seconds")
        self.ax1.set_ylabel("Power: dB")

        rt60_low = self.results["rt60_low"]
        rt60_mid = self.results["rt60_mid"]
        rt60_high = self.results["rt60_high"]

        #RT60 low
        self.ax1.plot(rt60_low[0], rt60_low[1], linewidth=1, alpha=0.7)
        self.ax1.plot(rt60_low[2], rt60_low[5], 'ro')
        self.ax1.plot(rt60_low[3], rt60_low[6], 'yo')
        self.ax1.plot(rt60_low[4], rt60_low[7], 'go')

        #RT60 mid
        self.ax1.plot(rt60_mid[0], rt60_mid[1], linewidth=1, alpha=0.7)
        self.ax1.plot(rt60_mid[2], rt60_mid[5], 'ro')
        self.ax1.plot(rt60_mid[3], rt60_mid[6], 'yo')
        self.ax1.plot(rt60_mid[4], rt60_mid[7], 'go')

        #RT60 high
        self.ax1.plot(rt60_high[0], rt60_high[1], linewidth=1, alpha=0.7)
        self.ax1.plot(rt60_high[2], rt60_high[5], 'ro')
        self.ax1.plot(rt60_high[3], rt60_high[6], 'yo')
        self.ax1.plot(rt60_high[4], rt60_high[7], 'go')

        self.canvas1.draw()

    def cycle_rt60(self):
        try:
            self.ax1.clear()

            self.ax1.set_xlabel("Time: Seconds")
            self.ax1.set_ylabel("Power: dB")

            # determine which rt60 plot to show
            if self.index%3 == 0:
                self.ax1.set_title("RT60 Low")
                rt60_data = self.results["rt60_low"]
            elif self.index%3 == 1:
                self.ax1.set_title("RT60 Mid")
                rt60_data = self.results["rt60_mid"]
            elif self.index%3 == 2:
                self.ax1.set_title("RT60 High")
                rt60_data = self.results["rt60_high"]

            if rt60_data:
                self.ax1.plot(rt60_data[0], rt60_data[1], linewidth=1, alpha=0.7, color='#004bc6')
                self.ax1.plot(rt60_data[2], rt60_data[5], 'ro')  # Plot points for RT60 data
                self.ax1.plot(rt60_data[3], rt60_data[6], 'go')
                self.ax1.plot(rt60_data[4], rt60_data[7], 'yo')


            self.canvas1.draw()

            self.index += 1
            self.index = self.index%3

        except:
            pass

    def update_intensity(self):
        self.ax5.clear()
        self.ax5.set_title("Intensity")
        self.ax5.set_xlabel("Time: Seconds")
        self.ax5.set_ylabel("Frequency: Hz")
        sample_rate, data = wavfile.read(self.results)
        spectrum, freqs, t, im = plt.specgram(data, Fs=sample_rate, NFFT=1024, cmap=plt.get_cmap('autumn_r'))
        cbar = plt.colorbar(im)
        self.canvas5.draw()