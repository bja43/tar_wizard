# import sys
# import os

import tkinter as tk
from tkinter import ttk
from tkinter import filedialog

# import numpy as np
import pandas as pd

# import plotly
# import seaborn as sns
# import matplotlib.pyplot as plt

# import jpype as jp
# import jpype.imports

# jp.startJVM(classpath=["Tetrad-gui-current-launch.jar"])

# import edu.cmu.tetrad.search as ts
# import edu.cmu.tetrad.data as td


def open_file():
    fpath = filedialog.askopenfilename()
    df = pd.read_csv(fpath)
    print(df)
    # text.insert(tk.INSERT, df)
    # sns.pairplot(df)
    # plt.show()


root = tk.Tk()
root.geometry("420x420")
root.title("tar wizard 0.0.1")

notebook = ttk.Notebook(root)
tabs = [tk.Frame(notebook) for _ in range(3)]
for i, tab in enumerate(tabs):
    notebook.add(tab, text=f"Tab {i}")
notebook.pack(expand=True, fill="both")

# text = tk.Text(root)
# text.pack()

menu_bar = tk.Menu(root)
root.config(menu=menu_bar)

file_menu = tk.Menu(menu_bar)
menu_bar.add_cascade(label="File", menu=file_menu)
file_menu.add_command(label="Open", command=open_file)
file_menu.add_command(label="Save")
file_menu.add_separator()
file_menu.add_command(label="Exit", command=quit)

edit_menu = tk.Menu(menu_bar)
menu_bar.add_cascade(label="Edit", menu=edit_menu)
edit_menu.add_command(label="Cut")
edit_menu.add_command(label="Copy")
edit_menu.add_command(label="Paste")



# button = tk.Button(text="open", command=open_file)
# button.pack()

root.mainloop()
