import tkinter as tk
from tkinter import filedialog
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import os

'''def select_path(entry_field):
    path = filedialog.askopenfilename()
    entry_field.delete(0, tk.END)
    entry_field.insert(0, path)
    filename = find_filename(path)
    label_name.config(text=("   File: " + filename))'''

'''def get_path():
    return path'''

'''def find_filename(path):
    return os.path.basename(path).split('/')[-1]'''

'''def change_graph():
    graph_disp = graph_select_var.get()
    if graph_disp == "Intensity Graph":
        pass
    elif graph_disp == "Waveform Graph":
        pass
    elif graph_disp == "RT60 Low":
        pass
    elif graph_disp == "RT60 Medium":
        pass
    elif graph_disp == "RT60 High":
        pass
'''


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
        self.graph_types = ["Intensity Graph", "Waveform Graph", "RT60 Low", "RT60 Medium", "RT60 High", "RT60 Combined"]

        #Labels
        self.label = tk.Label(self.root, text="   File entry:")
        self.label.grid(column=0, row=1)

        #
        self.path = tk.Entry(self.root, width=50)
        self.path.grid(column=1, row=1, columnspan=3)

        #
        self.file_button = tk.Button(self.root, text="Choose a file", command=lambda: select_path())
        self.file_button.grid(column=4, row=1)

        self.label_name = tk.Label(self.root, text=("   File: " + self.filename))
        self.label_name.grid(column=0, row=2, columnspan=4, sticky=('W'))

        self.graph_select_var = tk.StringVar(value=self.graph_types[0])
        self.graph_select = tk.OptionMenu(self.root, self.graph_select_var, *self.graph_types, command=self.change_graph())
        self.graph_select.grid(column=1, row=3, columnspan=4, sticky=('W'), pady = 10)

        self.fig,self.ax = plt.subplots()
        self.canvas = FigureCanvasTkAgg(self.fig,self.root)
        self.canvas.draw()
        self.widget = self.canvas.get_tk_widget()
        self.widget.grid(column=1, row=4, columnspan=4, sticky=('W'))

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

    def select_path(self):
        self.location = filedialog.askopenfilename()
        self.path.delete(0, tk.END)
        self.path.insert(0, self.location )
        self.filename = self.find_filename()
        self.label_name.config(text=("   File: " + self.filename))

    def get_path(self):
        return self.path

    def find_filename(self):
        return os.path.basename(self.location ).split('/')[-1]

    def change_graph(self):
        graph_disp = self.graph_select_var.get()
        if graph_disp == "Intensity Graph":
            pass
        elif graph_disp == "Waveform Graph":
            pass
        elif graph_disp == "RT60 Low":
            pass
        elif graph_disp == "RT60 Medium":
            pass
        elif graph_disp == "RT60 High":
            pass

hello = view()



