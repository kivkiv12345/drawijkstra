import tkinter as tk
from _tkinter import TclError
from typing import Set, List, Type
from weakref import WeakSet
from info import img_width, img_height


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
    """ Draws a line from the stored position to that of the mouse. """
    uid: int = None  # Unique ID of the drawn line. Will change whenever end position is updated.

    start_intersection = end_intersection = None  # Connected widgets.
    posX: int = None; posY: int = None  # Origin position of the line.

    root: tk.Tk = None  # Root GUI for the line (needed for bindings).
    canvas: tk.Canvas = None  # Canvas to draw the line upon.

    def __init__(self, root:tk.Tk, canvas:tk.Canvas, intersection:tk.Button) -> None:
        """
        :param root: Root GUI for the line (needed for bindings).
        :param canvas: Canvas to draw the line upon.
        :param intersection: Start intersection of the line.
        """
        self.root, self.canvas, self.start_intersection = root, canvas, intersection

        info = intersection.place_info()
        self.posX, self.posY = int(info['x']) + img_width, int(info['y']) + img_height

        super().__init__()
        current_mouselines.append(self)
        mouselines.add(self)

    def __getitem__(self, intersection:Type[tk.Button]):
        if not self.locked: raise AttributeError(f"{self} must be locked before the opposite intersection may be retrieved.")
        return self._opposite[intersection]

    def update(self, event) -> None:
        """ Update the end position of the line. """
        if not isinstance(event.widget, tk.Button):
            if self.uid: self.canvas.delete(self.uid)  # Delete the outdated line, if it exists.
            self.uid = self.canvas.create_line(self.posX, self.posY, event.x, event.y, fill='black', width=10)

    def destroy(self) -> None:
        """ Unbinds, removes and destroys this line. """

        # Multiple exceptions may occur when the program is closed. These are luckily of little concern to us,
        # if the program is to be closed anyway.
        try: self.canvas.delete(self.uid)  # Delete the outdated line, if it exists.
        except TclError: pass

        try: current_mouselines.remove(self)
        except ValueError: pass

        try: mouselines.remove(self)
        except ValueError: pass

        del self

    def lock_n_link(self, intersection:tk.Button) -> None:
        """ Links and locks the current line between two points. """
        current_mouselines.remove(self)
        self.end_intersection = intersection
        intersection.connections.add(self)
        self.start_intersection.connections.add(self)

        self._opposite = {intersection: self.start_intersection, self.start_intersection: intersection}

        class coords:
            """ Driver class for MouseLine lock_n_link line update. """
            widget = None
            x, y = intersection.winfo_x() + img_width, intersection.winfo_y() + img_height

        self.update(coords())

    @property
    def locked(self):
        """
        :return: True when both ends are linked to intersections, and the line is not tracking the mouse.
        """
        return self.start_intersection and self.end_intersection

    def opposite(self, intersection):
        """
        :param intersection: intersection whose opposite should be returned.
        :return: Returns the intersection at the opposite end of the connection.
        """
        return {self.end_intersection: self.start_intersection, self.start_intersection: self.end_intersection}.get(intersection, None)

    def __str__(self) -> str:
        return f"MouseLine UID{self.uid} [x{self.posX}, y{self.posY}]"


class Intersection(tk.Button):
    connections: Set[MouseLine] = None  # Stores all MouseLines currently connected to this intersection.

    def __init__(self, master=None, cnf={}, **kw):
        self.connections = WeakSet()  # Connections must be declared as an instance attribute, to avoid it being static.
        super().__init__(master, cnf, **kw)

    def destroy(self):
        """ Destroy this intersection, its descendant widgets and connected MouseLines. """
        for line in self.connections:
            line.destroy()
        super().destroy()

    def destroy_connections(self) -> None:
        destroy_all(self.connections)

    def connected_to(self, intersection):
        """
        :param intersection: The intersection to compare against.
        :return: Returns a boolean based on whether a connection exists between the two intersections.
        """
        return bool(self.connections.intersection(intersection.connections))


current_intersections: Set[Intersection] = set()  # Used to store all placed intersections
current_mouselines: List[MouseLine] = []  # List of all mouselines currently being drawn.
mouselines: Set[MouseLine] = set()  # Set of all placed connectors
