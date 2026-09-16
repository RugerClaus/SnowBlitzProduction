import math
def sine(current_time):
    t = current_time / 1000
    pulse = (math.sin(t) + 1) / 2
    return pulse
def load_file(filename):
    with open(filename, "r", encoding="utf-8") as file:
        return file.read()
    