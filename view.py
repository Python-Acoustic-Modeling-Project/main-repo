import tkinter as tk
from tkinter import filedialog
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
import os

from matplotlib.pyplot import title


class view:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("SPIDAM")
        self.root.grid()
        self.root.geometry("800x800")

        #initialize data variables
        self.rt60 = 0.0
        self.filelength = 0.0
        self.rt_difference = 0.0
        self.resonant_frequency = 0.0
        self.filename = ""
        self.location = ""
        self.graph_types = ["None","Intensity Graph", "Waveform Graph", "RT60 Low", "RT60 Medium", "RT60 High", "RT60 Combined"]

        #Label show file entry
        self.label = tk.Label(self.root, text="   File entry:")
        self.label.grid(column=0, row=1)

        #Label that displays the file path
        self.path = tk.Label(self.root, width=50)
        self.path.grid(column=1, row=1, columnspan=3)

        #Label: message to choose a file
        self.file_button = tk.Button(self.root, text="Choose a file", command=self.select_path)
        self.file_button.grid(column=4, row=1)

        #Label filename
        self.label_name = tk.Label(self.root, text=("   Filename: " + self.filename))
        self.label_name.grid(column=0, row=2, columnspan=4, sticky='W')

        # Creating the framework for the plots
        self.fig, self.ax = plt.subplots()
        self.canvas = FigureCanvasTkAgg(self.fig, self.root)
        self.widget = self.canvas.get_tk_widget()
        self.widget.grid(column=1, row=4, columnspan=4, sticky='W')
        self.change_graph("None")

        #dropdown to change the plot
        self.graph_select_var = tk.StringVar(value=self.graph_types[0])
        self.graph_select = tk.OptionMenu(self.root, self.graph_select_var, *self.graph_types, command=self.change_graph)
        self.graph_select.grid(column=1, row=3, columnspan=4, sticky='W', pady = 10)

        #Label to display file length
        self.label_file_length = tk.Label(self.root, text=("File Length: " + str(self.filelength) + "s"))
        self.label_file_length.grid(column=1, row=5, columnspan=4, sticky=('W'))

        #Label to display resonant frequency
        self.label_file_Resonant_Frequency = tk.Label(self.root, text=("Resonant Frequency: " + str(self.resonant_frequency) + "Hz"))
        self.label_file_Resonant_Frequency.grid(column=1, row=6, columnspan=4, sticky=('W'))

        #Label to display RT60 Difference
        self.label_file_rt60_diff = tk.Label(self.root, text=("RT60 Difference: " + str(self.rt_difference) + "s"))
        self.label_file_rt60_diff.grid(column=1, row=7, columnspan=4, sticky='W')
        self.root.mainloop()

    #Function to select a path on button push
    def select_path(self):
        self.location = filedialog.askopenfilename()
        self.path.config(text=self.location)
        self.filename = self.find_filename()
        self.label_name.config(text=("   Filename: " + self.filename))
        self.get_path()

    def get_path(self):
        return self.location

    def find_filename(self):
        return os.path.basename(self.location ).split('/')[-1]

    def change_graph(self, option):
        self.ax.clear()
        if option == "None":
            self.ax.plot()
            plt.title("No Data")

        elif option == "Intensity Graph":

            x = np.arange(0, np.pi * 2, 0.01)
            y = np.sin(x * 1)

            plt.plot(x, y)
            plt.title("Sine Wave!!")

        elif option == "Waveform Graph":
            x = np.arange(0, np.pi * 2, 0.01)
            y = np.sin(x * 2)

            plt.plot(x, y)
            plt.title("Sine Wave!!")
        elif option == "RT60 Low":
            x = np.arange(0, np.pi * 2, 0.01)
            y = np.sin(x * 3)

            plt.plot(x, y)
            plt.title("Sine Wave!!")
        elif option == "RT60 Medium":
            x = np.arange(0, np.pi * 2, 0.01)
            y = np.sin(x * 4)

            plt.plot(x, y)
            plt.title("Sine Wave!!")
        elif option == "RT60 High":
            x = np.arange(0, np.pi * 2, 0.01)
            y = np.sin(x * 5)

            plt.plot(x, y)
            plt.title("Sine Wave!!")
        self.canvas.draw()

test = view()



