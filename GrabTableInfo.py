from PIL import Image
import pytesseract
from logger import loggers

wpk_pixel_info = {
   "card_width": 80,          #牌宽
   "card_len": 70,            #牌高

   "self_left_start": 285,    #自己的牌的左起始点
   "self_top_start": 1220,    #自己的牌的上起始点

   "public_left_start": 155,  #公共牌左起始
   "public_top_start": 710,   #公共牌上部分起始

   # 自身筹码
   "chip_left_start": 310,    #自己的筹码标志位置
   "chip_top_start": 1138,
   "chip_width": 100,
   "chip_len": 27,

   # 自身action
   "self_action_left_start": 220,
   "self_action_top_start": 1020,
   "action_width": 95,
   "action_len": 30,

   # 底池
   "pot_left": 325,
   "pot_top": 530,
   "pot_width": 100,
   "pot_len": 30,

   # 跟注按钮信息
   "call_left_start": 480,
   "call_top_start": 1080,
   "call_width": 120,
   "call_len": 100,

   # button loc
   "button_width": 50,
   "button_len": 50,

   "button_0_left": 250,
   "button_0_top": 1100,

   "button_1_left": 130,
   "button_1_top": 900,

   "button_2_left": 110,
   "button_2_top": 690,

   "button_3_left": 130,
   "button_3_top": 440,

   "button_4_left": 420,
   "button_4_top": 290,

   "button_5_left": 540,
   "button_5_top": 440,

   "button_6_left": 580,
   "button_6_top": 690,

   "button_7_left": 540,
   "button_7_top": 900,

   "players_fold_coor": {
      "1": [35, 830, 80, 50],
      "2": [35, 580, 80, 50],
      "3": [35, 360, 80, 50],
      "4": [325, 220, 80, 50],
      "5": [610, 360, 80, 50],
      "6": [610, 580, 80, 50],
      "7": [610, 830, 80, 50],
   },


   "players_chip_coor":{
      "0":[410, 1045, 110, 30],
      "1": [142, 875, 70, 40],
      "2": [142, 625, 70, 40],
      "3": [142, 402, 70, 40],
      "4": [330, 380, 70, 40],
      "5": [512, 402, 70, 40],
      "6": [512, 625, 70, 40],
      "7": [512, 875, 70, 40],
   },

   "player_left_chip":{
      "0":[310, 1140, 100, 30],
      "1": [30, 915, 100, 30],
      "2": [30, 665, 100, 30],
      "3": [30, 441, 100, 30],
      "4": [310, 310, 100, 30],
      "5": [597, 441, 100, 30],
      "6": [597, 665, 100, 30],
      "7": [597, 915, 100, 30],
   }
}

big_blind = 1.0

table_2 = []

