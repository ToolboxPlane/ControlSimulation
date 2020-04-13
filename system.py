import math
import numpy as np

import config
import planestate
import input


def fix_angle(alpha: float) -> float:
    alpha = math.fmod(alpha, np.pi * 2)
    if alpha > np.pi:
        alpha -= np.pi * 2

    if alpha < -np.pi:
        alpha += np.pi * 2

    return alpha


def f(x: planestate.PlaneState, u: input.Input, dt: float) -> planestate.PlaneState:
    res = planestate.PlaneState()
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
    res.pitch = x.pitch + x.omega_pitch * dt + 0.5 * acc_pitch * dt ** 2
    res.roll = x.roll + x.omega_roll * dt + 0.5 * acc_roll * dt ** 2

    res.yaw = fix_angle(res.yaw)
    res.pitch = fix_angle(res.pitch)
    res.roll = fix_angle(res.roll)

    return res
