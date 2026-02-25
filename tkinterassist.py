# ui.py
from __future__ import annotations

import tkinter as tk
from tkinter import messagebox, filedialog
from typing import Callable, Optional, List, Literal


Align = Literal["left", "center", "right"]


# ======================
# Public helpers
# ======================

def createwindow(
    width: int,
    height: int,
    fullscreen: bool = False,
    title: str = "App"
) -> UIWindow:
    return UIWindow(width, height, fullscreen, title)


def alert(title: str, message: str) -> None:
    messagebox.showinfo(title, message)

def err(title: str, message: str) -> None:
    messagebox.showerror(title, message)

def confirm(title: str, message: str) -> bool:
    return messagebox.askyesno(title, message)


def openfile() -> str:
    return filedialog.askopenfilename()


class RadioGroup:
    def __init__(self):
        self.var = tk.StringVar()
        self.buttons: List[tk.Radiobutton] = []

    def get(self) -> str:
        return self.var.get()


# ======================
# Window
# ======================

class UIWindow:
    def __init__(
        self,
        width: int,
        height: int,
        fullscreen: bool,
        title: str
    ) -> None:
        self._width = width
        self._height = height

        self._root: tk.Tk = tk.Tk()
        self._root.title(title)

        self._visible: bool = True

        if fullscreen:
            self._root.attributes("-fullscreen", True)
            self._width = self._root.winfo_screenwidth()
        else:
            self._root.geometry(f"{width}x{height}")
   
    def setbackground(self, colour: str) -> None:
        self._root.configure(bg=colour)
    # ---------- Internal helpers ----------

    
    def _resolve_x(
        self,
        element_width: int,
        align: Optional[Align],
        x: Optional[int],
        offset: int = 0  # NEW
    ) -> int:
        if x is not None:
            return x + offset  # custom x overrides alignment

        if align == "center":
            return (self._width - element_width) // 2 + offset
        if align == "right":
            return self._width - element_width - 10 + offset

        # left (default)
        return 10 + offset

    # ---------- Controls ----------

    def addbutton(
        self,
        text: str,
        y: int,
        width: int = 100,
        height: int = 30,
        colour: str = "#dddddd",
        textcolour: str = "black",
        command: Optional[Callable[[], None]] = None,
        align: Optional[str] = None,
        x: Optional[int] = None,
        offset: int = 0
    ):
        x_pos = self._resolve_x(width, align, x, offset)

        btn = tk.Button(
            self._root,
            text=text,
            bg=colour,
            fg=textcolour,
            command=command
        )
        btn.place(x=x_pos, y=y, width=width, height=height)

        # Return a wrapper object
        return ButtonWrapper(btn)

    def addlabel(
        self,
        text: str,
        y: int,
        colour: str = "black",
        fontsize: int = 12,
        align: Optional[Align] = None,
        x: Optional[int] = None,
        bg: Optional[str] = None,
        offset: int = 0   # NEW
    ) -> LabelWrapper:  # returns wrapper
        label_bg = bg or (self._bg_colour if hasattr(self, "_bg_colour") else self._root["bg"])
        label = tk.Label(
            self._root,
            text=text,
            fg=colour,
            font=("Arial", fontsize),
            bg=label_bg
        )

        label.update_idletasks()
        width = label.winfo_reqwidth()
        x_pos = self._resolve_x(width, align, x, offset)
        label.place(x=x_pos, y=y)

        return LabelWrapper(label)

    def addtextbox(
        self,
        y: int,
        width: int = 150,
        align: Optional[Align] = None,
        x: Optional[int] = None,
        default: str = "",
        offset: int = 0  
    ) -> TextBox:
        x_pos = self._resolve_x(width, align, x, offset)

        entry = tk.Entry(self._root)
        entry.place(x=x_pos, y=y, width=width)

        # Set default text
        entry.insert(0, default)

        return TextBox(entry)

    def addcheckbox(
        self,
        text: str,
        y: int,
        align: Optional[Align] = None,
        x: Optional[int] = None,
        offset: int = 0   # NEW
    ) -> CheckBox:
        var = tk.BooleanVar()
        chk = tk.Checkbutton(self._root, text=text, variable=var)

        chk.update_idletasks()
        width = chk.winfo_reqwidth()

        x_pos = self._resolve_x(width, align, x, offset)
        chk.place(x=x_pos, y=y)

        return CheckBox(var)

    def addslider(
        self,
        y: int,
        width: int = 200,
        min_value: int = 0,
        max_value: int = 100,
        start: int = 0,
        align: Optional[Align] = None,
        x: Optional[int] = None,
        offset: int = 0   # NEW
    ) -> Slider:
        x_pos = self._resolve_x(width, align, x, offset)

        var = tk.IntVar(value=start)
        scale = tk.Scale(
            self._root,
            from_=min_value,
            to=max_value,
            orient=tk.HORIZONTAL,
            variable=var,
            showvalue=True
        )
        scale.place(x=x_pos, y=y, width=width)
        return Slider(var)


    def addradiobutton(
        self,
        text: str,
        y: int,
        group: RadioGroup,
        value: str,
        command: Optional[Callable[[], None]] = None,
        x: Optional[int] = None,
        align: Optional[str] = "left"
    ) -> tk.Radiobutton:
        x_pos = self._resolve_x(100, align, x)  # default width 100
        rb = tk.Radiobutton(
            self._root,
            text=text,
            variable=group.var,
            value=value,
            command=command,
            bg=getattr(self, "_bg_colour", "#ffffff")
        )
        rb.place(x=x_pos, y=y)
        group.buttons.append(rb)
        return rb

    def addframe(
        self,
        y: int,
        width: int,
        height: int,
        x: Optional[int] = None,
        align: Optional[str] = "left",
        colour: Optional[str] = None
    ) -> FrameWrapper:
        x_pos = self._resolve_x(width, align, x)
        frame_bg = colour or getattr(self, "_bg_colour", self._root["bg"])
        frame = tk.Frame(self._root, width=width, height=height, bg=frame_bg)
        frame.place(x=x_pos, y=y)
        return FrameWrapper(frame)    

    def adddropdown(
        self,
        y: int,
        options: List[str],
        width: int = 15,
        default: Optional[str] = None,
        align: Optional[Align] = None,
        x: Optional[int] = None,
        offset: int = 0   # NEW
    ) -> Dropdown:
        var = tk.StringVar()
        if default:
            var.set(default)
        elif options:
            var.set(options[0])

        dropdown = tk.OptionMenu(self._root, var, *options)
        dropdown.config(width=width)

        dropdown.update_idletasks()
        px_width = dropdown.winfo_reqwidth()

        x_pos = self._resolve_x(px_width, align, x)
        dropdown.place(x=x_pos, y=y)

        return Dropdown(var)

    # ---------- Events ----------

    def onkey(self, key: str, action: Callable[[], None]) -> None:
        self._root.bind(f"<{key}>", lambda _: action())

    def after(self, ms: int, action: Callable[[], None]) -> None:
        self._root.after(ms, action)

    # ---------- Visibility ----------

    def show(self) -> None:
        if not self._visible:
            self._root.deiconify()
            self._visible = True

    def hide(self) -> None:
        if self._visible:
            self._root.withdraw()
            self._visible = False

    def toggle(self) -> None:
        self.hide() if self._visible else self.show()

    # ---------- Window Control ----------

    def close(self) -> None:
        self._root.destroy()

    def run(self) -> None:
        self._root.mainloop()






