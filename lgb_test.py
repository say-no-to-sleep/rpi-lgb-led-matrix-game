from rgbmatrix import RGBMatrix, RGBMatrixOptions, graphics

# Configuration for the matrix
options = RGBMatrixOptions()
options.rows = 16
options.cols = 32
options.chain_length = 1
options.parallel = 1
options.hardware_mapping = 'regular'  # If you're using an Adafruit hat, use 'adafruit-hat'


matrix = RGBMatrix(options = options)

# Create a canvas to draw on
canvas = matrix.CreateFrameCanvas()

# Define the square properties
square_size = 6
start_x = (canvas.width - square_size) // 2
start_y = (canvas.height - square_size) // 2
color = graphics.Color(255, 0, 0)  # Red color

# Draw a square
for x in range(start_x, start_x + square_size):
    for y in range(start_y, start_y + square_size):
        canvas.SetPixel(x, y, color.red, color.green, color.blue)

# Update the display
canvas = matrix.SwapOnVSync(canvas)

# Keep the square displayed
import time
time.sleep(10)
