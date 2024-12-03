Overview
-
This Python-based application provides an interactive platform for analyzing and modeling acoustic data with a focus on improving audio intelligibility in enclosed spaces. The application calculates reverberation time (RT60) for audio samples, visualizes frequency-specific analysis, and offers tools for evaluating acoustic environments and their effects. Built with [Python](https://docs.python.org/3) and [Tkinter](https://docs.python.org/3/library/tkinter.html), the application features a user-friendly graphical interface for seamless interaction.

Key Features
-
+ Audio File Management
  + Load WAV and MP3 files via a Tkinter file dialog.
  + Automatic conversion of MP3 formats to WAV.
  + Handles multi-channel audio, converting it to single-channel as needed.
+ RT60 Analysis
  + Calculates RT60 values for low, mid, and high frequencies.
  + Identifies the frequency range with the longest reverberation time.
+ Data Visualization
  + Displays waveforms and RT60 data using Matplotlib.
  + Interactive plots for frequency-specific analysis.
+ Audio Playback
  + Built-in audio player to listen to the loaded sample.

Installation
-
Prerequisites:
+ Python 3.8+
+ [pip](https://pip.pypa.io/en/stable) for dependency management.

Steps:

1. Clone the repository:
   + ```git clone https://github.com/Python-Acoustic-Modeling-Project/main-repo.git```
2. Navigate to the project directory:
   + ```cd main-repo```
3. Install dependencies:
   + ```pip install -r requirements.txt```

Usage
-
1. Launch the application
   + ```python3 main.py```
2. Use the GUI to:
   + Load audio files.
   + Analyze and visualize RT60 data.
   + Play audio files.

Limitations
-
+ Limited to environments where Python and its dependencies are properly installed.
+ GUI performance may vary with large audio files due to the Tkinter framework's simplicity.
+ Designed for evaluating single audio samples at a time.
+ Only WAV and MP3 audio files are supported.

Contributors
-
+ Brayden Kondek
+ Pjark Sander
+ Ashlyn Ryan
+ Timothy Diehl

Screenshots
-
### Upon Opening Program
  <img src="https://assets.bradykondek.com/files/spidam-project/upon-open.png" width="450" height="450">

### Waveform Analysis
  <img src="https://assets.bradykondek.com/files/spidam-project/waveform-analysis.png" width="450" height="450">

### Combined RT60 Graph
  <img src="https://assets.bradykondek.com/files/spidam-project/combined-rt60.png" width="450" height="450">

### Intensity Graph
  <img src="https://assets.bradykondek.com/files/spidam-project/intensity-graph.png" width="450" height="450">