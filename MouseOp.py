from pynput.mouse import Button, Controller
import random
from logger import loggers

class WpkMouse():
    def __init__(self, deviation):
        self.deviation = deviation
        self.flod_range_x = [1145, 1170]
        self.flod_range_y = [980, 1010]
        self.mouse = Controller()

    def Flod(self):
        x = random.randint(self.flod_range_x[0], self.flod_range_x[1]) + self.deviation[0]
        y = random.randint(self.flod_range_y[0], self.flod_range_y[1]) + self.deviation[1]
        self.mouse.position = (x, y)
        #loggers.debug(self.mouse.position)
        self.mouse.click(Button.left, 1)

    def PrintCoor(self):
        loggers.debug(self.mouse.position)
    
    def Open(self, level):
        x = 0
        y = 0
        if level == "1/3":
            x = 1070 + random.randint(5, 10) + self.deviation[0]
            y = 850 + random.randint(5, 10) + self.deviation[1]
            self.mouse.position = (x, y)
        if level == "1/2":
            x = 1190 + random.randint(5, 10) + self.deviation[0]
            y = 810 + random.randint(5, 10) + self.deviation[1]
            self.mouse.position = (x, y)
        elif level == "2/3":
            x = 1310 + random.randint(5, 10) + self.deviation[0]
            y = 800 + random.randint(5, 10) + self.deviation[1]
            self.mouse.position = (x, y)
        elif level == "1":
            x = 1440 + random.randint(5, 10) + self.deviation[0]
            y = 805 + random.randint(5, 10) + self.deviation[1]
            self.mouse.position = (x, y)

        self.mouse.click(Button.left, 1)
    
    def Call(self):
        x = 1500 + random.randint(5, 10) + self.deviation[0]
        y = 1000 + random.randint(5, 10) + self.deviation[1]
        self.mouse.position = (x, y)
        self.mouse.click(Button.left, 1)

if __name__ == '__main__':
    import ScreenShot
    screenShot = ScreenShot.ScreenShot()
    pic_loc = {"top": 380, "left": 1560, "width": 720, "height": 1330}
    screenShot.shot("mouse_test", pic_loc)

    change_after_shot = (600,500)
    wpkMouse = WpkMouse((change_after_shot))
    #wpkMouse.Open("1/2")
    #wpkMouse.Call()