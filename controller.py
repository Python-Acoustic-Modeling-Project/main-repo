# Include libraries
import os
import pygame

# Controller class
class Controller:

    # Class initialization
    def __init__(self, model):
        """
        Initialize the controller, linking the model and the view.
        """

        # Set instance variables
        self.model = model
        self.view = None
        self.is_playing = False

        # Initialize pygame mixer for audio playback
        pygame.mixer.init()

    # Set view
    def set_view(self, view):

        # Set view instance variable
        self.view = view
    
    # Load file
    def load_file(self, filepath):
        """
        Handles file loading via the model.
        """

        # Handle if a filepath does not exist
        if not os.path.exists(filepath):

            # Raise FileNotFound exception
            raise FileNotFoundError("The selected file does not exist.")
        
        # Otherwise, load the file via the filepath
        self.model.load_audio(filepath)
    
    # Clean data
    def clean_data(self):
        """
        Handles data cleaning via the model.
        Converts non-WAV files to WAV format and processes metadata.
        """

        # Convert audio file to WAV if not already in that format
        if self.model.file_format != "WAV":
            
            # Convert file to WAV
            new_file = self.model.convert_to_wave(self.model.filepath)

            # Load newly-converted WAV audio file
            self.model.load_audio(new_file)

    # Analyze data
    def analyze_data(self):
        """
        Performs audio analysis using the model and returns the results.
        """

        # Ensure audio data is loaded
        if self.model.data is None:

            # Raise ValueError exception
            raise ValueError("No audio data loaded. Please load an audio file first.")
        
        # Perform analysis and assign results within dictionary
        results = {
            "length": len(self.model.data) / self.model.samplerate,
            "resonant_frequency": self.model.calculate_resonant_frequency(),
            "waveform": self.model.data,
            "rt60_low": self.model.rt60_visualization(250),
            "rt60_mid": self.model.rt60_visualization(1000),
            "rt60_high": self.model.rt60_visualization(5000),
            "rt60": self.model.calculate_rt60(),
            "Intensity": (self.model.data, self.model.samplerate),
        }

        # Return results
        return results
    
    # Play audio
    def play_audio(self):
        """
        Play the audio through pygame.
        """

        # If audio is not playing, play audio
        if not self.is_playing:  # if audio is not playing

            # Load audio file into mixer
            pygame.mixer.music.load(self.model.filepath)

            # Start audio playback
            pygame.mixer.music.play()

            # Change boolean variable state to True
            self.is_playing = True

    # Stop audio
    def stop_audio(self):
        """
        Stop the audio if it is playing.
        """

        # If audio is playing, stop audio
        if self.is_playing:  # if audio is playing
            
            # Stop audio playback
            pygame.mixer.music.stop()

            # Change boolean variable state to False
            self.is_playing = False