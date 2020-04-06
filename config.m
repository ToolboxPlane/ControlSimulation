DegreePerSecond = 60/0.14; % Speed of the servo
ServoChangeThreshold = 2; % Angle error (degree) of the servo to change position
KV = 900; % Speed of the motor
MotorSpoolUpTime = 0.2; % Time for the motor to reach full power (GUESSED)
PropRadius = 10/2 * 0.0254; % Radius of the propeller in meter
PropAngle = 4.5 * 0.0254; % Stroke of the propeller
PropEff = 0.7; % Efficiency of the propeller (GUESSED)
AirDensity = 1.2041; % Density of Air at 20°C
PlaneMass = 1.117 + 0.506 + 2*0.192; % Mass of the plane
Cw = 0.2; % Drag coefficient
A = 0.0654; % Frontal area of the plane
T_Roll = 0.1; % Time-constant regarding the roll axis
HeadingPerSecondPerDegree = 0.5; % Change of heading as a function of roll
WingArea = 0.3; % Wing area of the plane
Ca = 0.28; %Lift_coefficient, assuming a NACA 25112 Airfoil at 0° (see: http://airfoiltools.com/polar/details?polar=xf-naca25112-jf-200000)