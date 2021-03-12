import tkinter as tk
from _tkinter import TclError
from PIL import Image
from utils import M2ContextMenu, nocommand, current_intersections

if __name__ == '__main__':

    line_x = line_y = 0

    root = tk.Tk()
    root.title("DJ stra - Dijkstra's Algorithm")

    canvas = tk.Canvas(root, width=700, height=700)
    canvas.grid(row=0, column=0)

    intersection_image = tk.PhotoImage(file='images/circlesmall.gif')
    img_width, img_height = Image.open('images/circlesmall.gif').size
    img_width /= 2
    img_height /= 2

    def new_intersection(event):
        intersection = tk.Button(root, image=intersection_image, command=nocommand, borderwidth=0)
        intersection.place(x=event.x - img_width, y=event.y - img_height)
        current_intersections.add(intersection)

    def drawline(event):
        """ Function to run when drawing a line and moving the mouse. Should destroy any old lines, and place a new one. """
        # Could potentially have issues when the UID of the new line wraps around the integer limit.
        if not isinstance(event.widget, tk.Button):
            lines = canvas.create_line(line_x, line_y, event.x, event.y, fill='black', width=10)
            canvas.delete(lines-1)

    def m1click(event):
        """ Will be used to place and create intersections and connections """
        if isinstance(event.widget, tk.Button):
            global line_x
            global line_y
            info = event.widget.place_info()
            line_x = int(info['x']) + img_width
            line_y = int(info['y']) + img_height
            print(line_x, line_y)
            root.bind('<Motion>', drawline)
        else:
            try:  # Stop drawing; if we're currently drawing.
                root.unbind('<Motion>', 'drawline')
                print('tried')
            except TclError:  # Otherwise; create a new button where the mouse was clicked.
                new_intersection(event)


    def m2click(event):
        """ Will be used to show contextual actions based on what object was clicked """
        # Our right click context menu
        m2contextmenu = M2ContextMenu(root, bg="#AAAAAA")

        if isinstance(event.widget, tk.Button):
            m2contextmenu.insert_command(0, label="Remove intersection", command=nocommand)
        else:
            m2contextmenu.insert_command(0, label="Add intersection", command=lambda: new_intersection(event))

        m2contextmenu.tk_popup(event.x_root, event.y_root)

    root.bind("<Button 1>", m1click)
    root.bind("<Button 3>", m2click)

    root.mainloop()
