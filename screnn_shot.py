import mss
import mss.tools
import datetime

class ScreenShot:
    """截图指定的屏幕部分"""
    def shot(self, filename):
        with mss.mss() as sct:
            # The screen part to capture
            monitor = {"top": 0, "left": 0, "width": 720, "height": 1330}
            output = "{0}.png".format(filename)

            # Grab the data
            sct_img = sct.grab(monitor)

            # Save to the picture file
            mss.tools.to_png(sct_img.rgb, sct_img.size, output=output)
            print(output)

if __name__ == '__main__':
    screenShot = ScreenShot();    
    screenShot.shot("cur_test")