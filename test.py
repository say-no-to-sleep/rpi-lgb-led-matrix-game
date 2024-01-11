from rgbmatrix import RGBMatrix, RGBMatrixOptions, graphics
import getch
import threading
import time
import random

# Matrix configuration
options = RGBMatrixOptions()
options.rows = 16
options.cols = 32
options.chain_length = 1
options.parallel = 1
options.hardware_mapping = 'regular'
matrix = RGBMatrix(options=options)


# Game setup
snake = [(1, 3), (1, 4), (1, 5)]
food_pos = (random.randint(0, 15), random.randint(0, 31))
direction = "RIGHT"  # Initial direction
input_direction = "RIGHT"  # Direction based on keyboard input

# Gradient colors
start_color = graphics.Color(255, 0, 0)  # Red
end_color = graphics.Color(0, 0, 255)    # Blue

# Food color
food_color = graphics.Color(255, 255, 0)  # Yellow

def interpolate_color(start_color, end_color, ratio):
    new_red = int(start_color.red * (1 - ratio) + end_color.red * ratio)
    new_green = int(start_color.green * (1 - ratio) + end_color.green * ratio)
    new_blue = int(start_color.blue * (1 - ratio) + end_color.blue * ratio)
    return graphics.Color(new_red, new_green, new_blue)

def draw_snake(canvas):
    snake_length = len(snake)
    for i, segment in enumerate(snake):
        ratio = i / snake_length
        color = interpolate_color(start_color, end_color, ratio)
        canvas.SetPixel(segment[1], segment[0], color.red, color.green, color.blue)

def draw_food(canvas):
    canvas.SetPixel(food_pos[1], food_pos[0], food_color.red, food_color.green, food_color.blue)

def update_food_position():
    global food_pos
    while True:
        new_food_pos = (random.randint(0, 15), random.randint(0, 31))
        if new_food_pos not in snake:
            food_pos = new_food_pos
            break

def read_keyboard_input():
    global input_direction
    while True:
        char = getch.getch()  # Get a single character from keyboard
        if char.lower() == 'w':
            input_direction = "UP"
        elif char.lower() == 'a':
            input_direction = "LEFT"
        elif char.lower() == 's':
            input_direction = "DOWN"
        elif char.lower() == 'd':
            input_direction = "RIGHT"

input_thread = threading.Thread(target=read_keyboard_input)
input_thread.daemon = True  # Daemonize thread
input_thread.start()

direction = "RIGHT"  # Set an initial direction
input_direction = direction  # Synchronize input direction with initial direction

while True:
    print(f"Current direction: {direction}, Input direction: {input_direction}")

    direction = input_direction

    # Update snake position
    head = snake[0]
    print(f"Current head position: {head}")
    
    if direction == "RIGHT":
        head = (head[0], head[1] + 1)
    elif direction == "LEFT":
        head = (head[0], head[1] - 1)
    elif direction == "UP":
        head = (head[0] - 1, head[1])
    elif direction == "DOWN":
        head = (head[0] + 1, head[1])

    print(f"New head position: {head}")

    # Check for game over conditions
    if not (0 <= head[0] < 16 and 0 <= head[1] < 32):
        print("Game over condition met")
        break  # Snake hits the wall or itself

    snake.insert(0, head)

    # Check for food collision
    if head == food_pos:
        print("Food collision")
        update_food_position()  # Place new food
    else:
        snake.pop()  # Move the snake

    # Rendering
    canvas = matrix.CreateFrameCanvas()
    draw_snake(canvas)
    draw_food(canvas)
    canvas = matrix.SwapOnVSync(canvas)

    time.sleep(0.2)  # Control game speed