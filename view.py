# Include libraries
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import pygame

# View class
class View:

    # Class initialization
    def __init__(self, controller):
        """
        Initialize the GUI view for the audio analysis application.
        """

        # Set instance variables
        self.root = tk.Tk()  # create Tkinter instance
        self.root.minsize(800, 800)  # represents the size of the application window
        self.root.title("SPIDAM Audio Analysis Tool")  # set application title
        self.controller = controller  # assign controller to instance variable
        self.is_playing = False  # boolean variable to represent if audio is currently playing
        self.index = 0  # integer variable to represent the current index for the RT60 cycle graphs
        self.file_imported = False  # keeps track of if audio file has been imported yet
        self.file_analyzed = False  # keeps track of if audio file has been analyzed yet

        # Title heading at the top of application window
        tk.Label(self.root, text="SPIDAM Audio Analysis Tool", font=("Arial", 20, "bold")).pack(anchor=tk.CENTER, pady=10)

        # File import status text
        self.file_label = tk.Label(self.root, text="No file selected", fg="gray", font=("Arial", 12))
        self.file_label.pack(anchor=tk.CENTER, pady=5)

        # Frame to hold buttons horizontally
        self.buttons_frame = tk.Frame(self.root)
        self.buttons_frame.pack(anchor=tk.CENTER, pady=10)

        # File import selection
        self.import_button = tk.Button(self.buttons_frame, text="Import Audio File", command=self.load_file, font=("Arial", 12))
        self.import_button.pack(side=tk.LEFT, padx=10)

        # Cleaning tools selection
        self.clean_button = tk.Button(self.buttons_frame, text="Analyze Audio", command=self.clean_data, font=("Arial", 12), state="disabled")
        self.clean_button.pack(side=tk.LEFT, padx=10)

        # Visualization Title
        tk.Label(self.root, text="Visualizations", font=("Arial", 16, "bold")).pack(anchor=tk.CENTER, pady = 10)

        # Tabs for data display
        self.tabControl = ttk.Notebook(self.root)  # sets up "container" for tabs, and the content within each one
        self.tab1 = ttk.Frame(self.tabControl)  # set up tab 1, for waveform visualization graph
        self.tab2 = ttk.Frame(self.tabControl)  # set up tab 2, for RT60 graphs
        self.tab3 = ttk.Frame(self.tabControl)  # set up tab 3, for intensity graph

        # Add titles to tabs
        self.tabControl.add(self.tab1, text='Waveform')  # add title to tab 1
        self.tabControl.add(self.tab2, text='RT60 Cycle Graphs')  # add title to tab 2
        self.tabControl.add(self.tab3, text='Intensity Graph')  # add title to tab 3
        
        # Place in tab figure
        self.tabControl.pack()

        # Visualization selection: Waveform graph (tab 1)
        self.fig, self.ax = plt.subplots(figsize=(9, 4))  # establish plot, and set size
        self.ax.set_title("Audio Data Visualization")  # set plot title
        self.ax.set_xlabel("Time: Seconds")  # set x-axis label
        self.ax.set_ylabel("Amplitude")  # set y-axis label
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.tab1)  # establish canvas to contain plot
        self.canvas_widget = self.canvas.get_tk_widget()
        self.canvas_widget.grid(row = 1, column = 1)
        self.canvas_widget.pack()

        # Visualization selection: RT60 Cycle graph (tab 2)
        self.fig1, self.ax1 = plt.subplots(figsize=(9, 4))  # establish plot, and set size
        self.ax1.set_title("RT60")  # set plot title
        self.ax1.set_xlabel("Time: Seconds")  # set x-axis title
        self.ax1.set_ylabel("Power: dB")  # set y-axis title
        self.canvas1 = FigureCanvasTkAgg(self.fig1, master=self.tab2)  # establish canvas to contain plot
        self.canvas_widget1 = self.canvas1.get_tk_widget()
        self.canvas_widget1.grid(row = 0, column = 0, columnspan = 6)

        # Cycle RT60 graphs button (within tab 2)
        self.rt60_button = tk.Button(self.tab2, text="Cycle RT60 Graphs", command=self.cycle_rt60, font=("Arial", 10))  # calls cycle_rt60() function when clicked on
        self.rt60_button.grid(row = 1, column = 2, pady = 10)

        # Combined RT60 graph button (within tab 2)
        self.rt60_combined_button = tk.Button(self.tab2, text="Combined RT60 Graph", command=self.update_combined_rt60, font=("Arial", 10))  # calls update_combined_rt60() function when clicked on
        self.rt60_combined_button.grid(row = 1, column = 3, pady = 10)

        # Visualization selection: Intensity (tab 3)
        self.fig5, self.ax5 = plt.subplots(figsize=(9, 4))  # establish plot, and set size
        self.ax5.set_title("Intensity")  # set plot title
        self.ax5.set_xlabel("Time: Seconds")  # set x-axis title
        self.ax5.set_ylabel("Frequency: Hertz")  # set y-axis title
        self.canvas5 = FigureCanvasTkAgg(self.fig5, master=self.tab3)  # establish canvas to contain plot
        self.canvas_widget5 = self.canvas5.get_tk_widget()
        self.canvas_widget5.pack()

        # Analysis Results section
        self.results_frame = tk.Frame(self.root)  # establish frame to contain result labels (that has each result)
        self.results_frame.pack(anchor=tk.CENTER,pady=10)

        # Audio length label
        self.length_label = tk.Label(self.results_frame, text="Length: --- seconds", font=("Arial", 12))
        self.length_label.grid(row=0, column=0, padx=10)

        # RT60 label
        self.rt60_label = tk.Label(self.results_frame, text="RT60: --- seconds", font=("Arial", 12))
        self.rt60_label.grid(row=0, column=1, padx=10)

        # RT60 0.5 difference label
        self.difference_label = tk.Label(self.results_frame, text="RT60 .05 Difference: --- seconds", font=("Arial", 12))
        self.difference_label.grid(row=0, column=2, padx=10)

        # Resonant frequency label
        self.resonant_label = tk.Label(self.results_frame, text="Resonant Frequency: --- Hz", font=("Arial", 12))
        self.resonant_label.grid(row=0, column=3, padx=10)

        # Play/stop button
        self.play_button = tk.Button(self.root, text="Play", command=self.toggle_play, font=("Arial", 12))  # calls toggle_play() function when clicked on
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

        # Run application
        self.root.mainloop()

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

        # Trigger file selection window for user to select audio file
        filepath = filedialog.askopenfilename(filetypes=[("Audio Files", "*.wav *.mp3"), ("All Files", "*.*")])

        # If user selects file, load in the file, convert if needed, and analyze it
        if filepath:  # if filepath exists, meaning user selected proper file

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

        # Analyze audio file, get results, and plot them to respective graphs
        try:  # attempt to do
            
            # Set boolean check for analyzing audio to false (if not already; in case new audio is imported)
            self.file_analyzed = False
            
            # Update status message to indicate audio is being analyzed
            self.update_status("Analyzing audio file...")
            
            # Analyze audio and update results
            self.controller.clean_data()  # clean data
            self.results = self.controller.analyze_data()  # analyze data and assign results to instance variable
            self.update_results(self.results)  # update the results from instance variable

            # Prepare/update graphs
            self.update_visualization(self.results["waveform"])  # update waveform visualization graph
            self.cycle_rt60()  # update RT60 cycle graphs (low, mid, and high)
            self.update_combined_rt60()  # update RT60 combined graph
            self.update_intensity()  # update intensity graph

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

        # Label to display length of audio file
        self.length_label.config(text=f"Length: {results['length']:.2f} seconds")

        # Label to display RT60
        self.rt60_label.config(text=f"RT60: {results['rt60']:.2f} seconds")

        # Label to display RT60 .5 difference
        self.difference_label.config(text=f"RT60 .5 Difference: {results['rt60'] - 0.5:.2f} seconds")

        # Label to display resonant frequency
        self.resonant_label.config(text=f"Resonant Frequency: {results['resonant_frequency']:.2f} Hz")

    # Update visualization
    def update_visualization(self, waveform):
        """
        Updates the waveform visualization.
        """

        # Clear current plot
        self.ax.clear()

        # Plot waveform
        self.ax.plot(waveform, label="Waveform")

        # Add legend to plot
        self.ax.legend()

        # Set plot and axis titles
        self.ax.set_title("Audio Waveform")
        self.ax.set_xlabel("Time: Seconds")
        self.ax.set_ylabel("Amplitude")

        # Create display canvas for plot
        self.canvas.draw()
    
    # Check on current audio status, and display respective state in status bar
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
        
        # Clear current plot
        self.ax1.clear()

        # Update plot title and axis titles
        self.ax1.set_title("RT60 Combined")
        self.ax1.set_xlabel("Time: Seconds")
        self.ax1.set_ylabel("Power: dB")

        # Separate RT60 results into low, mid, and high; and then plot those results
        try:  # atttempt to do
            
            # Separate RT60 results into low, mid, and high
            rt60_low = self.results["rt60_low"]  # RT60 low
            rt60_mid = self.results["rt60_mid"]  # RT60 mid
            rt60_high = self.results["rt60_high"]  # RT60 high

            # Plot RT60 low
            self.ax1.plot(rt60_low[0], rt60_low[1], linewidth=1, alpha=0.7)
            self.ax1.plot(rt60_low[2], rt60_low[5], 'ro')
            self.ax1.plot(rt60_low[3], rt60_low[6], 'yo')
            self.ax1.plot(rt60_low[4], rt60_low[7], 'go')

            # Plot RT60 mid
            self.ax1.plot(rt60_mid[0], rt60_mid[1], linewidth=1, alpha=0.7)
            self.ax1.plot(rt60_mid[2], rt60_mid[5], 'ro')
            self.ax1.plot(rt60_mid[3], rt60_mid[6], 'yo')
            self.ax1.plot(rt60_mid[4], rt60_mid[7], 'go')

            # Plot RT60 high
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

            # Determine which rt60 plot to show (depending on current cycle index; index changes each time Cycle RT60 Graphs button is clicked)
            if self.index%3 == 1:  # if current cycle index is at 1
                
                # Plot RT60 low results
                self.ax1.set_title("RT60 Low")  # set graph title
                rt60_data = self.results["rt60_low"]  # update graph with RT60 low data

            elif self.index%3 == 2:  # if current cycle index is at 2

                # Plot RT60 mid results
                self.ax1.set_title("RT60 Mid")  # set graph title
                rt60_data = self.results["rt60_mid"]  # update graph with RT60 mid data

            elif self.index%3 == 0:  # if current cycle index is at 0

                # Plot RT60 high results
                self.ax1.set_title("RT60 High")  # set graph title
                rt60_data = self.results["rt60_high"]  # update graph with RT60 high data

            # Update the graph with the corresponding data
            if rt60_data:  # if RT60 data exists

                # Plot RT60 data
                self.ax1.plot(rt60_data[0], rt60_data[1], linewidth=1, alpha=0.7, color='#004bc6')
                self.ax1.plot(rt60_data[2], rt60_data[5], 'ro')  # Plot points for RT60 data
                self.ax1.plot(rt60_data[3], rt60_data[6], 'go')
                self.ax1.plot(rt60_data[4], rt60_data[7], 'yo')

            # Draw the plot
            self.canvas1.draw()

            # Update the index by one and keep it in the 1, 2, 3 scheme
            self.index += 1
            self.index = self.index%3

        except Exception:  # except if an exception arises
            
            # Print status message to status bar depending on current state of audio importing/analyzing
            self.audio_status()

    # Update intensity graph
    def update_intensity(self):
        """
        Updates the intensity graphs.
        """
        
        # Clear current graph
        self.ax5.clear()

        # Set plot and axis titles
        self.ax5.set_title("Intensity")
        self.ax5.set_xlabel("Time: Seconds")
        self.ax5.set_ylabel("Frequency: Hz")

        # Plot results
        plt.specgram(self.results["Intensity"][0], Fs=self.results["Intensity"][1], NFFT=1024, cmap=plt.get_cmap('autumn_r'))

        # Draw the plot
        self.canvas5.draw()