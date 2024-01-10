import ADC0834
from rgbmatrix import RGBMatrix, RGBMatrixOptions, graphics
from time import sleep
import random

# Matrix configuration
options = RGBMatrixOptions()
options.rows = 16
options.cols = 32
options.chain_length = 1
options.parallel = 1
options.hardware_mapping = 'regular'
matrix = RGBMatrix(options=options)

ADC0834.setup()

# Game setup
snake = [(1, 3), (1, 4), (1, 5)]
direction = "RIGHT"
food_pos = (random.randint(0, 15), random.randint(0, 31))

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

def get_joystick_direction():
    x = ADC0834.getResult(0)  # Assuming the X-axis of the joystick is on channel 0
    y = ADC0834.getResult(1)  # Assuming the Y-axis of the joystick is on channel 1

    # Map the analog values to directions
    # You might need to adjust the threshold values according to your joystick's characteristics
    if x > 200:
        return "RIGHT"
    elif x < 100:
        return "LEFT"
    elif y > 200:
        return "DOWN"
    elif y < 100:
        return "UP"
    else:
        return None  # No significant movement

while True:
    
    joystick_direction = get_joystick_direction()
    if joystick_direction:
        direction = joystick_direction

    # Update snake position
    head = snake[0]
    if direction == "RIGHT":
        head = (head[0], head[1] + 1)
    elif direction == "LEFT":
        head = (head[0], head[1] - 1)
    elif direction == "UP":
        head = (head[0] - 1, head[1])
    elif direction == "DOWN":
        head = (head[0] + 1, head[1])

    # Check for game over conditions
    if not (0 <= head[0] < 16 and 0 <= head[1] < 32) or head in snake:
        break  # Snake hits the wall or itself

    snake.insert(0, head)

    # Check for food collision
    if head == food_pos:
        update_food_position()  # Place new food
    else:
        snake.pop()  # Move the snake

    # Rendering
    canvas = matrix.CreateFrameCanvas()
    draw_snake(canvas)
    draw_food(canvas)
    canvas = matrix.SwapOnVSync(canvas)

    sleep(0.1)  # Control game speed

ADC0834.destroy()