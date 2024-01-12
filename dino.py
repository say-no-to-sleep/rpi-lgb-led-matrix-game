from rgbmatrix import RGBMatrix, RGBMatrixOptions, graphics
from time import sleep
import random
import getch  # Import the getch module
import threading

# Matrix configuration
options = RGBMatrixOptions()
options.rows = 16
options.cols = 32
options.chain_length = 1
options.parallel = 1
options.hardware_mapping = 'regular'
matrix = RGBMatrix(options=options)

# Game setup
dino_pos = [14, 3]  # Initial position of the dino
obstacles = []

# Colors
dino_color = graphics.Color(255, 0, 0)  # Red
obstacle_color = graphics.Color(0, 255, 0)  # Green

def draw_dino(canvas):
    canvas.SetPixel(dino_pos[1], dino_pos[0], dino_color.red, dino_color.green, dino_color.blue)

def draw_obstacles(canvas):
    for obstacle in obstacles:
        canvas.SetPixel(obstacle[1], obstacle[0], obstacle_color.red, obstacle_color.green, obstacle_color.blue)

def update_obstacles():
    while True:
        sleep_time = random.uniform(1.0, 2.0)
        sleep(sleep_time)
        obstacles.append([14, 31])

def read_keyboard_input():
    while True:
        char = getch.getch()  # Get a single character from the keyboard
        if char.lower() == ' ':
            jump_thread = threading.Thread(target=perform_jump)
            jump_thread.start()

def perform_jump():
    for _ in range(5):
        dino_pos[0] -= 1
        sleep(0.1)
    for _ in range(5):
        dino_pos[0] += 1
        sleep(0.1)

input_thread = threading.Thread(target=read_keyboard_input)
input_thread.daemon = True  # Daemonize thread
input_thread.start()

obstacle_thread = threading.Thread(target=update_obstacles)
obstacle_thread.daemon = True
obstacle_thread.start()

try:
    while True:
        # Update dino position
        dino_pos[0] = min(max(dino_pos[0], 0), 14)

        # Remove obstacles that have passed the screen
        obstacles = [obstacle for obstacle in obstacles if obstacle[1] > 0]

        # Generate new obstacles randomly
        if random.random() < 0.1:
            obstacles.append([14, 31])

        # Check for game over conditions
        if [dino_pos[0], dino_pos[1]] in obstacles:
            break  # Dino hits an obstacle

        # Rendering
        canvas = matrix.CreateFrameCanvas()
        draw_dino(canvas)
        draw_obstacles(canvas)
        canvas = matrix.SwapOnVSync(canvas)

        sleep(0.1)  # Control game speed

except KeyboardInterrupt:
    print("Game stopped by user")
except Exception as e:
    print("An error occurred:", e)
finally:
    print("Exiting game...")
