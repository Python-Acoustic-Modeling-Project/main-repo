# Include libraries
import os
from model import Model
from view import View
import soundfile as sf
import librosa

# Controller class
class Controller:

    # Class initialization
    def __init__(self, root):
        """
        Initialize the controller, linking the model and the view.
        """

        self.model = Model()
        self.view = View(root, self)

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
            new_file = self.model.convert_to_wave()

            # Load newly-converted WAV audio file
            self.model.load_audio(new_file)

    # Analyze data
    def analyze_data(self):
        """
        Performs audio analysis using the model and returns the results.
        """

        # Ensure audio data is loaded
        if self.model.audio_data is None:

            raise ValueError("No audio data loaded. Please load an audio file first.")
        
        # Perform analysis
        results = {}  # create empty dictionary
        results["length"] = self.model.get_audio_length()
        results["rt60"] = self.model.calaculate_rt60()
        results["resonant_frequeny"] = self.model.get_resonant_frequency()
        results["waveform"] = self.model.audio_data

        # Return results
        return results