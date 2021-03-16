import tkinter as tk
from info import img_width, img_height, imgpath
from utils import M2ContextMenu, nocommand, current_intersections, current_mouselines, MouseLine, Intersection

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

    def new_intersection(event):
        intersection = Intersection(root, image=intersection_image, borderwidth=0)
        intersection.place(x=event.x - img_width, y=event.y - img_height)
        current_intersections.add(intersection)

    def m1click(event):
        """ Will be used to place and create intersections and connections """
        if isinstance(event.widget, Intersection):
            if not current_mouselines:
                MouseLine(root, canvas, event.widget)
            else:
                intersection = event.widget
                for line in current_mouselines:
                    if line.start_intersection == intersection or intersection.connected_to(line.start_intersection):
                        line.destroy()
                    else:
                        line.lock_n_link(intersection)
        elif current_mouselines:  # Stop drawing; if we're currently drawing.
            for line in current_mouselines:
                line.destroy()
        else:  # Otherwise; create a new button where the mouse was clicked.
            new_intersection(event)


    def m2click(event):
        """ Will be used to show contextual actions based on what object was clicked """
        # Our right click context menu
        m2contextmenu = M2ContextMenu(root, bg="#AAAAAA")

        if isinstance(event.widget, Intersection):
            m2contextmenu.insert_command(0, label="Remove intersection", command=event.widget.destroy)
            m2contextmenu.insert_command(1, label="Remove connections", command=event.widget.destroy_connections)
        else:
            m2contextmenu.insert_command(0, label="Add intersection", command=lambda: new_intersection(event))

        m2contextmenu.tk_popup(event.x_root, event.y_root)

    root.bind("<Button 1>", m1click)
    root.bind("<Button 3>", m2click)

    root.mainloop()
