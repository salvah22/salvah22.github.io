'''
Windows skeleton
'''

class Window:
    '''
    Windows skeleton
    '''

    def _quit(self):
        # self.win.quit()     # stops mainloop
        self.root.destroy()  # this is necessary on Windows to prevent
                            # Fatal Python Error: PyEval_RestoreThread: NULL tstate
        self.root.update()

    def __init__(self):
        self.root = None
        self.position = None
        self.title = None