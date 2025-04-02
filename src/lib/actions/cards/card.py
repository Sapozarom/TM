
class Card():
    id = None
    name = None
    exp = None
    bottom_text = None
    top_text = None
    picto = None
    cost = None

    # requirements [max_t, min_t, max_ox, min_ox, min_oc, max_oc, tags]
    max_temp = None
    min_temp = None
    min_oxy = None
    max_oxy = None
    min_ocean = None
    max_ocean = None
    tags = None

    # tags [b, c, s, po, pl, m, a, e, j, v, w]
    t_building = 0
    t_city = 0
    t_space = 0
    t_power = 0
    t_plant = 0
    t_microbe = 0
    t_animal = 0
    t_earth = 0
    t_jovian = 0
    t_venus = 0
    t_wild = 0

    # resources [an, m, s, fl, as, fi]
    r_animal = None
    r_microbe = None
    r_science = None
    r_floater = None
    r_asteroid = None
    r_fighter = None

    def action(self):
        print("action")

    # behaviors

    def add_resource(self, player, resource, ammount):
        pass

    def add_resource_to_card(self, player, card, ammount):
        pass
