import numpy as np

from planestate import PlaneState
from input import Input
from system import f
from plot import plot

def main():
    dt = 0.01
    max_t = 10
    ts = np.arange(0, max_t, dt)

    u = Input()
    u.power = 1
    u.elevon_l = 1
    u.elevon_r = 1

    states = [PlaneState()]
    states[0].x = 0
    states[0].y = 0
    states[0].speed = 0
    states[0].yaw = np.pi / 4
    states[0].roll = 0
    states[0].pitch = 0
    states[0].omega_roll = 0
    states[0].omega_pitch = 0

    for _ in ts[1:]:
        states.append(f(states[-1], u, dt))

    plot(ts, states)



if __name__ == "__main__":
    main()
