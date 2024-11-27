import tkinter as tk
from tkinter import filedialog
import os

def select_path(entry_field):
    path = filedialog.askopenfilename()
    entry_field.delete(0, tk.END)
    entry_field.insert(0, os.path.basename(path).split('/')[-1])

root = tk.Tk()
root.title("SPIDAM")
root.grid()

root.geometry("800x500")

label = tk.Label(root, text="")
label.grid(column=0, row=0)

label = tk.Label(root, text="   File entry:")
label.grid(column=0, row=1)

path = tk.Entry(root, width=50)
path.grid(column=1, row=1, columnspan=3)

file_button = tk.Button(root, text="Choose a file", command=lambda: select_path(path))
file_button.grid(column=4, row=1)


root.mainloop()


