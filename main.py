import numpy as np
import time

from planestate import PlaneState
from input import Input
from plot import plot
import system


def main():
    dt = 0.01
    max_t = 30
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

    for t in ts[1:]:
        states.append(system.f(states[-1], u, dt))
        print("Time: %.1f (%.1f%%)" % (t, t / max_t * 100))
        #time.sleep(dt)

    plot(ts, states)


if __name__ == "__main__":
    main()
