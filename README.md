Features

PORT: Configures the serial port for communication with the Arduino.
DELTA: Defines the phase variation in degrees (°) per time step
TIMESTEP: Specifies the time step duration for phase shift in milliseconds (ms)
FREQUENCY: Sets the frequency in kHz of the generated waves.
NSTEPS: Executes a sequence of phase shifts based on the DELTA and TIMESTEP values. The system performs N steps to the right, followed by N steps to the left.
RUN: Initiates automated phase control with default parameters (DELTA: 30°, TIMESTEP 60° NSTEPS 50)
STOP: Stop the movement of the phase.
EXTERNAL Activates the analog input pin to control phase variation externally.
(Connect an external analog input device to the designated pin)
JOYSTICK/KEYS Enables manual phase control using a joystick or keyboard input.

(Pressing the RIGHT or LEFT arrow keys activates manual mode.
Each key press results in a 30° phase shift in the corresponding direction.)

VIBRATION Activates vibration mode (currently under development).


Contributions are welcome! Please submit bug reports and feature requests
