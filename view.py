# Include libraries
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog, messagebox
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.pyplot import colorbar
from scipy.io import wavfile
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
        self.file_imported = False  # keeps track of if audio file has been imported yet
        self.file_analyzed = False  # keeps track of if audio file has been analyzed yet

        # Title
        tk.Label(root, text="SPIDAM Audio Analysis Tool", font=("Arial", 20, "bold")).pack(anchor=tk.CENTER, pady=10)

        # File import status text
        self.file_label = tk.Label(root, text="No file selected", fg="gray", font=("Arial", 12))
        self.file_label.pack(anchor=tk.CENTER, pady=5)

        # Frame to hold buttons horizontally
        self.buttons_frame = tk.Frame(root)
        self.buttons_frame.pack(anchor=tk.CENTER, pady=10)

        # File import selection
        self.import_button = tk.Button(self.buttons_frame, text="Import Audio File", command=self.load_file, font=("Arial", 12))
        self.import_button.pack(side=tk.LEFT, padx=10)

        # Cleaning tools selection
        self.clean_button = tk.Button(self.buttons_frame, text="Analyze Audio", command=self.clean_data, font=("Arial", 12), state="disabled")
        self.clean_button.pack(side=tk.LEFT, padx=10)

        # Visualization Title
        tk.Label(root, text="Visualizations", font=("Arial", 16, "bold")).pack(anchor=tk.CENTER, pady = 10)

        # Tabs for data display
        self.tabControl = ttk.Notebook(root)
        self.tab1 = ttk.Frame(self.tabControl)
        self.tab2 = ttk.Frame(self.tabControl)
        self.tab6 = ttk.Frame(self.tabControl)

        self.tabControl.add(self.tab1, text='Waveform')
        self.tabControl.add(self.tab2, text='RT60 Cycle Graphs')
        self.tabControl.add(self.tab6, text='Intensity Graph')

        self.tabControl.pack()

        self.fig, self.ax = plt.subplots(figsize=(9, 4))
        self.ax.set_title("Audio Data Visualization")
        self.ax.set_xlabel("Time: Seconds")
        self.ax.set_ylabel("Amplitude")
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.tab1)
        self.canvas_widget = self.canvas.get_tk_widget()
        self.canvas_widget.grid(row = 1, column = 1)
        self.canvas_widget.pack()

        # Visualization selection: RT60 Cycle graph
        self.fig1, self.ax1 = plt.subplots(figsize=(9, 4))
        self.ax1.set_title("RT60")
        self.ax1.set_xlabel("Time: Seconds")
        self.ax1.set_ylabel("Power: dB")
        self.canvas1 = FigureCanvasTkAgg(self.fig1, master=self.tab2)
        self.canvas_widget1 = self.canvas1.get_tk_widget()
        self.canvas_widget1.grid(row = 0, column = 0, columnspan = 6)

        self.rt60_button = tk.Button(self.tab2, text="Cycle RT60 Graphs", command=self.cycle_rt60, font=("Arial", 10))
        self.rt60_button.grid(row = 1, column = 2, pady = 10)

        # Combined RT60 graph button
        self.rt60_combined_button = tk.Button(self.tab2, text="Combined RT60 Graph", command=self.update_combined_rt60, font=("Arial", 10))
        self.rt60_combined_button.grid(row = 1, column = 3, pady = 10)

        # Visualization selection: Intensity
        self.fig5, self.ax5 = plt.subplots(figsize=(9, 4))
        self.ax5.set_title("Intensity")
        self.ax5.set_xlabel("Time: Seconds")
        self.ax5.set_ylabel("Frequency: Hertz")
        self.canvas5 = FigureCanvasTkAgg(self.fig5, master=self.tab6)
        self.canvas_widget5 = self.canvas5.get_tk_widget()
        self.canvas_widget5.pack()

        # Analysis Results section
        self.results_frame = tk.Frame(root)
        self.results_frame.pack(anchor=tk.CENTER,pady=10)

        self.length_label = tk.Label(self.results_frame, text="Length: --- seconds", font=("Arial", 12))
        self.length_label.grid(row=0, column=0, padx=10)

        self.rt60_label = tk.Label(self.results_frame, text="RT60: --- seconds", font=("Arial", 12))
        self.rt60_label.grid(row=0, column=1, padx=10)

        self.difference_label = tk.Label(self.results_frame, text="RT60 .05 Difference: --- seconds", font=("Arial", 12))
        self.difference_label.grid(row=0, column=2, padx=10)

        self.resonant_label = tk.Label(self.results_frame, text="Resonant Frequency: --- Hz", font=("Arial", 12))
        self.resonant_label.grid(row=0, column=3, padx=10)

        # Play/stop button
        self.play_button = tk.Button(root, text="Play", command=self.toggle_play, font=("Arial", 12))
        self.play_button.pack(pady=10)

        # Status bar
        self.status_frame = ttk.Frame(self.root, relief="sunken", padding="2 2 2 2")
        self.status_frame.pack()

        # StringVar for status message which will be shown within status bar
        self.status_msg = tk.StringVar()
        self.update_status("Import audio file to start analyzing.")  # set default status message to be shown when application launches

        # Status label
        self.status = ttk.Label(self.status_frame, textvariable=self.status_msg, anchor="w")
        self.status.pack()

        # Initialize pygame mixer
        pygame.mixer.init()

    # Update status message
    def update_status(self, message):
        """
        Updates the status message.
        """
        
        # Update status instance variable to input
        self.status_msg.set(message)
    
    # Load file
    def load_file(self):
        """
        Handles the file import process. Calls the controller to load the file and updates the view.
        """

        filepath = filedialog.askopenfilename(filetypes=[("Audio Files", "*.wav *.mp3 *.m4a"), ("All Files", "*.*")])

        if filepath:

            try:  # attempt to do

                # Set boolean check for file importing to false (if not already; in case new audio file is being imported)
                self.file_imported = False
                
                # Update status message
                self.update_status("Awaiting file selection...")
                
                # Load file after selection
                self.controller.load_file(filepath)

                # Store name of file
                self.file_name = filepath.split('/')[-1]

                # Display name of file in file label
                self.file_label.config(text=f"File: {filepath.split('/')[-1]}", fg="black")

                # Set boolean check for file importing to true
                self.file_imported = True

                # Update status message displaying file has been loaded
                self.update_status(f"File \"{self.file_name}\" loaded sucessfully.")

                # Enable analyze audio and play buttons
                self.clean_button.config(state="normal")
                self.play_button.config(state="normal")
            
            except FileNotFoundError as error:  # except if the file is not found (a FileNotFound error exception arises)

                # Display error message in status bar
                self.update_status(f"Error: {str(error)}")

    # Toggle play
    def toggle_play(self):
        """
        Calls the controller to play or stop the audio.
        """

        # Control audio playback depending on state of play button
        if self.play_button['text'] == 'Play':  # if play button is currently in Play mode

            # Start audio playback
            self.controller.play_audio()

            # Change text on button to "Stop"
            self.play_button.config(text="Stop")

        else:  # if play button is not currently in Play mode
            
            # Stop audio playback
            self.controller.stop_audio()

            # Change text on button back to "Play"
            self.play_button.config(text="Play")
    
    # Clean data
    def clean_data(self):
        """
        Handles data cleaning via the controller.
        """

        try:  # attempt to do
            
            # Set boolean check for analyzing audio to false (if not already; in case new audio is imported)
            self.file_analyzed = False
            
            # Update status message to indicate audio is being analyzed
            self.update_status("Analyzing audio file...")
            
            # Analyze audio and update results
            self.controller.clean_data()
            self.results = self.controller.analyze_data()
            self.update_results(self.results)
            self.update_visualization(self.results["waveform"])
            self.cycle_rt60()
            self.update_combined_rt60()

            # Set boolean check for analyzing audio to true
            self.file_analyzed = True

            # Update status message to indicate audio has been successfully analyzed
            self.update_status(f"File \"{self.file_name}\" successfully analyzed.")

        except Exception as error:  # except if an exception arises

            self.update_status(f"Error: {error}")

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

    def audio_status(self):

        # Update status message indicating that graph cannot yet be generated since audio has not been imported
        if((self.file_imported is False)):  # if file has not yet been imported

            # Update status message indicating that audio has not yet been imported
            self.update_status("Audio not yet imported, graph cannot be generated.")

        if((self.file_imported is True) and (self.file_analyzed is False)):  # if file has been imported, but not analyzed

            # Update status message indicating that imported audio has not yet been analyzed
            self.update_status("Imported audio not yet analyzed, graph cannot be generated.")

    # Plot combined RT60 graphs
    def update_combined_rt60(self):
        """
        This function updates the combined RT60 graph.
        """
        self.ax1.clear()

        # Update plot title and axis titles
        self.ax1.set_title("RT60 Combined")
        self.ax1.set_xlabel("Time: Seconds")
        self.ax1.set_ylabel("Power: dB")

        # Separate RT60 results into low, mid, and high; and then plot those results
        try:  # atttempt to do
            
            rt60_low = self.results["rt60_low"]
            rt60_mid = self.results["rt60_mid"]
            rt60_high = self.results["rt60_high"]

            # RT60 low
            self.ax1.plot(rt60_low[0], rt60_low[1], linewidth=1, alpha=0.7)
            self.ax1.plot(rt60_low[2], rt60_low[5], 'ro')
            self.ax1.plot(rt60_low[3], rt60_low[6], 'yo')
            self.ax1.plot(rt60_low[4], rt60_low[7], 'go')

            # RT60 mid
            self.ax1.plot(rt60_mid[0], rt60_mid[1], linewidth=1, alpha=0.7)
            self.ax1.plot(rt60_mid[2], rt60_mid[5], 'ro')
            self.ax1.plot(rt60_mid[3], rt60_mid[6], 'yo')
            self.ax1.plot(rt60_mid[4], rt60_mid[7], 'go')

            # RT60 high
            self.ax1.plot(rt60_high[0], rt60_high[1], linewidth=1, alpha=0.7)
            self.ax1.plot(rt60_high[2], rt60_high[5], 'ro')
            self.ax1.plot(rt60_high[3], rt60_high[6], 'yo')
            self.ax1.plot(rt60_high[4], rt60_high[7], 'go')

        except AttributeError:  # except if an AttributeError exception arises (most notably because the audio has not yet been loaded for RT60 results to exist)

            # Print status message to status bar depending on current state of audio importing/analyzing
            self.audio_status()

        # Draw the plot with these results
        self.canvas1.draw()

    # Cycle through low, mid, and high RT60 graphs
    def cycle_rt60(self):
        """
        This function iterates through the 3 rt60 graphs LOW, MID, HIgh
        """
        try:
            
            # Clear current plot
            self.ax1.clear()

            # Update plot title and axis titles
            self.ax1.set_title("RT60")
            self.ax1.set_xlabel("Time: Seconds")
            self.ax1.set_ylabel("Power: dB")

            # Determine which rt60 plot to show
            if self.index%3 == 1:
                self.ax1.set_title("RT60 Low")
                rt60_data = self.results["rt60_low"]
            elif self.index%3 == 2:
                self.ax1.set_title("RT60 Mid")
                rt60_data = self.results["rt60_mid"]
            elif self.index%3 == 0:
                self.ax1.set_title("RT60 High")
                rt60_data = self.results["rt60_high"]

            #update the graph with the corresponding data
            if rt60_data:
                self.ax1.plot(rt60_data[0], rt60_data[1], linewidth=1, alpha=0.7, color='#004bc6')
                self.ax1.plot(rt60_data[2], rt60_data[5], 'ro')  # Plot points for RT60 data
                self.ax1.plot(rt60_data[3], rt60_data[6], 'go')
                self.ax1.plot(rt60_data[4], rt60_data[7], 'yo')

            self.canvas1.draw()

            #Update the index by one and keep it in the 1, 2, 3 scheme
            self.index += 1
            self.index = self.index%3

        except:
            
            # Print status message to status bar depending on current state of audio importing/analyzing
            self.audio_status()

    def update_intensity(self):
        """
        Updates the intensity graphs.
        """
        self.ax5.clear()
        self.ax5.set_title("Intensity")
        self.ax5.set_xlabel("Time: Seconds")
        self.ax5.set_ylabel("Frequency: Hz")
        sample_rate, data = wavfile.read(self.results)
        spectrum, freqs, t, im = plt.specgram(data, Fs=sample_rate, NFFT=1024, cmap=plt.get_cmap('autumn_r'))
        self.canvas5.draw()