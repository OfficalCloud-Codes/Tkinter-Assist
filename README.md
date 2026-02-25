# Tkinter Assist
Here is an extremly simple wrapper for the complicated Tkinter

# How To Use
Simply download the `tkinterassist.py` file and add into your main folder.

In any file you would like to use this, just add:
```python
Import tkinterassist as ui
```

# Getting Started
Here is a simple demo file to help you get started:
```python
import tkinterassist as ui
window = ui.createwindow(500,500,title="Demo")

window.addlabel("Hello!",y=240,align="center")

window.addbutton("Click Me!",y=280,align="center",command=lambda: print("Click"))

window.run()
```

# Documentation
In this documentation, `tkinterassist` will be displayed as `tka` instead.

align options:

## `tka.createwindow()`
Creates a window instance

### Paramaters

int `width=` Width of the window

int `height=` Height of the window

bool `fullscreen=` Sets if the window is fullscreen

str `title=` Sets the window title

### Returns

A window instance


## `window.addlabel()`
Creates a window instance

### Paramaters

str `text=` Text to be displayed

int `x=` x position of the label

str `colour=` Sets the background colour of the label

str `textcolour=` Sets the text colour of the label

align `align=` Sets the alignment position of the label, if X value is given, it will override align

int `offset=` Offsets the label from its align X

### Returns

A label instance

# This documentation is NOT done
