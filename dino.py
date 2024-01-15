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
score = 0
is_on_ground = True

# Colors
dino_color = graphics.Color(255, 0, 0)  # Red
obstacle_color = graphics.Color(0, 255, 0)  # Green

def draw_dino(canvas):
    canvas.SetPixel(dino_pos[1], dino_pos[0], dino_color.red, dino_color.green, dino_color.blue)

def draw_obstacles(canvas):
    for obstacle in obstacles:
        canvas.SetPixel(obstacle[1], obstacle[0], obstacle_color.red, obstacle_color.green, obstacle_color.blue)

def update_obstacles():
    # This function now only spawns new obstacles
    while True:
        sleep_time = random.uniform(1.0, 2.0)
        sleep(sleep_time)
        obstacles.append([14, 31])  # Spawn new obstacle at the right edge

def read_keyboard_input():
    while True:
        char = getch.getch()
        if char.lower() == ' ':
            jump_thread = threading.Thread(target=perform_jump)
            jump_thread.start()

# Modify the perform_jump function
def perform_jump():
    global is_on_ground
    if is_on_ground:
        is_on_ground = False
        # Ascent with decreasing sleep time (faster movement)
        ascent_intervals = [0.1, 0.08, 0.05, 0.03, 0.01]
        for interval in ascent_intervals:
            dino_pos[0] -= 1
            sleep(interval)

        # Descent with increasing sleep time (faster movement)
        descent_intervals = [0.01, 0.03, 0.05, 0.08, 0.1]
        for interval in descent_intervals:
            dino_pos[0] += 1
            sleep(interval)

        is_on_ground = True


def draw_score(canvas):
    global score
    score_str = str(score)
    
    # Load the font from the correct path
    font = graphics.Font()
    font.LoadFont("/home/esk/rpi-rgb-led-matrix/fonts/6x10.bdf")
    
    textColor = graphics.Color(255, 255, 0)  # Bright yellow color for visibility
    x_pos = options.cols - len(score_str) * 8  # Adjust x_pos based on score length
    y_pos = 9  # Set y_pos to a value within the upper area of the matrix

    graphics.DrawText(canvas, font, x_pos, y_pos, textColor, score_str)


input_thread = threading.Thread(target=read_keyboard_input)
input_thread.daemon = True  # Daemonize thread
input_thread.start()

obstacle_thread = threading.Thread(target=update_obstacles)
obstacle_thread.daemon = True
obstacle_thread.start()

try:
    while True:
        # Move obstacles to the left
        for obstacle in obstacles:
            obstacle[1] -= 1  # Move each obstacle left

        # Remove obstacles that have left the screen
        obstacles = [obstacle for obstacle in obstacles if obstacle[1] >= 0]

         # Check for game over conditions
        if [dino_pos[0], dino_pos[1]] in obstacles:
            break  # Dino hits an obstacle

        # Check for game over conditions
        if [dino_pos[0], dino_pos[1]] in obstacles:
            break  # Dino hits an obstacle

        for obstacle in obstacles:
            if obstacle[1] == dino_pos[1] - 1 and dino_pos[0] < 14:
                score += 1  # Increment score when dino jumps over an obstacle
                print(f'Score: {score}')


        # Rendering
        canvas = matrix.CreateFrameCanvas()
        draw_dino(canvas)
        draw_obstacles(canvas)
        draw_score(canvas)  # Draw the score
        canvas = matrix.SwapOnVSync(canvas)

        sleep(0.06)  # Control game speed

except KeyboardInterrupt:
    print("Game stopped by user")
except Exception as e:
    print("An error occurred:", e)
finally:
    print("Exiting game...")
