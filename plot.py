import matplotlib.pyplot as plt
import matplotlib.lines
import numpy as np


def plot(ts: np.ndarray, states: list):
    plt.figure()

    ax = plt.subplot(2, 2, 1)
    xs = list(map(lambda x: x.x, states))
    ys = list(map(lambda x: x.y, states))
    traj = matplotlib.lines.Line2D(xs, ys)
    ax.add_line(traj)
    ax.set_xlim(min(xs), max(xs))
    ax.set_ylim(min(ys), max(ys))
    plt.title("Position")
    plt.xlabel("x")
    plt.ylabel("y")

    plt.subplot(2, 2, 2)
    alts = list(map(lambda x: x.z, states))
    plt.plot(ts, alts)
    plt.title("Altitude")
    plt.xlabel("t")
    plt.ylabel("z")

    plt.subplot(2, 2, 3)
    speeds = list(map(lambda x: x.speed, states))
    plt.plot(ts, speeds)
    plt.title("Speed")
    plt.xlabel("t")
    plt.ylabel("v")

    plt.subplot(2, 2, 4)
    rolls = list(map(lambda x: x.roll, states))
    pitchs = list(map(lambda x: x.pitch, states))
    yaws = list(map(lambda x: x.yaw, states))
    plt.plot(ts, rolls)
    plt.plot(ts, pitchs)
    plt.plot(ts, yaws)
    plt.title("Rotation")
    plt.xlabel("t")
    plt.ylabel("angle (rad)")
    plt.legend(["Roll", "Pitch", "Yaw"])

    plt.show()
