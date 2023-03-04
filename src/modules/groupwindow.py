from tkinter import ttk
import tkinter as tk
import pandas as pd
import numpy as np

from typing import List

from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg, NavigationToolbar2Tk)
# Implement the default Matplotlib key bindings.
from matplotlib.backend_bases import key_press_handler
from matplotlib.figure import Figure

from utils.tk_inter import treeview_sort_column

class groupwindow:

    def _quit(self):
        # self.win.quit()     # stops mainloop
        self.win.destroy()  # this is necessary on Windows to prevent
                            # Fatal Python Error: PyEval_RestoreThread: NULL tstate
        self.win.update()

    def __init__(self, app, icon=None):
        self.tree_records = 15
        self.parent = app
        self.initiated = None
        self.tree_frame = None
        self.canvas_frame = None
        self.combined_frame = None
        self.footer_frame = None
        self.dataframe = None
        self.position = None
        self.title = None
        self.win = None
        self.icon = icon

    def update(self, dataframe: pd.DataFrame, fig, title:str=None, position:list=None, headings=True):
        self.initiated = True
        self.headings = headings
        self.setDataFrame(dataframe)
        self.position = position
        self.fig = fig
        self.updateTk(title)

    def setDataFrame(self, dataframe):
        self.dataframe = dataframe

    def updateTk(self,title):
        
        ### init the toplevel tk element
        if self.win is None or not self.win.winfo_exists():
            self.win = tk.Toplevel()
            self.win.bind('<Escape>', lambda e: self._quit())
            if self.icon is not None:
                self.win.tk.call('wm', 'iconphoto', self.win._w, self.icon)
        if title is not None:
            self.title = title
            self.win.wm_title(title)

        # if the frame exists, detroy it
        if self.combined_frame is not None:
            self.combined_frame.destroy()

        # look
        width = 130 * self.dataframe.shape[1]
        height = self.tree_records * 30 + 25
        
        ### scroll bar for dataframes with more than 15 rows
        if self.dataframe.shape[0] > self.tree_records:
            scrollbar_bool=True
            width += 15 # for the scrollbar
            # height = 450 + 25
        else:
            scrollbar_bool=False
            # height = 30 * self.dataframe.shape[0] + 25 # 30 per row + 25 margin

        if self.position is not None:
            self.win.geometry(f'{width + 500}x{height+60}+{self.position[0]}+{self.position[1]}') # (width, height, x, y)
        else:
            self.win.geometry(f'{width + 500}x{height+60}')
        
        if self.tree_frame is not None:
            self.tree_frame.destroy()

        # combined frame
        self.combined_frame = tk.Frame(self.win, borderwidth=0, width=width+500, height=height)
        self.combined_frame.pack(side=tk.TOP, fill=tk.Y, expand=1)

        # tree frame
        self.tree_frame = tk.Frame(self.combined_frame, borderwidth=0)
        self.tree_frame.pack(side=tk.LEFT, fill=tk.Y, expand=1)

        # treeview
        if self.headings:
            self.tree = ttk.Treeview(self.tree_frame, style="mystyle.Treeview", columns=list(self.dataframe.columns), height=self.tree_records, show='headings')
        else:
            self.tree = ttk.Treeview(self.tree_frame, style="mystyle.Treeview", columns=list(self.dataframe.columns), height=self.tree_records, show='tree')

        self.tree.pack(side=tk.LEFT, fill=tk.Y)

        if scrollbar_bool:
            scrollbar = ttk.Scrollbar(self.tree_frame, orient=tk.VERTICAL, command=self.tree.yview)
            self.tree.configure(yscroll=scrollbar.set)
            scrollbar.pack(side=tk.LEFT, fill=tk.Y)

        for colname in (self.dataframe.columns):
            self.tree.column(colname, anchor='center', width=130, stretch=tk.NO)
            if self.headings:
                self.tree.heading(colname, text=colname, anchor='center', command=lambda _col=colname: treeview_sort_column(self.tree, _col, False))

        self.updateTreeRecords()

        ### plt
        self.canvas_frame = tk.Frame(self.combined_frame, borderwidth=0)
        self.canvas_frame.pack(side=tk.LEFT, fill=tk.X, expand=1)
        canvas = FigureCanvasTkAgg(self.fig, master=self.canvas_frame)  # A tk.DrawingArea.
        canvas.draw()
        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)
        
        if self.footer_frame is not None:
            self.footer_frame.destroy()

        ### Footer buttons frame
        self.footer_frame = tk.Frame(self.win)
        self.footer_frame.pack(side=tk.TOP, expand=True)
        tk.Label(self.footer_frame, text="View grouped by: ", font=self.parent.config['fonts']['f10']).pack(side=tk.LEFT)
        self.category_button = tk.Button(self.footer_frame, text='Category', width=12, command=lambda: self.parent.update_groupby_win('Category'), font=self.parent.config['fonts']['f10'], bg=self.parent.config['colors']['green'])
        self.category_button.pack(side=tk.LEFT)
        self.note_button = tk.Button(self.footer_frame, text='Note', width=12, command=lambda: self.parent.update_groupby_win('Note'), font=self.parent.config['fonts']['f10'], bg=self.parent.config['colors']['green'])
        self.note_button.pack(side=tk.LEFT)


    def updateTreeRecords(self, columns: List[str] = []):
        self.tree.delete(*self.tree.get_children()) # delete data for next rendering)

        if columns == []:
            columns = list(self.dataframe.columns)
        
        for row in self.dataframe[columns].to_numpy():
            self.tree.insert("", 0, values=row.tolist())



