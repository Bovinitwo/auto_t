from enum import Enum

class PreOp(Enum):
    potBet = 1 #任何情况都一个底池加注
    call3Bet = 2 #任何情况都call 3 bet
    notCall3Bet = 3 #不call 3 bet
    callOpen = 4 #call open 
    notCallOpen = 5 #不call open
    justSpecailLoc = 6 #只在庄位|小盲玩, 只call open或者 open
    samllPair = 7
    
preFlopCardTable = {
    # A挂
    "1414o": PreOp.potBet, # AA
    "1413s": PreOp.potBet, # AKs
    "1413o": PreOp.potBet, # AKo
    "1412s": PreOp.notCall3Bet, # AQs
    "1412o": PreOp.notCall3Bet, # AQo
    "1411s": PreOp.notCall3Bet, # AJs
    "1411o": PreOp.notCall3Bet, # AJo
    "1410s": PreOp.justSpecailLoc,
    "1410o": PreOp.notCallOpen, # ATs

    # k挂
    "1313o": PreOp.potBet, # KK
    "1312s": PreOp.callOpen, # KQs
    "1312o": PreOp.callOpen, # KQs
    "1311s": PreOp.callOpen, # KJs
    "1311o": PreOp.notCallOpen, # KJo

    # Q挂
    "1212o": PreOp.call3Bet, # QQ
    "1211s": PreOp.justSpecailLoc, #QJs

    # J挂
    "1111o": PreOp.callOpen, # JJ
    "1110s": PreOp.justSpecailLoc, # JTs

    # 10挂
    "1010o": PreOp.callOpen,

    # 小手对
    "99o": PreOp.samllPair,
    "88o": PreOp.samllPair,
    "77o": PreOp.samllPair,
    "66o": PreOp.samllPair,
    "55o": PreOp.samllPair,
    "44o": PreOp.samllPair,
    "33o": PreOp.samllPair,
    "22o": PreOp.samllPair

}

if __name__ == '__main__':
    cards_type = "78s"
    if cards_type not in preFlopCardTable:
        print("Flod")