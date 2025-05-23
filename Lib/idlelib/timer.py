class Timer:
    '''
    This class handles the timer of a function or a file and returns a value
    in milliseconds to be displayed in the shell for the user to see.
    
    '''

    def __init__(self, editor):
        self.editor = editor

    def show_timer_event(self, event=None):
        print("Hello, World! Timer toggled.")
        # Add additional functionality as needed