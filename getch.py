import sys
import tty
import termios
import atexit

def restore_settings(saved_settings):
    termios.tcsetattr(sys.stdin.fileno(), termios.TCSADRAIN, saved_settings)

def getch():
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setraw(sys.stdin.fileno())
        ch = sys.stdin.read(1)
    finally:
        restore_settings(old_settings)
    return ch

# Restore terminal settings at exit
atexit.register(restore_settings, termios.tcgetattr(sys.stdin.fileno()))
