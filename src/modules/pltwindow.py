
import tkinter as tk

from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg, NavigationToolbar2Tk)
# Implement the default Matplotlib key bindings.
from matplotlib.backend_bases import key_press_handler
from matplotlib.figure import Figure

import numpy as np


class pltwindow:

    def _quit(self):
        # self.win.quit()     # stops mainloop
        self.win.destroy()  # this is necessary on Windows to prevent
                            # Fatal Python Error: PyEval_RestoreThread: NULL tstate
        self.win.update()

    def __init__(self, icon=None):
        self.initiated = None
        self.canvas_frame = None
        self.win = None
        self.icon = icon

    def initTk(self, fig, title:str=None):
        self.initiated = True

        if self.win is None:
            self.win = tk.Toplevel()
            self.win.bind('<Escape>', lambda e: self._quit())
            if self.icon is not None:
                self.win.tk.call('wm', 'iconphoto', self.win._w, self.icon)

        # if the frame exists, detroy it
        if self.canvas_frame is not None:
            self.canvas_frame.destroy()
            # for item in self.canvas.get_tk_widget().find_all():
            #     self.canvas.get_tk_widget().delete(item)

        if title is not None:
            self.win.wm_title(title)

        self.canvas_frame = tk.Frame(self.win, borderwidth=0)
        self.canvas_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=1)
        canvas = FigureCanvasTkAgg(fig, master=self.canvas_frame)  # A tk.DrawingArea.
        canvas.draw()
        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

