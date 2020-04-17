class PlaneState:
    def __init__(self):
        self.speed = 0
        self.x = 0
        self.y = 0
        self.z = 0
        self.yaw = 0
        self.pitch = 0
        self.omega_pitch = 0
        self.roll = 0
        self.omega_roll = 0

    def __str__(self):
        return "Pos=(%.1f, %.1f, %.1f)\t Rot=(%.1f, %.1f, %.1f)\t V=%.1f\t d/dt Rot=(%.1f, %.1f, %.1f)" \
               % (
                   self.x, self.y, self.z, self.roll, self.pitch, self.yaw, self.speed, self.omega_roll,
                   self.omega_pitch,
                   0)
