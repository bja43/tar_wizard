import tkinter as tk

def on_circle_click(event):
    global is_dragging, start_x, start_y
    is_dragging = True
    start_x, start_y = event.x, event.y

def on_circle_release(event):
    global is_dragging
    is_dragging = False

def on_circle_motion(event):
    global is_dragging, start_x, start_y
    if is_dragging:
        dx = event.x - start_x
        dy = event.y - start_y
        canvas.move(circle, dx, dy)
        start_x, start_y = event.x, event.y  # Initialize start_x and start_y here

# Initialize tkinter
root = tk.Tk()
root.title("Draggable Circle")

# Create a canvas
canvas = tk.Canvas(root, width=400, height=400)
canvas.pack()

# Draw the circle
circle_x, circle_y = 200, 200
circle_radius = 50
circle = canvas.create_oval(
    circle_x - circle_radius, circle_y - circle_radius,
    circle_x + circle_radius, circle_y + circle_radius,
    fill='gray'
)

# Variables to track dragging status
is_dragging = False
start_x, start_y = 0, 0  # Initialize start_x and start_y here

# Bind mouse events to the functions
canvas.tag_bind(circle, "<ButtonPress-1>", on_circle_click)
canvas.tag_bind(circle, "<ButtonRelease-1>", on_circle_release)
canvas.tag_bind(circle, "<B1-Motion>", on_circle_motion)

# Start the main event loop
root.mainloop()

