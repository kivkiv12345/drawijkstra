import tkinter as tk
from keymodes import KeyModes
from info import img_width, img_height, imgpath
from utils import M2ContextMenu, nocommand, current_intersections, current_mouselines, MouseLine, Intersection, \
    destroy_all

if __name__ == '__main__':

    root = tk.Tk()
    root.title("Drawijkstra - Dijkstra's Algorithm")

    canvas = tk.Canvas(root, width=700, height=700)
    canvas.grid(row=0, column=0)

    intersection_image = tk.PhotoImage(file=imgpath)

    def lineupdate(event):
        for line in current_mouselines:
            line.update(event)

    root.bind('<Motion>', lineupdate)

    def new_intersection(event, locklines=False) -> Intersection:
        """
        Places a new intersection at the specified location.
        :param event: Event with coordinates for the new intersection.
        :param locklines: Whether current mouselines should lock to the new intersection.
        :return: Returns the created intersection.
        """
        intersection = Intersection(root, image=intersection_image, borderwidth=0)
        intersection.place(x=event.x - img_width, y=event.y - img_height)
        current_intersections.add(intersection)
        if locklines:
            for line in current_mouselines:
                line.lock_n_link(intersection, (event.x, event.y))
        return intersection


    def m1click(event, mode:KeyModes=None):
        """ Will be used to place and create intersections and connections """

        target = event.widget
        if isinstance(target, Intersection):
            if not current_mouselines:
                if mode == KeyModes.CONTROL: target.destroy()
                else: MouseLine(root, canvas, target)
            else:
                if mode == KeyModes.CONTROL:
                    for line in current_mouselines:
                        target.disconnect(line.start_intersection)
                    destroy_all(current_mouselines)
                else:
                    for line in current_mouselines:
                        if line.start_intersection == target or target.connected_to(line.start_intersection):
                            line.destroy()
                        else:
                            line.lock_n_link(target)
                    if mode == KeyModes.SHIFT: MouseLine(root, canvas, target)
        elif current_mouselines and not mode:  # Stop drawing; if we're currently drawing.
            for line in current_mouselines:
                line.destroy()
        else:  # Otherwise; create a new button where the mouse was clicked.
            newi = new_intersection(event, mode==KeyModes.SHIFT)
            if mode in {KeyModes.SHIFT, KeyModes.ALT}: MouseLine(root, canvas, newi)


    def m2click(event):
        """ Shows contextual actions based on what object was clicked """
        # Create an easily adaptable right click context menu whenever we right click.
        m2contextmenu = M2ContextMenu(root, bg="#AAAAAA")

        target = event.widget
        if isinstance(target, Intersection):  # What should be shown when right clicking on an intersection.
            m2contextmenu.insert_command(0, label="Remove intersection", command=target.destroy)
            if target.connections: m2contextmenu.insert_command(1, label="Remove connections", command=target.destroy_connections)
        else:  # What should be shown when right clicking on empty space on the canvas.
            m2contextmenu.insert_command(0, label="Add intersection", command=lambda: new_intersection(event, bool(current_mouselines)))

        m2contextmenu.tk_popup(event.x_root, event.y_root)

    root.bind("<Button 1>", m1click)
    root.bind("<Button 3>", m2click)

    # Bind some event modifiers, these alter the behavior when clicking the mouse.
    root.bind('<Shift-Button-1>', lambda event: m1click(event, KeyModes.SHIFT))
    root.bind('<Control-Button-1>', lambda event: m1click(event, KeyModes.CONTROL))
    root.bind('<Alt-Button-1>', lambda event: m1click(event, KeyModes.ALT))

    root.mainloop()
