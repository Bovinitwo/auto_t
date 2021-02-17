from PIL import Image
import pytesseract

wpk_pixel_info = {
   "card_width": 80,          #牌宽
   "card_len": 70,            #牌高

   "self_left_start": 285,    #自己的牌的左起始点
   "self_top_start": 1220,    #自己的牌的上起始点

   "public_left_start": 155,  #公共牌左起始
   "public_top_start": 710,   #公共牌上部分起始

   "chip_left_start": 310,    #自己的筹码标志位置
   "chip_top_start": 1138,
   "chip_width": 100,
   "chip_len": 30,

   "pot_left": 355,
   "pot_top": 530,
   "pot_width": 100,
   "pot_len": 30,
}

big_blind = 4

class GrabTableInfo:
   #获取选手信息
   def __init__(self, pixel_info):
      self.pixel_info = pixel_info 
   
   # 获取自己的牌
   def get_self_card(self, image):
      ls = self.pixel_info["self_left_start"]
      ts = self.pixel_info["self_top_start"]
      box = (ls, ts, ls + self.pixel_info["card_width"] * 2 , ts + self.pixel_info["card_len"])
      image_for_num = image.crop(box)
      image_for_num.show()
      content = pytesseract.image_to_string(image_for_num, config=("-c tessedit"
                  "_char_whitelist=AJKQZ123456789"
                  " --psm 10"
                  " -l osd"
                  " ")).strip()
      print(content)
      cards = self.str_to_cards(content)

      start_loc = (self.pixel_info["self_left_start"], self.pixel_info["self_top_start"])
      colors = self.get_colors(image, len(cards), start_loc, wpk_pixel_info["card_width"])
      print(cards) 
      print(colors)

   # 获取公共牌
   def get_public_card(self, image): 
      ls = self.pixel_info["public_left_start"]
      ts = self.pixel_info["public_top_start"]
      box = (ls, ts, ls + self.pixel_info["card_width"] * 3 , ts + self.pixel_info["card_len"])
      image_for_num = image.crop(box)
      image_for_num.show()
      content = pytesseract.image_to_string(image_for_num, config=("-c tessedit"
                  "_char_whitelist=AJKQZ123456789"
                  " --psm 10"
                  " -l osd"
                  " ")).strip()
      print(content)
      cards = self.str_to_cards(content)

      start_loc = (self.pixel_info["public_left_start"], self.pixel_info["public_top_start"])
      colors = self.get_colors(image, len(cards), start_loc, wpk_pixel_info["card_width"])
      print(cards) 
      print(colors)

   # 获取各个选手筹码
   def get_self_blind(self, image):        
      ls = self.pixel_info["chip_left_start"]
      ts = self.pixel_info["chip_top_start"]
      box = (ls, ts, ls + self.pixel_info["chip_width"] , ts + self.pixel_info["chip_len"])
      image_for_num = image.crop(box)
      image_for_num.show()
      content = pytesseract.image_to_string(image_for_num).strip()
      bb_num = float(content) / big_blind
      return bb_num

   # 获取底池
   def get_pot(self, image):
      ls = self.pixel_info["pot_left"]
      ts = self.pixel_info["pot_top"]
      box = (ls, ts, ls + self.pixel_info["pot_width"] , ts + self.pixel_info["pot_len"])
      image_for_num = image.crop(box)
      image_for_num.show()
      content = pytesseract.image_to_string(image_for_num).strip()
      bb_num = float(content) / big_blind
      print(bb_num)
      return bb_num
      
   # 文字转牌型
   def str_to_cards(self, content):
      char_range = ['2', '3', '4', '5','6','7','8','9','1', 'J', 'Q', '0','K', 'A']
      cards = []
      i = 0
      while i < len(content):
         if content[i] in char_range:
            if content[i] == 'J':               
               cards.append(11)
            elif content[i] == 'Q' or content[i] == '0': #有时候Q会被识别为0
               cards.append(12)
            elif content[i] == 'K':
               cards.append(13)
            elif content[i] == 'A':
               cards.append(14)
            elif content[i] == '1':
               cards.append(10)
               i += 1
            else:
               cards.append(int(content[i]))
         i += 1 
      return cards

   # 获取颜色
   def get_colors(self, image, card_num, start_loc, width):
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
         
         # 0: 灰色 1: 红色 2: 绿色 3: 蓝色
         if abs(avg[0] - avg[1]) < 5 and abs(avg[0] - avg[2]) < 5:
            colors.append(0)
         elif avg[0] > avg[1] and avg[0] > avg[2]:
            colors.append(1)
         elif avg[1] > avg[0] and avg[1] > avg[2]:
            colors.append(2)
         elif avg[2] > avg[0] and avg[2] > avg[1]:
            colors.append(3)

      return colors


if __name__ == '__main__':
   image = Image.open('cur_test.png') 
   grabTableInfo = GrabTableInfo(wpk_pixel_info)
   grabTableInfo.get_public_card(image)