import numpy as np
import matplotlib.pyplot as plt
import matplotlib.lines
import math

import config
from planestate import PlaneState
from input import Input


def fix_angle(alpha: float) -> float:
    alpha = math.fmod(alpha, np.pi * 2)
    if alpha > np.pi:
        alpha -= np.pi * 2

    if alpha < -np.pi:
        alpha += np.pi * 2

    return alpha


def system(x: PlaneState, u: Input, dt: float) -> PlaneState:
    res = PlaneState()
    # Motor
    motor_rps = config.KV / 60 * config.V_BAT * u.power  # Motor dynamic is not modelled

    # Speed
    motor_air_speed = motor_rps * config.PROP_PITCH
    relative_motor_air_speed = motor_air_speed - x.speed
    volume_flow = relative_motor_air_speed * np.pi * config.PROP_RADIUS ** 2 * config.PROP_EFF
    mass_flow = volume_flow * config.RHO_AIR
    thrust = mass_flow * relative_motor_air_speed
    air_resistance = config.CW * config.A_FRONT * 0.5 * config.RHO_AIR * x.speed ** 2
    gravitation = config.G * config.M_PLANE * np.sin(x.pitch)
    acc_force = thrust - air_resistance - gravitation
    acc = acc_force / config.M_PLANE
    res.speed = x.speed + acc * dt

    # Position
    res.x = x.x + np.cos(x.pitch) * np.cos(x.yaw) * (x.speed * dt + acc * 0.5 * dt ** 2)
    res.y = x.y + np.cos(x.pitch) * np.sin(x.yaw) * (x.speed * dt + acc * 0.5 * dt ** 2)
    res.z = x.z + np.sin(x.pitch) * (x.speed * dt + acc * 0.5 * dt ** 2)

    # Elevons
    elevon_angle_l = u.elevon_l * config.SERVO_MAX_ANGLE
    elevon_angle_r = u.elevon_r * config.SERVO_MAX_ANGLE

    elevon_in_thrust = 0.5 * x.speed * config.ELEVON_AREA * x.speed

    elevon_l_force = elevon_in_thrust * np.abs(np.sin(elevon_angle_l))
    elevon_l_vert_force = elevon_l_force * np.sin(elevon_angle_l)
    elevon_l_horiz_force = elevon_l_force * np.sin(elevon_angle_l)

    elevon_r_force = elevon_in_thrust * np.abs(np.sin(elevon_angle_r))
    elevon_r_vert_force = elevon_r_force * np.sin(elevon_angle_r)
    elevon_r_horiz_force = elevon_r_force * np.sin(elevon_angle_r)

    print("L: %f" % elevon_l_vert_force)
    print("R: %f" % elevon_r_vert_force)

    pitch_torque = elevon_r_vert_force * config.ELEVON_DIST + elevon_l_vert_force * config.ELEVON_DIST
    roll_torque = elevon_r_vert_force * config.ELEVON_DIST - elevon_l_vert_force * config.ELEVON_DIST

    acc_pitch = pitch_torque / config.MOMENT_INERTIA_PITCH
    acc_roll = roll_torque / config.MOMENT_INERTIA_ROLL
    res.omega_pitch = acc_pitch * dt
    res.omega_roll = acc_roll * dt

    # Rotation
    res.yaw = x.yaw
    res.pitch = x.pitch + x.omega_pitch * dt + 0.5 * acc_pitch * dt**2
    res.roll = x.roll + x.omega_roll * dt + 0.5 * acc_roll * dt**2

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
    u.elevon_l = 1
    u.elevon_r = 1

    states = [PlaneState()]
    states[0].x = 0
    states[0].y = 0
    states[0].speed = 0
    states[0].yaw = np.pi/4
    states[0].roll = 0
    states[0].pitch = 0
    states[0].omega_roll = 0
    states[0].omega_pitch = 0

    for _ in ts[1:]:
        states.append(system(states[-1], u, dt))

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



if __name__ == "__main__":
    main()
