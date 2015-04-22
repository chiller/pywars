from card_type import EmptyField

class FieldUtilsMixin():
    def get_friendly_cards_on_field(self):
        return filter(
            lambda card: type(card)!=EmptyField,
            self.cards
        )