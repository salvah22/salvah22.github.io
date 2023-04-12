"""
Money Manager software developed by Salvador Hernández
Created: September 2022
Last Edit: February 2023
"""

# standard python libraries

import sys, yaml, os
import datetime
from dateutil.relativedelta import relativedelta
import tkinter as tk
from tkinter import filedialog
from tkinter import ttk
from tkinter.messagebox import showinfo

# extra libraries
import pandas as pd

# own utils
from utils.time import parse_period
from utils.data import *
from utils.graph import *
from utils.tk_inter import *
from modules.groupwindow import *
from modules.treewindow import *


class App:
    """
    https://stackoverflow.com/questions/3794268/command-for-clicking-on-the-items-of-a-tkinter-treeview-widget
    """
    today = datetime.datetime.today()
    todays_month = datetime.datetime(today.year, today.month, 1)

    '''
    @property
    def period(self):
        return self._period

    @period.setter
    def period(self, value):
        self._period = value
        self.period_update_callback()

    def period_update_callback(self):
        self.tk_elems['period_days'].set(str(self.period.days) + " days")
        self.tk_elems['period_months'].set(str(self.period.months) + " months")
        self.tk_elems['period_years'].set(str(self.period.years) + " years")
    '''

    # constructor, loads configs, data, and bootstrap the tk inter
    def __init__(self, data_path:str=None, config_path:str=None, tk:bool=True):
        self.initiated = False
        ### parameters ###
        # load config file
        if config_path and os.path.exists(config_path):
            pass
        elif os.path.exists('src'):
            config_path = 'src/configs/app.yml'
        else:
            print('cannot locate app.yml config file')
        with open(config_path, 'r') as f:
            self.config = yaml.load(f, Loader=yaml.FullLoader)
        # initiate important variables
        self.period = relativedelta(months=1)
        self.group = 'None'
        self.group_opts = []
        self.in_out = self.config['default_subset']
        self.dates = {'start': self.todays_month - self.period, 'end': self.todays_month} # dates in ISO format: '2022-06-01T00:00:00'
        ### load data ###
        # locate input data to load as dataframe
        if data_path:
            if os.path.exists(data_path):
                self.data_path = data_path
            else:
                print('file path supplied via data_path arg is not valid')
        elif len(sys.argv) > 1:
            if os.path.exists(sys.argv[1]):
                self.data_path = sys.argv[1]
            else:
                print('file path supplied via sys.argv is not valid')
        else:
            self.data_path = 'src/resources/dummy_data_with_balances.xlsx'
        self.df = pd.DataFrame()
        self.df_subset = pd.DataFrame()
        self.load_df()
        print('data loaded and prepared successfully')
        # df must have Row and AccountBalance columns
        self.config['columns'].insert(0, 'Row')
        self.config['columns'].append('AccountBalance')
        self.config['display_columns'] = self.config['columns']

        ### tk inter gui ###
        self.tk_elems = {}
        if tk:
            self.init_tk()
            self.balances_win = treewindow(icon=self.tk_elems['icon'])
            # self.plt_win = pltwindow(icon=self.tk_elems['icon'])
            # self.groupby_win = treewindow(icon=self.tk_elems['icon'])
            self.groupby_win = groupwindow(icon=self.tk_elems['icon'], app=self)
            self.details = treewindow(icon=self.tk_elems['icon'])
            # show popup window with balances
            self.move_time_window('onwards') # wraps update_subset
            self.show_balances()
            self.update_groupby_win('Category')
            self.initiated = True
            self.tk_elems['main_app'].mainloop()


    def load_df(self):
        # for employing the proper load function based on extension
        self.df = data_loader(self.data_path)
        # analyze the df for main_currency
        self.determine_main_currency()
        # ensure a datatime type column exists, fills NA's, adds Row and AccountBalance columns, sort by Day:
        self.df = data_prepare(self.df, self.config['main_currency'])
        # write the dates of the first and last record
        self.dates['first_record'] = datetime.datetime.fromisoformat(self.df['Day'].iloc[0])
        self.dates['last_record'] = datetime.datetime.fromisoformat(self.df['Day'].iloc[-1]) + relativedelta(days=1)

    def determine_main_currency(self):
        c = self.config['currencies'] 
        for currency in c:
            if currency in self.df.columns:
                self.config['main_currency'] = currency
                self.config['columns'].append(currency)
                return
        print('no valid currency found in dataframe. the header of one column has to match one of the following: ' + str(c))     

    def init_tk(self):
        ### main definitions
        self.windows = ['main_app']
        self.tk_elems['tree_main_records'] = 15
        self.tk_elems['frame_tree_height'] = int(30 * self.tk_elems['tree_main_records'])
        self.tk_elems['frame_tree_width'] = int(60 + (len(self.config['display_columns']) - 1) * 130) # 60 idx + 130 p/column 
        self.tk_elems['main_app'] = tk.Tk()
        self.tk_elems['main_app'].title('Money Mgr.')
        self.tk_elems['main_app'].bind('<Escape>', lambda e: self.tk_elems['main_app'].quit())
        self.tk_elems['main_app'].tk.call('source', 'src/configs/forest-dark.tcl')
        
        self.tk_elems['screen_width'] = self.tk_elems['main_app'].winfo_screenwidth()
        self.tk_elems['screen_height'] = self.tk_elems['main_app'].winfo_screenheight()
        self.tk_elems['main_app_width'] = self.tk_elems['frame_tree_width'] + 10 # + 10 for margins ~ 1000
        self.tk_elems['main_app_height'] = self.tk_elems['frame_tree_height'] + 110 # 450 treeview + 110 other elements ~ 650
        self.tk_elems['main_app'].geometry(f'{self.tk_elems["main_app_width"]}x{self.tk_elems["main_app_height"]}')
        self.tk_elems['main_app_x'] = int((self.tk_elems['screen_width'])/2 - (self.tk_elems['main_app_width'])/2) # screen_width - app_width
        self.tk_elems['main_app_y'] = int((self.tk_elems['screen_height'])/2 - (self.tk_elems['main_app_height'])/2)
        self.tk_elems['icon'] = tk.PhotoImage(file="src/resources/favicon.png")
        self.tk_elems['main_app'].tk.call('wm', 'iconphoto', self.tk_elems['main_app']._w, self.tk_elems['icon'])
        ### menu bar
        self.tk_elems['main_app_menubar'] = tk.Menu(self.tk_elems['main_app'])
        # file cascade menu
        self.tk_elems['main_app_filemenu'] = tk.Menu(self.tk_elems['main_app_menubar'], tearoff=0)
        self.tk_elems['main_app_filemenu'].add_command(label="Exit", command=self.tk_elems['main_app'].quit)
        self.tk_elems['main_app_menubar'].add_cascade(label="File", menu=self.tk_elems['main_app_filemenu'])
        # view cascade menu
        self.tk_elems['main_app_viewmenu'] = tk.Menu(self.tk_elems['main_app_menubar'], tearoff=0)
        self.tk_elems['main_app_viewmenu'].add_command(label="Balances", command=self.show_balances)
        self.tk_elems['main_app_viewmenu'].add_command(label="Group By", command=lambda: self.update_groupby_win('Category'))
        self.tk_elems['main_app_menubar'].add_cascade(label="View", menu=self.tk_elems['main_app_viewmenu'])
        # set menubar when ready
        self.tk_elems['main_app'].config(menu=self.tk_elems['main_app_menubar'])
        ### style
        self.tk_elems['style'] = ttk.Style()
        self.tk_elems['style'].theme_use('forest-dark') # for all ttk elems
        self.tk_elems['style_bg_col'] = str(self.tk_elems['style'].lookup('TFrame', 'background'))
        plt.rcParams['figure.facecolor'] = self.tk_elems['style_bg_col']
        self.tk_elems['style'].configure("mystyle.Treeview", rowheight=30) # default: 20
        self.tk_elems['style'].configure("mystyle.Treeview", font=self.config['fonts']['f08'])
        self.tk_elems['style'].configure("mystyle.Treeview.Heading", font=self.config['fonts']['f10'])
        self.tk_elems['style'].layout("mystyle.Treeview", [('mystyle.Treeview.treearea', {'sticky': 'nswe'})])
        self.tk_elems['frame_header'] = tk.Frame(self.tk_elems['main_app'], borderwidth=0)
        self.tk_elems['frame_header'].pack(expand=True)
        ### Period frames
        self.tk_elems['button_last'] = ttk.Button(self.tk_elems['frame_header'], text='Today', style='Accent.TButton', command=lambda: self.move_time_window('today'))
        self.tk_elems['button_last'].grid(row=0, column=0, padx=(5,5), pady=5, sticky="nsew") #.pack(side=tk.LEFT, fill=tk.Y)
        self.tk_elems['button_today'] = ttk.Button(self.tk_elems['frame_header'], text='First', command=lambda: self.move_time_window('last') )
        self.tk_elems['button_today'].grid(row=0, column=1, padx=(0,5), pady=5, sticky="nsew")
        self.tk_elems['frame_period'] = tk.Frame(self.tk_elems['frame_header'], borderwidth=0)
        self.tk_elems['frame_period'].grid(row=0, column=2, padx=(0,5), pady=5, sticky="nsew", columnspan=1) # .pack(expand=True, side=tk.LEFT, fill=tk.Y)

        self.tk_elems['frame_period_alter'] = tk.Frame(self.tk_elems['frame_period'], borderwidth=0)
        self.tk_elems['frame_period_alter'].pack( side=tk.BOTTOM, fill=tk.Y)
        self.tk_elems['start_date'] = tk.StringVar()
        self.tk_elems['end_date'] = tk.StringVar()
        c = 0
        self.tk_elems['button_backwards'] = ttk.Button(self.tk_elems['frame_period_alter'], text='◄', command=lambda: self.move_time_window('backwards'))
        self.tk_elems['button_backwards'].grid(row=0, column=c, sticky="w", padx=5) 
        c += 1
        self.tk_elems['entry_date_start'] = ttk.Entry(self.tk_elems['frame_period_alter'], textvariable=self.tk_elems['start_date'],justify='center', width=10)
        self.tk_elems['entry_date_start'].grid(row=0, column=1, sticky="nsew", padx=5)
        self.tk_elems['entry_date_start'].bind('<Return>', lambda event: self.on_entry_change('start'))
        c += 1
        self.tk_elems['entry_date_end'] = ttk.Entry(self.tk_elems['frame_period_alter'], textvariable=self.tk_elems['end_date'], justify='center', width=10)
        self.tk_elems['entry_date_end'].grid(row=0, column=2, sticky="nsew", padx=5) 
        self.tk_elems['entry_date_end'].bind('<Return>', lambda event: self.on_entry_change('end'))
        c += 1
        self.tk_elems['button_onwards'] = ttk.Button(self.tk_elems['frame_period_alter'], text='►', command=lambda: self.move_time_window('onwards'))
        self.tk_elems['button_onwards'].grid(row=0, column=3, sticky="w", padx=5) 

        self.tk_elems['frame_DMY'] = tk.Frame(self.tk_elems['frame_period'], borderwidth=0)
        self.tk_elems['frame_DMY'].pack(expand=True, side=tk.BOTTOM, fill=tk.Y)

        self.tk_elems['period_days'] = tk.StringVar()
        self.tk_elems['period_days'].set('0')
        self.tk_elems['period_months'] = tk.StringVar()
        self.tk_elems['period_months'].set('1')
        self.tk_elems['period_years'] = tk.StringVar()
        self.tk_elems['period_years'].set('0')

        c = 0
        tk.Label(self.tk_elems['frame_DMY'], text="Days", font=self.config['fonts']['f10']).grid(row=0, column=c, sticky="nsew", padx=5) 
        c += 1
        self.tk_elems['spinbox_period_days'] = ttk.Spinbox(self.tk_elems['frame_DMY'], textvariable=self.tk_elems['period_days'], from_=0, to=31, increment=1, width=3)
        self.tk_elems['spinbox_period_days'].grid(row=0, column=c, sticky="nsew", padx=(0,10)) 
        c += 1
        tk.Label(self.tk_elems['frame_DMY'], text="Months", font=self.config['fonts']['f10']).grid(row=0, column=c, sticky="nsew", padx=5) 
        c += 1
        self.tk_elems['spinbox_period_months'] = ttk.Spinbox(self.tk_elems['frame_DMY'], textvariable=self.tk_elems['period_months'], from_=0, to=11, increment=1, width=3)
        self.tk_elems['spinbox_period_months'].grid(row=0, column=c, sticky="nsew", padx=(0,10)) 
        c += 1
        tk.Label(self.tk_elems['frame_DMY'], text="Years", font=self.config['fonts']['f10']).grid(row=0, column=c, sticky="nsew", padx=5) 
        c += 1
        self.tk_elems['spinbox_period_years'] = ttk.Spinbox(self.tk_elems['frame_DMY'], textvariable=self.tk_elems['period_years'], from_=0, to=99, increment=1, width=3)
        self.tk_elems['spinbox_period_years'].grid(row=0, column=c, sticky="nsew") 

        ### Button Group In/Out (EXPENSE/INCOME/TRANSFER/ALL)
        self.tk_elems['frame_in_out'] = tk.Frame(self.tk_elems['frame_header'], borderwidth=0)
        self.tk_elems['frame_in_out'].grid(row=0, column=3, padx=(0,5), pady=5, sticky="nsew", columnspan=2)#.pack(expand=True, side=tk.LEFT, fill=tk.BOTH)
        self.tk_elems['frame_in_out'].columnconfigure(tuple(range(2)), weight=1)
        self.tk_elems['frame_in_out'].rowconfigure(tuple(range(2)), weight=1)
        self.tk_elems['button_income'] = ttk.Button(self.tk_elems['frame_in_out'], text='Income', 
                                                  command=lambda: self.update_subset('inout_Income'))
        self.tk_elems['button_income'].grid(row=0, column=0, sticky="nswe", padx=(0,2.5), pady=(0,2.5))
        self.tk_elems['button_expenses'] = ttk.Button(self.tk_elems['frame_in_out'], text='Expenses',
                                                  command=lambda: self.update_subset('inout_Expenses'))
        self.tk_elems['button_expenses'].grid(row=1, column=0, sticky="nswe", padx=(0,2.5), pady=(2.5,0))
        self.tk_elems['button_transfers'] = ttk.Button(self.tk_elems['frame_in_out'], text='Transfer',
                                                  command=lambda: self.update_subset('inout_Transfer'))
        self.tk_elems['button_transfers'].grid(row=0, column=1, sticky="nswe", padx=(2.5,0), pady=(0,2.5))
        self.tk_elems['button_all'] = ttk.Button(self.tk_elems['frame_in_out'], text='All',
                                                  command=lambda: self.update_subset('inout_All'))
        self.tk_elems['button_all'].grid(row=1, column=1, sticky="nswe", padx=(2.5,0), pady=(2.5,0))
        ### GROUPING
        self.tk_elems['frame_groups'] = tk.Frame(self.tk_elems['frame_header'], padx=5, pady=5) # , highlightbackground="black", highlightthickness=2
        self.tk_elems['frame_groups'].grid(row=0, column=5, padx=(0,5), pady=5, sticky="nsew")#.pack(expand=True)
        ttk.Label(self.tk_elems['frame_groups'], text="Grouping").grid(row=0, column=0, sticky="nsew") 
        self.tk_elems['group'] = tk.StringVar()
        self.tk_elems['group_opt_menu'] = ttk.OptionMenu(self.tk_elems['frame_groups'], self.tk_elems['group'],"None", "None", "Day", "Month", "Year", command=self.group_change)
        self.tk_elems['group_opt_menu'].grid(row=1, column=0, sticky="nsew") 
        self.tk_elems['group_category'] = tk.BooleanVar(value=False)
        self.tk_elems['checkbox_category'] = ttk.Checkbutton(self.tk_elems['frame_groups'], text='category', variable=self.tk_elems['group_category'], onvalue=True, offvalue=False, command=self.group_opts_change)
        self.tk_elems['checkbox_category'].grid(row=2, column=0, sticky="nsew")  #.pack(side=tk.TOP, expand=True, padx=(0, 5))
        ### MAIN BIG TREE
        self.tk_elems['frame_tree_container'] = tk.Frame(self.tk_elems['main_app'])
        self.tk_elems['frame_tree_container'].pack(expand=True, side=tk.TOP)
        self.tk_elems['frame_tree'] = tk.Frame(self.tk_elems['frame_tree_container'], width=self.tk_elems["frame_tree_width"], height=self.tk_elems['frame_tree_height']) # -20 for the scrollbar
        self.tk_elems['frame_tree'].grid(row=0, column=0)
        # By default, Tkinter Frame fits to its children and thus its width and height depends on its children. 
        # You can override this behavior and force a specific width and height to the frame.
        self.tk_elems['frame_tree'].pack_propagate(0)
        self.tk_elems['tree_main'] = ttk.Treeview(self.tk_elems['frame_tree'], style="mystyle.Treeview", height=self.tk_elems['tree_main_records'], columns=self.config['display_columns'], show='headings') # originally height=10
        self.tk_elems['tree_main'].bind('<Double-1>', self.on_double_click)
        self.tk_elems['tree_main'].pack(side=tk.LEFT) # .pack(side=tk.LEFT)
        update_tree_structure(self.tk_elems['tree_main'], self.config['display_columns'])
        self.tk_elems['tree_main_scrollbar'] = ttk.Scrollbar(self.tk_elems['frame_tree_container'], orient=tk.VERTICAL, command=self.tk_elems['tree_main'].yview)
        self.tk_elems['tree_main'].configure(yscroll=self.tk_elems['tree_main_scrollbar'].set)
        self.tk_elems['tree_main_scrollbar'].grid(row=0, column=1, sticky='ns') # .pack(side=tk.LEFT, fill=tk.Y)

        # the period spinbox variables need to be defined after tree_main exists
        self.tk_elems['period_days'].trace('w', lambda *_: self.on_entry_change('period'))
        self.tk_elems['period_months'].trace('w', lambda *_: self.on_entry_change('period'))
        self.tk_elems['period_years'].trace('w', lambda *_: self.on_entry_change('period'))

    def group_opts_change(self):
        if self.tk_elems['group_category'].get():
            self.group_opts.append('Category')
        elif 'Category' in self.group_opts:
            self.group_opts.remove('Category')
        # if group options change but we not showing groups leave it
        if self.group != "None":
            self.group_change(self.group)

    def group_change(self, group):
        self.details.close()
        self.group = group

        if group == 'None':
            self.config['display_columns'] = self.config['columns']
            # -1 since original columns got the Row column
            self.tk_elems['frame_tree_width'] = int(60 + (len(self.config['display_columns']) - 1) * 130)
        else:
            self.config['display_columns'] = ['group'] + self.group_opts + [self.config['main_currency']]
            # groups aint got Row col
            self.tk_elems['frame_tree_width'] = int(len(self.config['display_columns']) * 130)
            
        self.tk_elems['frame_tree']['width'] = self.tk_elems['frame_tree_width']
        update_tree_structure(self.tk_elems['tree_main'], self.config['display_columns'])
        self.update_subset()

    def move_time_window(self, direction=''):
        self.details.close()
        if direction == 'today':
            self.tk_elems['period_days'].set('0')
            self.tk_elems['period_months'].set('1')
            self.tk_elems['period_years'].set('0')
            self.period = relativedelta(months=1)
            self.dates['start'] = self.todays_month - self.period
            self.dates['end'] = self.todays_month
        elif direction == 'last':
            self.tk_elems['period_days'].set('0')
            self.tk_elems['period_months'].set('1')
            self.tk_elems['period_years'].set('0')
            self.period = relativedelta(months=1)
            self.dates['start'] = self.dates['first_record']
            self.dates['end'] = self.dates['first_record'] + self.period
        elif direction == 'backwards':
            self.dates['start'] = self.dates['start'] - self.period
            self.dates['end'] = self.dates['end'] - self.period
            if self.dates['end'] < self.dates['first_record']:
                showinfo('Information', 'Period set before the first record ('+str(self.dates['first_record'])+')')
        elif direction == 'onwards':
            self.dates['start'] = self.dates['start'] + self.period
            self.dates['end'] = self.dates['end'] + self.period
            if self.dates['start'] > self.dates['last_record']:
                if self.initiated:
                    showinfo('Information', 'Period set past the last record ('+str(self.dates['last_record'])+')')
                else:
                    self.move_time_window('backwards')
        self.tk_elems['start_date'].set(self.dates['start'].strftime("%Y-%m-%d"))
        self.tk_elems['end_date'].set(self.dates['end'].strftime("%Y-%m-%d"))
        self.update_subset()
        self.tk_elems['tree_main'].yview_moveto(0)


    def update_subset(self, instruction=''):
        self.details.close()

        # timely
        if self.dates['start'] and self.dates['end']:
            self.df_subset = self.df[(self.dates['start'] <= self.df['datetime']) & (self.df['datetime'] <= self.dates['end'])]
        self.tk_elems['start_date'].set(self.dates['start'].strftime("%Y-%m-%d"))
        self.tk_elems['end_date'].set(self.dates['end'].strftime("%Y-%m-%d"))

        # in/out
        if instruction[:5] == 'inout':
            self.in_out = instruction[6:]
        if self.in_out == 'All':
            pass
        elif self.in_out in ['Income', 'Expenses']:
            self.df_subset = self.df_subset[self.df_subset['Income/Expenses'] == self.in_out]
        elif self.in_out == 'Transfer':
            self.df_subset = self.df_subset[(self.df_subset['Income/Expenses'] == 'Transfer in') | (self.df_subset['Income/Expenses'] == 'Transfer out')]

        # groups
        if self.group != 'None':
            if self.group == 'Day':
                self.df_subset['group'] = self.df_subset['Day']
            elif self.group == 'Month':
                self.df_subset['group'] = [year_month_from_iso(_) for _ in self.df_subset['Day'].to_list()]
            elif self.group == 'Year':
                self.df_subset['group'] = [year_from_iso(_) for _ in self.df_subset['Day'].to_list()]
            self.df_subset = self.df_subset.groupby(['group'] + self.group_opts).sum()[self.config['main_currency']].reset_index()
            # group has the bad habit of having infinite decimal places
            self.df_subset[self.config['main_currency']] = self.df_subset[self.config['main_currency']].round(2)

        update_tree_records(self.df_subset, self.tk_elems['tree_main'], self.config['display_columns'])

        # update groupby_win if it was initiated
        if self.groupby_win.initiated:
            self.update_groupby_win(self.group_by)


    def on_double_click(self, event):
        tree_idx = self.tk_elems['tree_main'].identify('item', event.x, event.y)
        df_idx = int(self.tk_elems['tree_main'].item(tree_idx, 'values')[0]) # formerly (tree_idx, 'text') when Row was supplied
        
        self.details.update(
            dataframe = pd.DataFrame([self.df_subset.columns,self.df_subset.loc[df_idx].to_list()]).T.rename(columns={0: "Column", 1: "Cell"}),
            title = "Details",
            position = [
                self.tk_elems['main_app_width'] + self.tk_elems['main_app_x'] + 15, 
                self.tk_elems['main_app_y'] + self.balances_win.dataframe.shape[0] * 30 + 60 # 30 * 11 ~ 340
            ]

        )


    def on_entry_change(self, instruction):
        if instruction == 'start':
            self.dates['start'] = datetime.datetime.fromisoformat(self.tk_elems['start_date'].get())
        elif instruction == 'end':
            self.dates['end'] = datetime.datetime.fromisoformat(self.tk_elems['end_date'].get())
        elif instruction == 'period':
            yearsStr = self.tk_elems['period_years'].get()
            years = int(yearsStr) if yearsStr != '' else 0
            monthsStr = self.tk_elems['period_months'].get()
            months = int(monthsStr) if monthsStr != '' else 0
            daysStr = self.tk_elems['period_days'].get()
            days = int(daysStr) if daysStr != '' else 0
            self.period = relativedelta(years=years, months=months, days=days)
            if self.dates['start'] + self.period <= self.dates['last_record']:
                self.dates['end'] = self.dates['start'] + self.period
            else:
                self.dates['start'] = self.dates['end'] - self.period

        if instruction in ['end', 'start']:
            self.period = parse_period(self.dates['start'], self.dates['end'])
            # TODO: WRITE THIS PERIOD NOW THAT IS WORKING REALLY COOL TO A DROPDOWN / ENTRY

        self.update_subset()


    def update_groupby_win(self, by):
        self.group_by = by
        grouped = self.df_subset.groupby([by])[self.config['main_currency']]
        groupedsum = grouped.sum().reset_index()
        groupedsorted = groupedsum.sort_values(by=self.config['main_currency'], ascending=True)
        groupedsortedrounded = groupedsorted.round(0)

        self.groupby_win.update(
            dataframe = groupedsortedrounded,
            fig = pie_chart(df_grouped=grouped, color=self.tk_elems['style_bg_col']),
            title = f"{self.in_out} grouped by {by}",
            position = [15, 15] # [x,y]
        )


    def show_balances(self):
        balances = pd.DataFrame(get_last_balance_per_account(self.df), columns=["Account",self.config['main_currency']])

        self.balances_win.update(
            dataframe=balances[-balances["Account"].isin(self.config['hidden_balances'])], 
            title="Balances", 
            position=[ # [x,y]
                self.tk_elems['main_app_width'] + self.tk_elems['main_app_x'] + 15, 
                self.tk_elems['main_app_y'] - 13
            ]
        )


if __name__ == '__main__':
    app = App()