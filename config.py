import numpy as np

KV = 900  # Speed of the motor
V_BAT = 16.8  # Battery voltage
PROP_RADIUS = 10 / 2 * 0.0254  # Radius of the propeller in meter
PROP_PITCH = 4.5 * 0.0254  # Stroke of the propeller
PROP_EFF = 0.7  # Efficiency of the propeller (GUESSED)
RHO_AIR = 1.2041  # Density of Air at 20°C
M_PLANE = 1.117 + 0.506 + 2 * 0.192  # Mass of the plane
CW = 0.2  # Drag coefficient (GUESSED)
A_FRONT = 0.0654  # Frontal area of the plane (GUESSED)
G = 9.81
SERVO_MAX_ANGLE = 35 * np.pi / 180  # Max deflection angle of the elevon
ELEVON_AREA = 0.43 * 0.07  # Surface area of the elevon
ELEVON_DIST = 0.6  # Distance from elevon centre to plane centre
WINGSPAN = 2.0
LENGTH = 0.5 # (GUESSED)
HEIGHT = 0.2 # (GUESSED)
MOMENT_INERTIA_ROLL = 1/12.0 * M_PLANE * (WINGSPAN**2 + HEIGHT**2)  # Estimated
MOMENT_INERTIA_PITCH = 1/12.0 * M_PLANE * (HEIGHT**2 + LENGTH**2)  # Estimated
