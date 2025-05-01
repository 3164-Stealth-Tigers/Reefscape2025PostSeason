from lib.conversions import inches_to_meters

LEFT_MOTOR_ID = 9
RIGHT_MOTOR_ID = 10

INVERT_MOTORS = False

kP = 4

MAX_VELOCITY = inches_to_meters(150)
MAX_ACCELERATION = inches_to_meters(200)

SPROCKET_PITCH_DIAMETER = inches_to_meters(1.757)
GEAR_RATIO = 5.45

MINIMUM_CARRIAGE_HEIGHT = inches_to_meters(30.5)
MAXIMUM_CARRIAGE_HEIGHT = inches_to_meters(80)
OFFSET_FROM_FLOOR = inches_to_meters(30.5)

LIMITS_ENABLED = True

CARRIAGE_MASS = 9  # kg

