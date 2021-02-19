import ScreenShot
import GrabTableInfo
import PreFlopTable
import MouseOp
import JudgStatus

import time
import signal
from enum import Enum

from PIL import Image
from logger import loggers

from pynput.mouse import Button, Controller

stop = False

def term_sig_handler(signum, frame):
    print('catched singal: %d' % signum)
    stop = True

class PlayerStatus(Enum):
    preFlopNoOp = 1
    preFlopWaitingOp = 2

if __name__ == "__main__":
    signal.signal(signal.SIGTERM, term_sig_handler)   #kill pid
    signal.signal(signal.SIGINT, term_sig_handler)     #ctrl -c
    screenShot = ScreenShot.ScreenShot()
    grabTableInfo = GrabTableInfo.GrabTableInfo(GrabTableInfo.wpk_pixel_info) 
    wpkMouseOp = MouseOp.WpkMouse()
    judgStatus = JudgStatus.JudgeStatus()
    change_after_shot = (600,500)
    
    try_time = 30 
    playerStatus = PlayerStatus.preFlopNoOp

    while try_time > 0:
        if stop:
            break
        time.sleep(2.5)
        cur_time = time.time()
        save_file = "images/cur_test_{0}".format(cur_time)

        # 屏幕截图
        pic_loc = {"top": 380, "left": 1560, "width": 720, "height": 1330}
        screenShot.shot(save_file, pic_loc)

        # 获取手牌
        image = Image.open(save_file + ".png")
        cards, colors = grabTableInfo.get_self_card(image, False)
        cards_type = grabTableInfo.get_self_cards_type(cards, colors)

        # 获取公共牌
        public_cards, public_colors = grabTableInfo.get_public_card(image, False)
        loggers.info(str(public_cards))
        loggers.info(str(public_colors))

        # 获取自身状态
        action = grabTableInfo.get_self_action(image)
        if action == "straddle":                    
            playerStatus = PlayerStatus.preFlopWaitingOp

        if judgStatus.isPreFlop(cards, public_cards):
            # 判断是否翻前弃牌
            loggers.info("card type is: {0}".format(cards_type))
            if cards_type not in PreFlopTable.preFlopCardTable and playerStatus == PlayerStatus.preFlopNoOp:
                loggers.info("flod")
                wpkMouseOp.Flod(change_after_shot)
                playerStatus = PlayerStatus.preFlopNoOp
            else:
                loggers.info("play")