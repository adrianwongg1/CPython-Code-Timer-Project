import time
from tkinter import Toplevel, Frame, Label, Button, PhotoImage
from tkinter import SUNKEN, TOP, BOTTOM, LEFT, X, BOTH, W, EW, NSEW, E

class Timer(Toplevel):
    '''
    This class handles the timer of a function or a file and returns a value
    in milliseconds to be displayed in the shell for the user to see.
    
    '''
    def __init__(self, parent, title='Timer', *, _htest=False, _utest=False):
        """Create popup, do not return until tk widget destroyed.

        parent - parent of this dialog
        title - string which is title of popup dialog
        _htest - bool, change box location when running htest
        _utest - bool, don't wait_window when running unittest
        """
        Toplevel.__init__(self, parent)
        self.configure(borderwidth=5)
        # place dialog below parent if running htest
        self.geometry("+%d+%d" % (
                        parent.winfo_rootx()+30,
                        parent.winfo_rooty()+(30 if not _htest else 100)))
        self.bg = "#bbbbbb"
        self.fg = "#000000"
        self.create_widgets()
        self.resizable(height=False, width=False)
        self.title(title)
        self.transient(parent)
        self.grab_set()
        self.protocol("WM_DELETE_WINDOW", self.close)
        self.parent = parent
        self.button_close.focus_set()
        self.bind('<Return>', self.close)  # dismiss dialog
        self.bind('<Escape>', self.close)  # dismiss dialog
        self._current_textview = None
        self._utest = _utest

        if not _utest:
            self.deiconify()
            self.wait_window()

    def create_widgets(self):
        frame = Frame(self, borderwidth=2, relief=SUNKEN)
        frame_buttons = Frame(self)
        frame_buttons.pack(side=BOTTOM, fill=X)
        frame.pack(side=TOP, expand=True, fill=BOTH)
        self.button_run = Button(frame_buttons, text='Run',
                                 command=self.run)
        self.button_run.pack(side=LEFT, padx=10, pady=10)
        self.button_rerun = Button(frame_buttons, text='Rerun',
                                   command=self.rerun)
        self.button_rerun.pack(side=LEFT, padx=10, pady=10)
        self.button_close = Button(frame_buttons, text='Close',
                                command=self.close)
        self.button_close.pack(side=LEFT, padx=10, pady=10)

        frame_background = Frame(frame, bg=self.bg)
        frame_background.pack(expand=True, fill=BOTH)

        self.header = Label(frame_background, text='00:00:00', fg=self.fg,
                       bg=self.bg, font=('courier', 24, 'bold'))
        self.header.grid(row=0, column=0, sticky=E, padx=10, pady=10)

    def update_header(self, elapsed_time):
        # Format as HH:MM:SS.mmm
        seconds = int(elapsed_time)
        millis = int((elapsed_time - seconds) * 1000)
        formatted = time.strftime('%H:%M:%S', time.gmtime(seconds)) + f".{millis:03d}"
        print(f'formatted time to change in timer {formatted}')
        self.header.config(text=formatted)

    def run(self, event=None):
        print("Running timer")
        self.parent.timer_run_requested = True
        # Trigger the run-module event
        self.parent.text.event_generate("<<run-module>>")
        print('running module')

    def rerun(self, event=None):
        print("Rerunning timer")

    def close(self, event=None):
        "Dismiss timer window."
        self.grab_release()
        self.destroy()