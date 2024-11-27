import tkinter as tk
from tkinter import filedialog
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import os

rt60 = 0.0
filelength = 0.0
rt_difference = 0.0
resonant_frequency = 0.0
filename = ""
graph_types = ["Intensity Graph", "Waveform Graph", "RT60 Low", "RT60 Medium", "RT60 High", "RT60 Combined"]

def select_path(entry_field):
    path = filedialog.askopenfilename()
    entry_field.delete(0, tk.END)
    entry_field.insert(0, path)
    filename = find_filename(path)
    label_name.config(text=("   File: " + filename))

def get_path():
    return path

def find_filename(path):
    return os.path.basename(path).split('/')[-1]

def change_graph():
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

root = tk.Tk()
root.title("SPIDAM")
root.grid()

root.geometry("800x800")

label = tk.Label(root, text="")
label.grid(column=0, row=0)

label = tk.Label(root, text="   File entry:")
label.grid(column=0, row=1)

path = tk.Entry(root, width=50)
path.grid(column=1, row=1, columnspan=3)

file_button = tk.Button(root, text="Choose a file", command=lambda: select_path(path))
file_button.grid(column=4, row=1)

label_name = tk.Label(root, text=("   File: " + filename))
label_name.grid(column=0, row=2, columnspan=4, sticky=('W'))

graph_select_var = tk.StringVar(value=graph_types[0])
graph_select = tk.OptionMenu(root, graph_select_var, *graph_types, command=change_graph)
graph_select.grid(column=1, row=3, columnspan=4, sticky=('W'), pady = 10)

fig,ax = plt.subplots()
canvas = FigureCanvasTkAgg(fig,root)
canvas.draw()
widget = canvas.get_tk_widget()
widget.grid(column=1, row=4, columnspan=4, sticky=('W'))

label_file_length = tk.Label(root, text=("File Length: " + str(filelength) + "s"))
label_file_length.grid(column=1, row=5, columnspan=4, sticky=('W'))

label_file_Resonant_Frequency = tk.Label(root, text=("Resonant Frequency: " + str(resonant_frequency) + "Hz"))
label_file_Resonant_Frequency.grid(column=1, row=6, columnspan=4, sticky=('W'))

label_file_rt60_diff = tk.Label(root, text=("RT60 Difference: " + str(rt_difference) + "s"))
label_file_rt60_diff.grid(column=1, row=7, columnspan=4, sticky=('W'))

root.mainloop()

