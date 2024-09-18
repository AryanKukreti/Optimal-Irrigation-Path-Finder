import numpy as np
from matplotlib import pyplot as plt

def onclick(event, image_array, starting_point):
    """Callback function for user to select starting point."""
    if event.xdata is not None and event.ydata is not None:
        x, y = int(event.xdata), int(event.ydata)
        if image_array[y, x] < 60:
            print("Sorry, but you can't make the irrigation over the ditch.")
        else:
            starting_point[0] = x
            starting_point[1] = y
            print(f"Selected Starting Point: {starting_point}")
            plt.close()  # Close plot once the point is selected