class GrabTableInfo:
   # 获取选手信息
   def __init__(self, pixel_info):
      self.pixel_info = pixel_info 

   def image_to_2(self, image, shreshold):
      image_l = image.convert('L')
      table = []
      for i in range(256):
         if i < shreshold:
            table.append(1)
         else:
            table.append(0)
      return image_l.point(table, '1')

   def isButton(self, image, box):
      count = 0
      for i in range(box[0], box[2]):
         for j in range(box[1], box[3]):
            pixel = image.getpixel((i, j))
            if pixel[0] > 200 and pixel[1] > 200 and pixel[2] > 200:
               count += 1
      if count > 300:
         return True

   # 获取一个玩家的行动信息: Flod/Call/Raise
   def get_player_info(self, image, loc, debug = False):
      if self.isFold(image, loc, debug):
         if debug:
            loggers.debug("{0} Flod".format(loc))
         return -1
      else:
         chip_num = self.get_player_put_chip(image, loc, debug) / big_blind
         if debug:
            loggers.debug("{0} put chip {1}".format(loc, chip_num))
         return chip_num
         

   # 获取玩家放下的筹码
   def get_player_put_chip(self, image, loc, debug = False):
      ls = self.pixel_info["players_chip_coor"][str(loc)][0]
      ts = self.pixel_info["players_chip_coor"][str(loc)][1]
      width = self.pixel_info["players_chip_coor"][str(loc)][2]
      height = self.pixel_info["players_chip_coor"][str(loc)][3]
      box = (ls, ts, ls + width , ts + height)
      image_for_flod = image.crop(box)
      image_for_flod = self.image_to_2(image_for_flod, 160)

      if debug:
         image_for_flod.show()

      content = pytesseract.image_to_string(image_for_flod, config="-psm 10000").strip()
      if debug:
         loggers.debug("{0} get_player_put_chip raw chip: {1}".format(loc, content))

      content = content.replace("I", "1", 10)
      content = content.replace("l", "1", 10)
      num = "".join(filter(lambda ch: ch in '0123456789.', content))

      try:
         result = float(num)
         return result
      except:
         return 0
      
   # 获取玩家剩余筹码
   def get_player_left_chip(self, image, loc, debug = False):
      ls = self.pixel_info["player_left_chip"][str(loc)][0]
      ts = self.pixel_info["player_left_chip"][str(loc)][1]
      width = self.pixel_info["player_left_chip"][str(loc)][2]
      height = self.pixel_info["player_left_chip"][str(loc)][3]
      box = (ls, ts, ls + width, ts + height)
      image_for_flod = image.crop(box)
      image_for_flod = self.image_to_2(image_for_flod, 210)

      if debug:
         image_for_flod.show()

      content = pytesseract.image_to_string(image_for_flod, config="-psm 10000").strip()
      if debug:
         loggers.debug("{0} get_player_left_chip raw chip: {1}".format(loc, content))

      content = content.replace("I", "1", 10)
      content = content.replace("l", "1", 10)
      content = content.replace("Z", "2", 10)
      content = content.replace("O", "0", 10)
      num = "".join(filter(lambda ch: ch in '0123456789.', content))

      if debug:
         loggers.debug("{0} get_player_left_chip raw chip: {1}".format(loc, content))

      try:
         result = float(num)
         return result
      except:
         return 0

   # 确认当前玩家是否Flod
   def isFold(self, image, loc, debug = False):
      if loc == 0:
         return False
      ls = self.pixel_info["players_fold_coor"][str(loc)][0]
      ts = self.pixel_info["players_fold_coor"][str(loc)][1]
      width = self.pixel_info["players_fold_coor"][str(loc)][2]
      hight = self.pixel_info["players_fold_coor"][str(loc)][3]
      box = (ls, ts, ls + width , ts + hight)
      image_for_flod = image.crop(box)
      image_for_flod = self.image_to_2(image_for_flod, 180)
      
      if debug:
         image_for_flod.show()

      content = pytesseract.image_to_string(image_for_flod, config='-psm 100').strip()

      if debug:
         loggers.debug("{0} raw Fold info: {1}".format(loc, content))

      if "F" in content and 'd' in content :
         return True

   # 找到button位置
   def get_button_loc(self, image, debug = False):
      ls = self.pixel_info["button_0_left"]
      ts = self.pixel_info["button_0_top"]
      box = (ls, ts, ls + self.pixel_info["button_width"] , ts + self.pixel_info["button_len"])
      if debug:
         image_for_num = image.crop(box)
         image_for_num.show()

      if self.isButton(image, box):
         return 0
      
      ls = self.pixel_info["button_1_left"]
      ts = self.pixel_info["button_1_top"]
      box = (ls, ts, ls + self.pixel_info["button_width"] , ts + self.pixel_info["button_len"])
      if debug:
         image_for_num = image.crop(box)
         image_for_num.show()

      if self.isButton(image, box):
         return 1

      ls = self.pixel_info["button_2_left"]
      ts = self.pixel_info["button_2_top"]
      box = (ls, ts, ls + self.pixel_info["button_width"] , ts + self.pixel_info["button_len"])
      if debug:
         image_for_num = image.crop(box)
         image_for_num.show()
      if self.isButton(image, box):
         return 2

      ls = self.pixel_info["button_3_left"]
      ts = self.pixel_info["button_3_top"]
      box = (ls, ts, ls + self.pixel_info["button_width"] , ts + self.pixel_info["button_len"])
      if debug:
         image_for_num = image.crop(box)
         image_for_num.show()
      if self.isButton(image, box):
         return 3

      ls = self.pixel_info["button_4_left"]
      ts = self.pixel_info["button_4_top"]
      box = (ls, ts, ls + self.pixel_info["button_width"] , ts + self.pixel_info["button_len"])
      if debug:
         image_for_num = image.crop(box)
         image_for_num.show()
      if self.isButton(image, box):
         return 4

      ls = self.pixel_info["button_5_left"]
      ts = self.pixel_info["button_5_top"]
      box = (ls, ts, ls + self.pixel_info["button_width"] , ts + self.pixel_info["button_len"])
      if debug:
         image_for_num = image.crop(box)
         image_for_num.show()
      if self.isButton(image, box):
         return 5

      ls = self.pixel_info["button_6_left"]
      ts = self.pixel_info["button_6_top"]
      box = (ls, ts, ls + self.pixel_info["button_width"] , ts + self.pixel_info["button_len"])
      if debug:
         image_for_num = image.crop(box)
         image_for_num.show()
      if self.isButton(image, box):
         return 6

      ls = self.pixel_info["button_7_left"]
      ts = self.pixel_info["button_7_top"]
      box = (ls, ts, ls + self.pixel_info["button_width"] , ts + self.pixel_info["button_len"])
      if debug:
         image_for_num = image.crop(box)
         image_for_num.show()
      if self.isButton(image, box):
         return 7

   '''
   # 获取自身行为
   def get_self_action(self, image, debug = False):
      ls = self.pixel_info["self_action_left_start"]
      ts = self.pixel_info["self_action_top_start"]
      box = (ls, ts, ls + self.pixel_info["action_width"] , ts + self.pixel_info["action_len"])
      image_for_num = image.crop(box)
      if debug:
         image_for_num.show()
      content = pytesseract.image_to_string(image_for_num).strip()
      content = ''.join(filter(str.isalpha, content))

      loggers.debug(content)

      if "traddle" in content:
         return "straddle"
   '''

   # 获取手牌类型(为preFlop)
   def get_self_cards_type(self, cards, colors):
      color_type = 'o' 
      if colors[0] == colors[1]:
         color_type = 's'
      return "{0}{1}{2}".format(str(cards[0]), str(cards[1]), color_type)
   
   # 获取自己的牌
   def get_self_card(self, image, debug = False):
      # 图像识别
      ls = self.pixel_info["self_left_start"]
      ts = self.pixel_info["self_top_start"]
      box = (ls, ts, ls + self.pixel_info["card_width"] * 2 , ts + self.pixel_info["card_len"])
      image_for_num = image.crop(box)
      image_for_num = self.image_to_2(image_for_num, 180) 
      if debug:
         image_for_num.show()
      content = pytesseract.image_to_string(image_for_num, config=("-c tessedit"
                  "_char_whitelist=AJKQZ123456789"
                  " --psm 10"
                  " -l osd"
                  " ")).strip()
      loggers.debug("picture result: {0}".format(content))

      # 牌型转换
      cards = self.str_to_cards(content)
      cards.sort(reverse = True)
      loggers.debug("to cards:{0}".format(cards))

      # 颜色识别
      start_loc = (self.pixel_info["self_left_start"], self.pixel_info["self_top_start"])
      colors = self.get_colors(image, len(cards), start_loc, wpk_pixel_info["card_width"], debug)
      loggers.debug("colors:{0}".format(colors))

      return cards, colors

   # 获取公共牌
   def get_public_card(self, image, debug = False): 
      ls = self.pixel_info["public_left_start"]
      ts = self.pixel_info["public_top_start"]
      box = (ls, ts, ls + self.pixel_info["card_width"] * 5 , ts + self.pixel_info["card_len"])
      image_for_num = image.crop(box).convert('L')
      if debug:
         image_for_num.show()
      content = pytesseract.image_to_string(image_for_num, config=("-c tessedit"
                  "_char_whitelist=AJKQZ123456789"
                  " --psm 10"
                  " -l osd"
                  " ")).strip()
      if debug:
         loggers.debug("public picture result: {0}".format(content))
      cards = self.str_to_cards(content)
      if len(cards) < 3:
         cards = []

      start_loc = (self.pixel_info["public_left_start"], self.pixel_info["public_top_start"])
      colors = self.get_colors(image, len(cards), start_loc, wpk_pixel_info["card_width"])
      return cards, colors

   # 获取各个选手筹码
   def get_self_blind(self, image):        
      ls = self.pixel_info["chip_left_start"]
      ts = self.pixel_info["chip_top_start"]
      box = (ls, ts, ls + self.pixel_info["chip_width"] , ts + self.pixel_info["chip_len"])
      image_for_num = image.crop(box)
      image_for_num.show()
      content = pytesseract.image_to_string(image_for_num, config=("-c tessedit"
                  "_char_whitelist=0123456789"
                  " --psm 10"
                  " -l osd"
                  " ")).strip()
      i = 0
      while i < len(content):
         if content[i] == 'I':
            content = content[0:i] + '1' + content[i+1:]
         i += 1
      bb_num = float(content) / big_blind
      print(bb_num)
      return bb_num

   # 获取底池
   def get_pot(self, image):
      ls = self.pixel_info["pot_left"]
      ts = self.pixel_info["pot_top"]
      box = (ls, ts, ls + self.pixel_info["pot_width"] , ts + self.pixel_info["pot_len"])
      image_for_num = image.crop(box)
      image_for_num.show()
      content = pytesseract.image_to_string(image_for_num).strip()
      content = "".join(filter(lambda ch: ch in '0123456789.', content))
      bb_num = float(content) / big_blind
      return bb_num
      
   # 文字转牌型
   def str_to_cards(self, content):
      char_range = ['2', '3', '4', '5','6','7', 'T','8','9','1', 'J', 'Q', '0', 'O', "D", 'K', 'A']
      cards = []
      i = 0
      while i < len(content):
         if content[i] in char_range:
            if content[i] == 'J':               
               cards.append(11)
            elif content[i] == 'Q' or content[i] == '0' or content[i] == 'O' or content[i] == 'D': #有时候Q会被识别为0, O,D
               cards.append(12)
            elif content[i] == 'K':
               cards.append(13)
            elif content[i] == 'A':
               cards.append(14)
            elif content[i] == '1':
               cards.append(10)
               i += 1
            elif content[i] == 'T':
               cards.append(7)
            else:
               cards.append(int(content[i]))
         i += 1 
      return cards

   # 获取颜色
   def get_colors(self, image, card_num, start_loc, width, debug = False):
      colors = []
      for i in range(card_num):
         total = [0, 0 ,0]
         avg = [0, 0, 0]
         count = 0
         for j in range(width):
            for k in range(20):
               pixel = image.getpixel((start_loc[0] + i * width + j, start_loc[1] + k))
               if pixel[0] > 200 or pixel[0] < 20:
                  continue
               total[0] += pixel[0]
               total[1] += pixel[1]
               total[2] += pixel[2]
               count += 1
         avg[0] = total[0] / count
         avg[1] = total[1] / count
         avg[2] = total[2] / count

         if debug:
            loggers.debug("avg:" + str(avg))
         
         # 0: 灰色 1: 红色 2: 绿色 3: 蓝色
         if abs(avg[0] - avg[1]) < 10 and abs(avg[0] - avg[2]) < 10:
            colors.append(0)
         elif avg[0] > avg[1] and avg[0] > avg[2]:
            colors.append(1)
         elif avg[1] > avg[0] and avg[1] > avg[2]:
            colors.append(2)
         elif avg[2] > avg[0] and avg[2] > avg[1]:
            colors.append(3)

      return colors

if __name__ == '__main__':
   image = Image.open('images\cur_test_1614104222.9695358.png') 
   grabTableInfo = GrabTableInfo(wpk_pixel_info)
   #grabTableInfo.get_public_card(image)
   #grabTableInfo.get_self_card(image, True)
   #grabTableInfo.get_self_blind(image)
   #grabTableInfo.get_pot(image)
   #button_loc = grabTableInfo.get_button_loc(image, True)
   #loggers.debug(button_loc)

   '''
   grabTableInfo.get_player_info(image, 1)
   grabTableInfo.get_player_info(image, 2)
   grabTableInfo.get_player_info(image, 3)
   grabTableInfo.get_player_info(image, 4)
   grabTableInfo.get_player_info(image, 5)
   grabTableInfo.get_player_info(image, 6)
   grabTableInfo.get_player_info(image, 7)
   '''

   players_left_chips = []
   for i in range(8):
      debug = False
      if i == 0:
         debug = True
      num = grabTableInfo.get_player_left_chip(image, i, debug)
      players_left_chips.append(num)

   print(players_left_chips)