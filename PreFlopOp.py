import ScreenShot
import GrabTableInfo
import PreFlopTable
import MouseOp
import JudgStatus

import random
import time
import signal
from enum import Enum

from PIL import Image
from logger import loggers

from pynput.mouse import Button, Controller
import sys

stop = False

def term_sig_handler(signum, frame):
    print('catched singal: %d' % signum)
    stop = True
    sys.exit()

class PlayerStatus(Enum):
    preFlopNoOp = 1
    preFlopWaitingOp = 2

class PreFlopAlgorithm():

    def __init__(self, wpk_mouse):
        self.wpk_mouse = wpk_mouse

    def isPreCall(self, pre_actions):
        if max(pre_actions) == GrabTableInfo.big_blind:
            return True
        else:
            return False

    def isOpen(self, pre_actions, max_bb_num):
        if max(pre_actions) / GrabTableInfo.big_blind <= max_bb_num:
            return True
        else:
            return False

    def do_self_action(self, pre_actions, cards_type, button_loc):
        # 判断此时该谁action
        max_num = max(pre_actions)
        if max_num <= 0 :
            loggers.debug("not in preflop")
            return

        # straddle 不在玩的范围内时，前面有人open直接丢
        if button_loc == 5 and (cards_type not in PreFlopTable.preFlopCardTable) and max_num > GrabTableInfo.big_blind:
            loggers.debug("fold when straddle meet open")    
            self.wpk_mouse.Flod()
            return

        action_loc = -1
        # 若自己不是straddle，且自身chip放入最大，则一定当前不是自己的操作顺序
        if max_num == pre_actions[0] and button_loc != 5:
            loggers.info("not my turn")
            return

        # 判断当前是谁操作
        i = len(pre_actions) - 1
        while i >= 0:
            if max_num == pre_actions[i]:
                break
            i -= 1

        i += 1
        while i <= 7 :
            if pre_actions[i] == -1:
                i += 1
                continue
            else:
                break

        action_loc = i % 8
        loggers.debug("{0} need action".format(action_loc))

        if action_loc != 0:
            return

        # 判断是否前面全 Flod / Call
        if self.isPreCall(pre_actions):
            loggers.debug("pre all Flod or Call")
            
            # 前面没有Open, 在 straddle位置，直接call
            if cards_type not in PreFlopTable.preFlopCardTable:
                loggers.debug("straddle call")
                self.wpk_mouse.Call()
                return

            # 根据牌型做出操作
            status = PreFlopTable.preFlopCardTable[cards_type]
            if status == PreFlopTable.PreOp.potBet:
                loggers.debug("1 pot bet")
                self.wpk_mouse.Open("1")
            elif status < PreFlopTable.PreOp.justSpecailLoc:
                loggers.debug("2/3 pot bet")
                self.wpk_mouse.Open("2/3")
            elif status == PreFlopTable.PreOp.justSpecailLoc:
                if button_loc == 0:
                    loggers.debug("2/3 pot bet")
                    self.wpk_mouse.Open("2/3")
                else:
                    loggers.debug("not in special loc -> Flod")
                    self.wpk_mouse.Flod()
            elif status == PreFlopTable.PreOp.samllPair:
                loggers.debug("call")
                self.wpk_mouse.Call()
            else:
                loggers.debug("Never arrive here")

        # 判断是否是小于5个BB的Open
        elif self.isOpen(pre_actions, 5):
            # straddle位置，牌不在玩的范围内, 就Flod掉
            if cards_type not in PreFlopTable.preFlopCardTable:
                loggers.debug("straddle Flod")
                self.wpk_mouse.Flod()
                return

            status = PreFlopTable.preFlopCardTable[cards_type]

            if status == PreFlopTable.PreOp.potBet:
                loggers.debug("1 pot 3 bet")
                self.wpk_mouse.Open("1")
            elif status <= PreFlopTable.PreOp.notCall3Bet:
                loggers.debug("2/3 pot 3 bet")
                self.wpk_mouse.Open("2/3")
            elif status == PreFlopTable.PreOp.callOpen or status == PreFlopTable.PreOp.samllPair: 
                loggers.debug("call open")
                self.wpk_mouse.Call()
            elif status == PreFlopTable.PreOp.justSpecailLoc:
                # 只在庄和大盲位置玩部分牌
                if button_loc == 5 or button_loc == 0:
                    loggers.debug("call open")
                    self.wpk_mouse.Call()
                else:
                    loggers.debug("not play justSpecailLoc when not in button or blind")
                    self.wpk_mouse.Flod()
            elif status == PreFlopTable.PreOp.notCallOpen:
                loggers.debug("not call open Flod")
                self.wpk_mouse.Flod()
            else:
                loggers.debug("never arrive here for deal open")


if __name__ == "__main__":
    signal.signal(signal.SIGTERM, term_sig_handler)   #kill pid
    signal.signal(signal.SIGINT, term_sig_handler)     #ctrl -c
    change_after_shot = (600,500)
    screenShot = ScreenShot.ScreenShot()
    grabTableInfo = GrabTableInfo.GrabTableInfo(GrabTableInfo.wpk_pixel_info) 
    wpkMouseOp = MouseOp.WpkMouse(change_after_shot)
    judgStatus = JudgStatus.JudgeStatus()
    preFlopAlgorithm = PreFlopAlgorithm(wpkMouseOp)
    
    playerStatus = PlayerStatus.preFlopNoOp

    try_time = 1

    while try_time > 0:
        if stop:
            break
        sleep_time = random.randint(1, 2)
        time.sleep(sleep_time)
        cur_time = time.time()
        save_file = "images/cur_test_{0}".format(cur_time)

        # 屏幕截图
        pic_loc = {"top": 380, "left": 1560, "width": 720, "height": 1330}
        screenShot.shot(save_file, pic_loc)
        save_file = "images\cur_test_1613848034.6979752"

        image = Image.open(save_file + ".png")

        # 获取button位置
        button_loc = grabTableInfo.get_button_loc(image)
        loggers.info("button_loc: {0}".format(button_loc))

        # 获取手牌
        cards, colors = grabTableInfo.get_self_card(image)
        if len(cards) == 0:
            continue
        cards_type = grabTableInfo.get_self_cards_type(cards, colors)

        # 获取当前牌桌动作
        preFlopAction = []
        for i in range(0, 8):
            preFlopAction.append(grabTableInfo.get_player_info(image, i))
        loggers.debug("preFlopAction: {0}".format(preFlopAction))

        # 获取公共牌
        public_cards, public_colors = grabTableInfo.get_public_card(image)
        if len(public_cards) > 0:
            loggers.info("public card: {0}".format(str(public_cards)))
            loggers.info("public colors: {0}".format(str(public_colors)))

        if judgStatus.isPreFlop(cards, public_cards):
            # 判断是否翻前弃牌
            loggers.info("card type is: {0}".format(cards_type))
            if cards_type not in PreFlopTable.preFlopCardTable and button_loc != 5:
                loggers.info("flod")
                wpkMouseOp.Flod()
                playerStatus = PlayerStatus.preFlopNoOp
            else:
                loggers.info("play")
                preFlopAlgorithm.do_self_action(preFlopAction, cards_type, button_loc)