'''
Window for app's config
'''

import tkinter as tk
from tkinter.ttk import Button

from modules.window import Window

class Filterswindow(Window):
    '''
    Window for app's config
    '''

    def __init__(self, app, icon):
        super().__init__()
        self.icon = icon
        self.app = app
        self.main = None
        self.frame = None

    def show(self, filters_list):
        ### init the toplevel tk element
        if self.main is None or not self.main.winfo_exists():
            self.main = tk.Toplevel(self.app.main.main)
            self.main.group(self.app.main.main)
            self.main.bind('<Escape>', lambda e: self._quit())
            if self.icon is not None:
                self.main.tk.call('wm', 'iconphoto', self.main._w, self.icon)

        self.main.wm_title("Filters")

        # if the frame exists, detroy it
        if self.frame is not None:
            self.frame.destroy()
        
        self.frame = tk.Frame(self.main, borderwidth=0)
        self.frame.pack(side=tk.TOP, fill=tk.Y, expand=1)

        r = 0
        buttons = {}
        for _ in filters_list:
            c = 0
            tk.Label(self.frame, text=_[0]).grid(row=r, column=c, padx=5, pady=5, sticky="w")
            c += 1
            tk.Label(self.frame, text=_[1]).grid(row=r, column=c, padx=5, pady=5, sticky="w")
            c += 1
            buttons[r] = Button(self.frame, text='X', command=lambda: self.remove_filter(_))
            buttons[r].grid(row=r, column=c, padx=5, pady=5)
            r += 1

    def remove_filter(self, val):
        self.app.filters_list.remove(val)
        print(val)
        print(self.app.filters_list)
        self.app.update_tree_records()
        self.show(self.app.filters_list)