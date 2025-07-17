import cv2
import numpy as np

# Canvas
canvas = np.ones((500, 600, 3), np.uint8) * 255  # Wider canvas for controls
drawing = False
brush_size = 5
color = (0, 0, 0)
tool = "Brush"
prev_x, prev_y = -1, -1

# Draw function
def draw(event, x, y, flags, param):
    global drawing, prev_x, prev_y

    if x > 500:  # Ignore drawing in control panel area
        return

    if event == cv2.EVENT_LBUTTONDOWN:
        drawing = True
        prev_x, prev_y = x, y
    elif event == cv2.EVENT_MOUSEMOVE and drawing:
        cv2.line(canvas, (prev_x, prev_y), (x, y), color, brush_size)
        prev_x, prev_y = x, y
    elif event == cv2.EVENT_LBUTTONUP:
        drawing = False

# Create trackbars for R, G, B
def nothing(x):
    pass

cv2.namedWindow("Paint App")
cv2.setMouseCallback("Paint App", draw)

# Create a control panel on the right (100px wide)
cv2.createTrackbar("R", "Paint App", 0, 255, nothing)
cv2.createTrackbar("G", "Paint App", 0, 255, nothing)
cv2.createTrackbar("B", "Paint App", 0, 255, nothing)

# Instructions text
def draw_info():
    cv2.rectangle(canvas, (500, 0), (600, 500), (240, 240, 240), -1)
    cv2.putText(canvas, "Tools:", (505, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (50, 50, 50), 1)
    cv2.putText(canvas, "b: Brush", (505, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1)
    cv2.putText(canvas, "e: Eraser", (505, 85), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1)
    cv2.putText(canvas, "c: Clear", (505, 110), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1)
    cv2.putText(canvas, "s: Save", (505, 135), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1)
    cv2.putText(canvas, "+/-: Size", (505, 160), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1)
    cv2.putText(canvas, "q: Quit", (505, 185), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1)

    cv2.putText(canvas, f"Size: {brush_size}", (505, 230), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1)
    cv2.putText(canvas, f"Tool: {tool}", (505, 255), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 100, 200), 1)
    cv2.putText(canvas, f"Color:", (505, 280), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (50, 50, 50), 1)
    cv2.rectangle(canvas, (505, 295), (595, 315), color, -1)

print("🎨 Sliders and instructions are displayed inside the app window.")

# Main loop
while True:
    # Update color from sliders
    r = cv2.getTrackbarPos("R", "Paint App")
    g = cv2.getTrackbarPos("G", "Paint App")
    b = cv2.getTrackbarPos("B", "Paint App")
    color = (b, g, r) if tool == "Brush" else (255, 255, 255)

    draw_info()

    cv2.imshow("Paint App", canvas)
    key = cv2.waitKey(1) & 0xFF

    if key == ord('q'):
        break
    elif key == ord('e'):
        tool = "Eraser"
    elif key == ord('b'):
        tool = "Brush"
    elif key == ord('c'):
        canvas[:, :500] = 255  # clear only the drawing area
    elif key == ord('s'):
        cv2.imwrite("paint_output.png", canvas[:, :500])
        print("✅ Saved as 'paint_output.png'")
    elif key == ord('+') or key == ord('='):
        brush_size = min(brush_size + 1, 50)
    elif key == ord('-'):
        brush_size = max(1, brush_size - 1)

cv2.destroyAllWindows()
