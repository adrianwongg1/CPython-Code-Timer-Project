'''
  TODO: 
  1. Add test to check whether the window is created if no error
  2. Check for Error pop-up if file is not saved or no main function is found
  3. Test for an estimate time for a specific function (Will need to be given a range)
  4. Figure out how to test the time of code execution
         a. Either grab the text and try to execute it
         b. Treat it like Pyshell and try to execute it
  5. Add human tests
'''
from idlelib import timer
import unittest
import unittest.mock
from idlelib.delegator import Delegator
from idlelib.percolator import Percolator
import tkinter as tk
from tkinter import Text
from tkinter import messagebox
from idlelib.timer import Timer

class Dummy_editwin:
  def __init__(self, text_content=""):
    self.root = tk.Tk()
    self.root.withdraw()
    self.text = Text(self.root)
    self.text.insert("1.0", text_content)
    self.text.pack()
    self.timer_run_requested = False
    self.scriptbinding = DummyScriptBinding()

class DummyScriptBinding:
  def __init__(self):
    self.run_module_event_called = False
  def run_module_event(self, event=None):
    self.run_module_event_called = True

class TestTimer(unittest.TestCase):
  def setUp(self):
    self.root = tk.Tk()
    self.root.withdraw()  # Hide main window during tests
    self.editwin = Dummy_editwin()
    # Create Timer instance with _utest=True to avoid wait_window()
    self.timer = Timer(self.root, self.editwin, _utest=True)

  def tearDown(self):
    self.timer.destroy()
    self.root.destroy()

  def test_run_sets_flag_and_calls_scriptbinding(self):
    self.editwin.scriptbinding.run_module_event_called = False
    self.timer.run()
    self.assertTrue(self.editwin.timer_run_requested)
    self.assertTrue(self.editwin.scriptbinding.run_module_event_called)

  def test_update_header_formats_time_correctly(self):
    # Pass a float seconds value
    self.timer.update_header(12.345)
    text = self.timer.header['text']
    self.assertIn("00:00:12", text)
    self.assertIn(".", text)

  def test_update_header_accepts_string(self):
    self.timer.update_header("Error")
    self.assertEqual(self.timer.header['text'], "Error")

  def test_close_destroys_timer(self):
    self.timer.close()
    self.assertFalse(self.timer.winfo_exists())
  

if __name__ == '__main__':
    unittest.main()
