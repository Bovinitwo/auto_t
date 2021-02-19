import mss
import mss.tools
import datetime

class ScreenShot:
    """截图指定的屏幕部分"""
    def shot(self, filename, pic_loc):
        with mss.mss() as sct:
            # The screen part to capture
            monitor = {"top": pic_loc["top"], "left": pic_loc["left"], "width": pic_loc["width"], "height": pic_loc["height"]}
            output = "{0}.png".format(filename)

            # Grab the data
            sct_img = sct.grab(monitor)

            # Save to the picture file
            mss.tools.to_png(sct_img.rgb, sct_img.size, output=output)

if __name__ == '__main__':
    screenShot = ScreenShot()    
    pic_loc = {"top": 380, "left": 1560, "width": 720, "height": 1330}
    screenShot.shot("cur_test", pic_loc)