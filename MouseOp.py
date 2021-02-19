from pynput.mouse import Button, Controller
import random
from logger import loggers

class WpkMouse():
    def __init__(self):
        self.flod_range_x = [1145, 1170]
        self.flod_range_y = [980, 1010]
        self.mouse = Controller()

    def Flod(self, deviation):
        x = random.randint(self.flod_range_x[0], self.flod_range_x[1]) + deviation[0]
        y = random.randint(self.flod_range_y[0], self.flod_range_y[1]) + deviation[1]
        self.mouse.position = (x, y)
        loggers.debug(self.mouse.position)
        self.mouse.click(Button.left, 1)
    def PrintCoor(self):
        loggers.debug(self.mouse.position)
    

if __name__ == '__main__':
    wpkMouse = WpkMouse()
    wpkMouse.Flod()