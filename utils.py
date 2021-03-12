import tkinter as tk
from typing import Set


current_intersections: Set[tk.Button] = set()  # Used to store all placed intersections


def nocommand(*args, **kwargs):
    raise NotImplementedError('Command has not been impleted yet')


def destroy_all(inlist:Set[tk.BaseWidget]):
    """ Iterate over provided set and destroy widgets """
    for widget in inlist:
        try:  # Ensure that we do not break if exceptions occur.
            widget.destroy()
        except Exception as e:
            print(e)
    inlist.clear()  # clear the set once we are finished with it.


class M2ContextMenu(tk.Menu):
    """ This class defines our custom right click menu. """

    def __init__(self, master=None, cnf={}, **kw):
        """ __init__ has been adapted to include our custom commands by default. """

        super().__init__(master, cnf, **kw, tearoff=False)

        # Context specific commands will be inserted at the first index.
        self.add_separator()
        self.add_command(label="Clear Map", command=lambda: destroy_all(current_intersections))
        self.add_command(label="Save Map", command=nocommand)
        self.add_separator()
        self.add_command(label="Exit", command=master.quit)


class MouseLine:
    """ Singleton class which represents the line being drawn between a point and the mouse. """
    _instance = None

    def __new__(self):
        if self._instance is None:
            print('Creating the object')
            self._instance = super(MouseLine, self).__new__(self)
            # Put any initialization here.
        return self._instance


class RoundedButton(tk.Canvas):
    """ Sourced from: https://stackoverflow.com/questions/42579927/rounded-button-tkinter-python """
    def __init__(self, parent, width, height, cornerradius, padding, color, bg, command=None):
        tk.Canvas.__init__(self, parent, borderwidth=0,
            relief="flat", highlightthickness=0, bg=bg)
        self.command = command

        if cornerradius > 0.5*width:
            print("Error: cornerradius is greater than width.")
            return None

        if cornerradius > 0.5*height:
            print("Error: cornerradius is greater than height.")
            return None

        rad = 2*cornerradius
        def shape():
            self.create_polygon((padding,height-cornerradius-padding,padding,cornerradius+padding,padding+cornerradius,padding,width-padding-cornerradius,padding,width-padding,cornerradius+padding,width-padding,height-cornerradius-padding,width-padding-cornerradius,height-padding,padding+cornerradius,height-padding), fill=color, outline=color)
            self.create_arc((padding,padding+rad,padding+rad,padding), start=90, extent=90, fill=color, outline=color)
            self.create_arc((width-padding-rad,padding,width-padding,padding+rad), start=0, extent=90, fill=color, outline=color)
            self.create_arc((width-padding,height-rad-padding,width-padding-rad,height-padding), start=270, extent=90, fill=color, outline=color)
            self.create_arc((padding,height-padding-rad,padding+rad,height-padding), start=180, extent=90, fill=color, outline=color)


        id = shape()
        (x0,y0,x1,y1)  = self.bbox("all")
        width = (x1-x0)
        height = (y1-y0)
        self.configure(width=width, height=height)
        self.bind("<ButtonPress-1>", self._on_press)
        self.bind("<ButtonRelease-1>", self._on_release)

    def _on_press(self, event):
        self.configure(relief="sunken")

    def _on_release(self, event):
        self.configure(relief="raised")
        if self.command is not None:
            self.command()