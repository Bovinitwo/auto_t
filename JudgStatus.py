
class JudgeStatus:

    def isPreFlop(self, self_cards, public_cards):
        if len(self_cards) == 2 and len(public_cards) == 0:
            return True