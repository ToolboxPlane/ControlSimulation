import numpy as np
import matplotlib.pyplot as plt
import matplotlib.lines
import math

import config
from state import State
from input import Input


def fix_angle(alpha: float) -> float:
    alpha = math.fmod(alpha, np.pi * 2)
    if alpha > np.pi:
        alpha -= np.pi * 2
    return alpha


def system(x: State, u: Input, dt: float) -> State:
    res = State()
    # Motor
    motor_rps = config.KV / 60 * config.V_BAT * u.power  # Motor dynamic is not modelled

    # Speed
    motor_air_speed = motor_rps * config.PropAngle
    relative_motor_air_speed = motor_air_speed - x.speed
    volume_flow = relative_motor_air_speed * np.pi * config.PropRadius ** 2 * config.PropEff
    mass_flow = volume_flow * config.AirDensity
    thrust = mass_flow * motor_air_speed
    air_resistance = config.Cw * config.A * 0.5 * config.AirDensity * x.speed ** 2
    gravitation = config.G * config.PlaneMass * np.sin(x.pitch)
    acc_force = thrust - air_resistance - gravitation
    acc = acc_force / config.PlaneMass
    res.speed = x.speed + acc * dt

    # Position
    res.x = x.x + np.cos(x.pitch) * np.cos(x.yaw) * (x.speed * dt + acc * 0.5 * dt ** 2)
    res.y = x.y + np.cos(x.pitch) * np.sin(x.yaw) * (x.speed * dt + acc * 0.5 * dt ** 2)
    res.z = x.z + np.sin(x.pitch) * (x.speed * dt + acc * 0.5 * dt ** 2)

    # Rotation
    res.yaw = x.yaw + np.pi / 1000
    res.pitch = x.pitch
    res.roll = x.roll

    res.yaw = fix_angle(res.yaw)
    res.pitch = fix_angle(res.pitch)
    res.roll = fix_angle(res.roll)

    return res


def main():
    dt = 0.01
    max_t = 10
    ts = np.arange(0, max_t, dt)

    u = Input()
    u.power = 1
    u.elevon_l = 0
    u.elevon_r = 0

    states = [State()]
    states[0].x = 0
    states[0].y = 0
    states[0].speed = 0
    states[0].yaw = np.pi / 4
    states[0].roll = 0
    states[0].pitch = np.pi / 4

    for _ in ts[1:]:
        states.append(system(states[-1], u, dt))

    plt.figure()
    speeds = list(map(lambda x: x.speed, states))
    plt.plot(ts, speeds)
    plt.title("Speed")
    plt.xlabel("t")
    plt.ylabel("v")
    plt.show()

    plt.figure()
    alts = list(map(lambda x: x.z, states))
    plt.plot(ts, alts)
    plt.title("Altitude")
    plt.xlabel("t")
    plt.ylabel("z")
    plt.show()

    plt.figure()
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

    xs = list(map(lambda x: x.x, states))
    ys = list(map(lambda x: x.y, states))
    traj_fig = plt.figure()
    ax = traj_fig.add_subplot(111)
    traj = matplotlib.lines.Line2D(xs, ys)
    ax.add_line(traj)
    ax.set_xlim(min(xs), max(xs))
    ax.set_ylim(min(ys), max(ys))
    plt.title("Position")
    plt.xlabel("x")
    plt.ylabel("y")
    plt.show()


if __name__ == "__main__":
    main()
