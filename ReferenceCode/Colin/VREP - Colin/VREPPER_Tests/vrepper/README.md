# vrepper

Tethered V-REP (using V-REP as a remote controlled multi-body simulator) in Python.


THIS IS A FORK FROM https://github.com/ctmakro/vrepper, WITH SOME ADDITIONAL FEATURES:

- Linux support
- versioned V-Rep libraries, so you don't get any weird version conflicts
- Python 2.7 support
- access to joint angles (reading/writing)
- access to synchronous/non-synchronous simuation
- PEP-8 conformity 


^ these have now been merged by the original author

**NEW FEATURES (2018 Jan 27, v0.0.4):**
- getting images from a V-REP simulated camera
- getting depth maps from simulated camera
- new example with real robot arm

**NEW FEATURES (2018 Feb 04, v0.0.5):**
- less bloat (removed the files that aren't necessary for this library and which are included with the V-Rep installation anyway)
- better V-Rep executable control (i.e. less noisy logging, better killing and instanciating, and propoer port number search all thanks to @CrazyHeex )
- collision detection (this needs a bit work in V-Rep too, see documentation in file "core.py" -> function "def get_collision_handle")

**NEW FEATURES (2018 Apr 16, v0.0.6)**
- added suppot for V-Rep 3.5.0 rev4


The Python binding (`vrep.py` and `vrepConst.py`) and the driver libraries (`remoteApi.dll`, `remoteApi.dylib`, and `remoteApi.so`) are copied as-is from V-REP PRO EDU V3.5


## Prerequisites

Of course in order to use this, you might want to install V-Rep first. If you work in academia or do anything with education, you can get a free educational copy over here: http://www.coppeliarobotics.com/downloads.html 


## Usage

Add the path to your V-REP installation to your `PATH`:

- (Windows) might be something like `C:/Program Files/V-REP3/V-REP_PRO_EDU/`

  ```bash
  $ set PATH=%PATH%;C:/Program Files/V-REP3/V-REP_PRO_EDU/
  ```

- (Mac OS X) might be something like `/Users/USERNAME/V-REP_PRO_EDU/vrep.app/Contents/MacOS/`

  ```bash
  $ export PATH=$PATH:"/Users/USERNAME/V-REP_PRO_EDU/vrep.app/Contents/MacOS/"
  ```

- (Linux) might be something like `/home/USERNAME/tools/V-REP_PRO_EDU_V3_4_0_Linux`

  ```bash
  $ export PATH="/home/USERNAME/tools/V-REP_PRO_EDU_V3_4_0_Linux":$PATH
  ```

Then run the following:

```bash
$ git clone https://github.com/ctmakro/vrepper
$ cd vrepper
$ pip install -e . #(install the vrepper package in edit mode)
$ ipython test_body_joint.py #(run the example)
```

The last command will start V-REP in headless mode (no GUI) and run a simple simulation step-by-step. Then it will shut itself down and exit.

## A note on PyCharm

For those of you using the PyCharm IDE and are having issues running their experiments using the internal Python shell... that's normal. Somewhat. If you start PyCharm from the start menu then it will **NOT** keep any environmental variables (like the `export PATH...` line from above that you should have put in your `~/.bashrc` or `~/.zshrc`). But if you **start PyCharm from a shell** that solves the issue. It's a bit of a nasty workaround, but for the moment that's the easier solution for me (rather than editing the run configuration of every single experiment by hand).

## Why should you use V-REP

- build your model with its GUI tools
- simulate your model with whatever programming language you like

## Why should you use vrepper

If you are looking for:

- remote controlled simulation
- low overhead communication
- ability to start/stop simulation repeatedly to perform all kinds of experiment

Then vrepper has already paved the way for you. You should at least take a look at vrepper's source code.

## Known Issues

- On Linux after the end of the script the V-Rep process isn't killed properly. Workaround: run "killall vrep" manually after the script finishes.
