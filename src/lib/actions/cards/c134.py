
from src.lib.actions.cards.card import Card


class C134(Card):
    id = 134
    name = "Extreme-Cold Fungus"
    exp = "base"
    bottom_text = "It must be -10°C or colder."
    top_text = "Action: Gain 1 plant or add 2 microbes to ANOTHER card."
    picto = "|plant| / 2 |microbe|"

    # requirements
    max_temp = -10

    t_microbe = 1

    # def __init__(self):
    #     super().__init__()
