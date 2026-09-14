# CPython IDLE Timer

A fork of CPython that adds a **Timer** feature to IDLE: a popup (`Lib/idlelib/timer.py`)
reachable from an editor window's **Run** menu that runs the current module and
displays how long execution took.

Original CPython build/install instructions are unchanged and still live in
[`README.rst`](README.rst). This document covers building and trying out the
Timer feature specifically.

## Why you can't just use your system Python

This checkout is CPython **3.14** (see `Include/patchlevel.h`). `Lib/idlelib/sidebar.py`
already calls `Text.count(..., return_ints=True)`, a Tk binding feature that
isn't in the tkinter shipped with older system Pythons (3.12/3.13 elsewhere
on the machine). Mixing this source tree's `idlelib` with an unrelated
interpreter's tkinter crashes on startup. You must build and run **this
checkout's own interpreter**.

## 1. One-time setup: install Tcl/Tk

```bash
brew install tcl-tk
```

## 2. Build CPython (from the repo root)

```bash
PKG_CONFIG_PATH="$(brew --prefix tcl-tk)/lib/pkgconfig" ./configure
make -j"$(sysctl -n hw.ncpu)"
```

This produces `./python.exe` at the repo root. A plain (non-optimized,
non-debug) build is enough for iterating on `idlelib` — it's much faster to
build than `--enable-optimizations`, and neither flag is needed just to try
the feature.

You only need to rebuild (`make -j...`) if you touch C source. Any edit
under `Lib/idlelib/*.py` is picked up the next time you launch — no rebuild.

## 3. Launch IDLE

```bash
./python.exe -m idlelib
```

## 4. Use the Timer

The **Shell window** (the one IDLE opens by default) has **no Run menu** —
see `PyShell.menu_specs` in `Lib/idlelib/pyshell.py`. The Timer command
lives on the **editor window's** Run menu, so:

1. Open an editor window: **File → New File** (⌘N), or open an existing
   `.py` file.
2. Write/load some code.
3. **Run → Timer** — opens the Timer popup.
4. Click **Run** in the popup. This runs the module in the subprocess
   (equivalent to Run Module / F5, and likewise restarts the subprocess).
5. The header shows `RUNNING...`, then updates to the elapsed time
   (`HH:MM:SS.mmm`) once the module finishes.

If the module fails to compile (syntax error), the header shows `FAILED!`
instead of a time.

## Known behavior worth knowing

Once a Timer has run a module, its `timer_obj` stays registered as an RPC
proxy on that subprocess for the rest of the subprocess's life. That means
any code you subsequently type directly into the **interactive Shell**
(not just future "Run Module" calls) will also silently update that Timer
window's header — `Executive.runcode()` in `Lib/idlelib/run.py` checks for a
registered `timer_obj` on *every* execution in the subprocess, not just
module runs. Worth keeping in mind if the intent is to time module runs
only.

## Running the unit tests

```bash
./python.exe -m unittest idlelib.idle_test.test_timer -v
```

## Troubleshooting

- `IDLE can't import Tkinter` / `Your Python may not be configured for Tk` —
  wrong interpreter; use `./python.exe` from step 2, not system Python.
- `TypeError: Text.count() got an unexpected keyword argument
  'return_ints'` — same cause: you're running `idlelib` against a tkinter
  older than what this source tree needs.
