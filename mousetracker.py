from pynput import mouse

# Callback function to handle mouse movement
def on_move(x, y):
    print(f"Mouse moved to ({x}, {y})")

# Callback function to handle mouse clicks
def on_click(x, y, button, pressed):
    if pressed:
        print(f"Mouse clicked at ({x}, {y}) with {button}")
    else:
        print(f"Mouse released at ({x}, {y}) with {button}")

# Callback function to handle mouse scroll
def on_scroll(x, y, dx, dy):
    print(f"Mouse scrolled at ({x}, {y}) with delta ({dx}, {dy})")

# Start the listener
with mouse.Listener(on_move=on_move, on_click=on_click, on_scroll=on_scroll) as listener:
    print("Mouse tracker is running. Press Ctrl+C to exit.")
    listener.join()
