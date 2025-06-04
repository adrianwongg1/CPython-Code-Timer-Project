from idlelib import timer
import unittest
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
    self.root.withdraw()  
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
