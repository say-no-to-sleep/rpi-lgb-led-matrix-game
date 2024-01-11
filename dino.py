# keyboard_input.py
import getch

print("Press a key (WASD for direction, Q to quit):")

while True:
    char = getch.getch()

    if char.lower() == 'w':
        print("Up")
    elif char.lower() == 'a':
        print("Left")
    elif char.lower() == 's':
        print("Down")
    elif char.lower() == 'd':
        print("Right")
    elif char.lower() == 'q':
        print("Quitting")
        break
    else:
        print("Unknown key:", char)
