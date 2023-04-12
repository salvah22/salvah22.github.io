from tkinter import ttk
import tkinter as tk
import pandas as pd
import numpy as np

from typing import List

from utils.tk_inter import treeview_sort_column

class treewindow:

    def _quit(self):
        # self.win.quit()     # stops mainloop
        self.win.destroy()  # this is necessary on Windows to prevent
                            # Fatal Python Error: PyEval_RestoreThread: NULL tstate
        self.win.update()

    def __init__(self, icon=None):
        self.initiated = None
        self.tree_frame = None
        self.dataframe = None
        self.position = None
        self.title = None
        self.win = None
        self.icon = icon

    def close(self):
        if self.initiated:
            self.win.destroy()

    def update(self, dataframe: pd.DataFrame, title:str=None, position:list=None, headings=True):
        self.initiated = True
        self.headings = headings
        self.setDataFrame(dataframe)
        if self.win is None or not self.win.winfo_exists():
            self.win = tk.Toplevel()
            self.win.bind('<Escape>', lambda e: self._quit())
            if self.icon is not None:
                self.win.tk.call('wm', 'iconphoto', self.win._w, self.icon)
        self.title = title
        if self.title is not None:
            self.win.wm_title(title)
        self.position = position
        self.updateTk()

    def setDataFrame(self, dataframe):
        self.dataframe = dataframe

    def updateTk(self):

        # look
        width = 130 * self.dataframe.shape[1]
        
        # use a scroll bar for dataframes with more than 15 rows
        if self.dataframe.shape[0] > 15:
            scrollbar_bool=True
            width += 15 # for the scrollbar
            height = 450 + 25
        else:
            scrollbar_bool=False
            height = 30 * self.dataframe.shape[0] + 25 # 30 per row + 25 margin

        if self.position is not None:
            self.win.geometry(f'{width}x{height}+{self.position[0]}+{self.position[1]}') # (width, height, x, y)
        else:
            self.win.geometry(f'{width}x{height}')
        
        # frame
        if self.tree_frame is not None:
            self.tree_frame.destroy()

        self.win.grid_rowconfigure(0, weight=1)
        self.win.grid_columnconfigure(0, weight=1)

        self.tree_frame = tk.Frame(self.win, borderwidth=0)
        self.tree_frame.grid(column=0, row=0, sticky="nsew")

        # treeview
        if self.headings:
            self.tree = ttk.Treeview(self.tree_frame, style="mystyle.Treeview", columns=list(self.dataframe.columns), height=self.dataframe.shape[0], show='headings')
        else:
            self.tree = ttk.Treeview(self.tree_frame, style="mystyle.Treeview", columns=list(self.dataframe.columns), height=self.dataframe.shape[0], show='tree')

        self.tree.pack(side=tk.LEFT, expand=True, fill=tk.BOTH)

        if scrollbar_bool:
            scrollbar = ttk.Scrollbar(self.tree_frame, orient=tk.VERTICAL, command=self.tree.yview)
            self.tree.configure(yscroll=scrollbar.set)
            scrollbar.pack(side=tk.LEFT, fill=tk.Y)

        for colname in (self.dataframe.columns):
            self.tree.column(colname, anchor='center', width=130, stretch=tk.YES)
            if self.headings:
                self.tree.heading(colname, text=colname, anchor='center', command=lambda _col=colname: treeview_sort_column(self.tree, _col, False))

        self.updateTreeRecords()

    def updateTreeRecords(self, columns: List[str] = []):
        self.tree.delete(*self.tree.get_children()) # delete data for next rendering)

        if columns == []:
            columns = list(self.dataframe.columns)
        
        for row in self.dataframe[columns].to_numpy():
            self.tree.insert("", 0, values=row.tolist())