# ======================
# Safe wrappers
# ======================


class TextBox:
    def __init__(self, entry: tk.Entry) -> None:
        self._entry = entry

    def get(self) -> str:
        return self._entry.get()

    def set(self, value: str) -> None:
        self._entry.delete(0, tk.END)
        self._entry.insert(0, value)

    def clear(self) -> None:
        self._entry.delete(0, tk.END)


class CheckBox:
    def __init__(self, var: tk.BooleanVar) -> None:
        self._var = var

    def get(self) -> bool:
        return self._var.get()

    def set(self, value: bool) -> None:
        self._var.set(value)


class Slider:
    def __init__(self, var: tk.IntVar) -> None:
        self._var = var

    def get(self) -> int:
        return self._var.get()

    def set(self, value: int) -> None:
        self._var.set(value)


class Dropdown:
    def __init__(self, var: tk.StringVar) -> None:
        self._var = var

    def get(self) -> str:
        return self._var.get()

    def set(self, value: str) -> None:
        self._var.set(value)

class LabelWrapper:
    def __init__(self, label: tk.Label):
        self._label = label

    def set(self, text: str):
        self._label.config(text=text)

    def get(self) -> str:
        return self._label.cget("text")

class ButtonWrapper:
    def __init__(self, widget: tk.Button):
        self._widget = widget

    def destroy(self):
        self._widget.destroy()