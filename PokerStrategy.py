
class PokerStrategy():
    def __init__(self):
        self.pre_flop_poker_strategy_dic = {}
        self.set_pre_flop_poker_strategy()
    
    def set_pre_flop_poker_strategy(self):

        # 在对方筹码量很少，直接allin的情况下，选择call
        call_less_chip_allin = {"Call": [["bet_num", "<=", ]]}

        # AA
        self.pre_flop_poker_strategy_dic["1414o"] = {
            "Open1": [["bet_num", "==", 1]],
            "Open2/3": [["bet_num", ">=", 2]]
        }

        # AKs | AKo
        self.pre_flop_poker_strategy_dic["1413s"] = {
            "Open1": [["bet_num", "<=", 3]]
        }
        self.pre_flop_poker_strategy_dic["1413o"] = self.pre_flop_poker_strategy_dic["1413s"]

        # AQs | AQo
        self.pre_flop_poker_strategy_dic["1412s"] = {
            "Open1": [["bet_num"], "<=", 2], ["max_bet", "<=", 6]],
            "Call": [["bet_num", "==", 2], ["max_bet", "<=", 20], ["bet_player_left_chip", "<=", 5]]
        }
        self.pre_flop_poker_strategy_dic["1412o"] = self.pre_flop_poker_strategy_dic["1412s"]

        # AJs | AJo
        self.pre_flop_poker_strategy_dic["1411s"] = {
            "Open2/3": [["bet_num", "==", 1]],
            "Call": [["bet_num", "==", 2], ["max_bet", "<=", 5]],
            "Callx": [["bet_num", "==", 2], ["max_bet", "<=", 10], ["bet_player_left_chip", "<=", 5]]
        }
        self.pre_flop_poker_strategy_dic["1411o"] = self.pre_flop_poker_strategy_dic["1411s"]

        # ATs 
        self.pre_flop_poker_strategy_dic["1410s"] = {
            "Open2/3": [["bet_num", "==", 1]],
            "Call": [["bet_num", "==", 2], ["max_bet", "<=", 5]],
            "Callx": [["bet_num", "==", 2], ["max_bet", "<=", 10], ["bet_player_left_chip", "<=", 5]]
        }

        # ATo
        self.pre_flop_poker_strategy_dic["1410o"] = {
            "Open2/3": [["bet_num", "==", 1]],
            "Callx": [  ["bet_num", "==", 2], ["max_bet", "<=", 10], ["bet_player_left_chip", "<=", 5],
                        ["will_action_num", "<=", 2]]
        }

        # Ax s
        self.pre_flop_poker_strategy_dic["149s"] = {
            "Open2/3": [["button_loc", "==", 0], ["bet_num", "==", 1]],
            "Call": [["button_loc", "==", 0], ["bet_num", "==", 2], ["max_bet", "<=", 4]],
            "Callx": [  ["bet_num", "==", 2], ["max_bet", "<=", 8], ["bet_player_left_chip", "<=", 2],
                        ["will_action_num", "==", 0]]
        }
        self.pre_flop_poker_strategy_dic["149o"] = self.pre_flop_poker_strategy_dic["149s"]
        self.pre_flop_poker_strategy_dic["148s"] = self.pre_flop_poker_strategy_dic["149s"]
        self.pre_flop_poker_strategy_dic["147s"] = self.pre_flop_poker_strategy_dic["149s"]
        self.pre_flop_poker_strategy_dic["146s"] = self.pre_flop_poker_strategy_dic["149s"]
        self.pre_flop_poker_strategy_dic["145s"] = self.pre_flop_poker_strategy_dic["149s"]
        self.pre_flop_poker_strategy_dic["144s"] = self.pre_flop_poker_strategy_dic["149s"]
        self.pre_flop_poker_strategy_dic["143s"] = self.pre_flop_poker_strategy_dic["149s"]
        self.pre_flop_poker_strategy_dic["142s"] = self.pre_flop_poker_strategy_dic["149s"]


        # KK
        self.pre_flop_poker_strategy_dic["1313o"] = {
            "Open1": [],
        }

        # KQs | KQo
        

        # QJs
        self.pre_flop_poker_strategy_dic["1211s"] = {
            "Open2/3": [["bet_num", "==", 1]],
            "Call": [["bet_num", "<=", 2], ["isBetterLoc", "==", True], ["chip_to_call", "<=", 4]],
        }
    
    def poker_op(self, card_type, strategy_param):
        for op_key, op_conditon in self.pre_flop_poker_strategy_dic[card_type].items():
            check_result = True
            for check_iter in op_conditon:
                if not self.check_one_param(strategy_param, check_iter[0], check_iter[1], check_iter[2]):
                    check_result = False          

            if check_result:
                return op_key

        return "Fold" 

    def check_one_param(self, params, key, op, value):
        if op == "==":
            return params[key] == value 
        elif op == "<=":
            return params[key] <= value 
        elif op == ">=":
            return params[key] >= value 

if __name__ == '__main__':
    pokerStrategy = PokerStrategy()
    print(pokerStrategy.pre_flop_poker_strategy_dic)

    strategy_param = {  'actioned': True, 
                        'actioned_player_num': 1, 
                        'called_num': 0, 
                        'bet_num': 4, 
                        'will_action_num': 0, 
                        'isBetterLoc': True, 
                        'chip_to_call': 3.14, 
                        'odds_to_call': 0.3459667612484799, 
                        'bet_player_left_chip': 0.0, 
                        'button_loc': 1}

    op = pokerStrategy.poker_op("1413s", strategy_param)
    print(op)