import ScreenShot
import GrabTableInfo
import PreFlopTable
import MouseOp

from PIL import Image
from logger import loggers

from pynput.mouse import Button, Controller

if __name__ == "__main__":
    save_file = "cur_test"

    screenShot = ScreenShot.ScreenShot()
    grabTableInfo = GrabTableInfo.GrabTableInfo(GrabTableInfo.wpk_pixel_info) 
    wpkMouseOp = MouseOp.WpkMouse()
    
    # 屏幕截图
    pic_loc = {"top": 380, "left": 1560, "width": 720, "height": 1330}
    screenShot.shot(save_file, pic_loc)

    # 获取手牌
    image = Image.open(save_file + ".png")
    cards, colors = grabTableInfo.get_self_card(image, False)
    cards_type = grabTableInfo.get_self_cards_type(cards, colors)

    # 判断是否翻前弃牌
    loggers.info("card type is: {0}".format(cards_type))
    if cards_type not in PreFlopTable.preFlopCardTable:
        loggers.info("flod")
        wpkMouseOp.Flod((600, 500))
        wpkMouseOp.PrintCoor()
    else:
        loggers.info("play")
        loggers.info("play type:{0}".format(PreFlopTable.preFlopCardTable[cards_type]))
    
    public_cards, public_colors = grabTableInfo.get_public_card(image, False)
    loggers.info(str(public_cards))
    loggers.info(str(public_colors))

    mouse = Controller()
    mouse.position = (1145 + 600 + 1800, 980 +500 + 400)
    mouse.click(Button.left, 1)