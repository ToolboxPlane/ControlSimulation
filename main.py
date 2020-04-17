import numpy as np
import time

from planestate import PlaneState
from input import Input
from plot import plot
import system
import controller


def main():
    dt = 0.01
    max_t = 100
    ts = np.arange(0, max_t, dt)

    control = controller.Controller()

    states = [PlaneState()]
    states[0].x = 0
    states[0].y = 0
    states[0].speed = 0
    states[0].yaw = np.pi / 4
    states[0].roll = 0
    states[0].pitch = 0
    states[0].omega_roll = 0
    states[0].omega_pitch = 0

    last_percent = 0
    for t in ts[1:]:
        u = control.get(states[-1], t)
        new_state = system.f(states[-1], u, dt)
        states.append(new_state)
        # time.sleep(dt)

        progress = t/max_t*100
        if int(progress) > last_percent:
            print("Time: %.1f (%.d%%)\t%s" % (t, int(progress), str(new_state)))
            last_percent = int(progress)

    plot(ts, states)


if __name__ == "__main__":
    main()
