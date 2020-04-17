import numpy as np

RHO_AIR = 1.2041  # Density of Air at 20°C
G = 9.81

M_PLANE = 1.117 + 0.506 + 2 * 0.192  # Mass of the plane
WIDTH = 2  # Maximal width of the plane
LENGTH = 0.9  # Maximal length of the plane
HEIGHT = 0.2  # Maximal height of the plane
CW = 0.2  # Drag coefficient (GUESSED)
A_FRONT = 157448 / 1000 ** 2  # Frontal area (pixels/(pixel/meter)^2)
A_SIDE = 63256 / 1000 ** 2  # Side area
A_TOP = 717182 / 1000 ** 2  # Top area

# M = I * a'' <=> I = M / a'' = (F * r) / a'' = (m*g*r) / a''
# Real M: M - M_mass = M - m * r^2
MOMENT_INERTIA_ROLL = (0.197 * G * 0.5) / (185 / 180 * np.pi) - (0.197 * 0.5 ** 2)
MOMENT_INERTIA_PITCH = (0.197 * G * 0.42) / (275 / 180 * np.pi) - (0.197 * 0.42 ** 2)

KV = 900  # Speed of the motor
V_BAT = 16.8  # Battery voltage
PROP_RADIUS = 10 / 2 * 0.0254  # Radius of the propeller in meter
PROP_PITCH = 4.5 * 0.0254  # Stroke of the propeller
PROP_EFF = 0.7  # Efficiency of the propeller (GUESSED)

SERVO_MAX_ANGLE = 35 * np.pi / 180  # Max deflection angle of the elevon
ELEVON_AREA = 0.43 * 0.07  # Surface area of the elevon

# Distance from elevon centre to plane centre
ELEVON_DIST_X = 0.3
ELEVON_DIST_Y = 0.6
