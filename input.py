class Input:
    def __init__(self):
        self.power = 0
        self.elevon_l = 0
        self.elevon_r = 0

    def __str__(self):
        return "Power=%.1f, L=%.1f, R=%.1f" % (self.power, self.elevon_l, self.elevon_r)