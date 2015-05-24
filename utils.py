
class FieldUtilsMixin():
    def get_friendly_cards_on_board(self):
        from cards import EmptyField
        return filter(
            lambda card: type(card)!=EmptyField,
            self.cards
        )

class colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def color(color, string):
    return color + string + colors.ENDC
