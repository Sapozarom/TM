

class Card():
    id = 134
    name = "Extreme-Cold Fungus"
    exp = "base"
    bottom_text = "It must be -10°C or colder."
    top_text = "Action: Gain 1 plant or add 2 microbes to ANOTHER card."

    # requirements
    max_temp = -10
    min_temp = None
    min_oxy = None
    max_oxy = None
    min_ocean = None

    # tags
    Building = 0
    City = 0
