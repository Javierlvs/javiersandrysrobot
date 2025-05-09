#region VEXcode Generated Robot Configuration
from vex import *
import urandom

# Brain should be defined by default
brain=Brain()

# Robot configuration code
left_motor_a = Motor(Ports.PORT2, GearSetting.RATIO_18_1, False)
left_motor_b = Motor(Ports.PORT4, GearSetting.RATIO_18_1, False)
left_drive_smart = MotorGroup(left_motor_a, left_motor_b)
right_motor_a = Motor(Ports.PORT1, GearSetting.RATIO_18_1, True)
right_motor_b = Motor(Ports.PORT3, GearSetting.RATIO_18_1, True)
right_drive_smart = MotorGroup(right_motor_a, right_motor_b)
drivetrain = DriveTrain(left_drive_smart, right_drive_smart, 319.19, 295, 40, MM, 1)
motor_group_5_motor_a = Motor(Ports.PORT5, GearSetting.RATIO_36_1, False)
motor_group_5_motor_b = Motor(Ports.PORT6, GearSetting.RATIO_36_1, True)
motor_group_5 = MotorGroup(motor_group_5_motor_a, motor_group_5_motor_b)
distance_20 = Distance(Ports.PORT20)
line_tracker_h = Line(brain.three_wire_port.h)

# wait for rotation sensor to fully initialize
wait(30, MSEC)

# Make random actually random
def initializeRandomSeed():
    wait(100, MSEC)
    random = brain.battery.voltage(MV) + brain.battery.current(CurrentUnits.AMP) * 100 + brain.timer.system_high_res()
    urandom.seed(int(random))
      
# Set random seed 
initializeRandomSeed()

def play_vexcode_sound(sound_name):
    # Helper to make playing sounds from the V5 in VEXcode easier and
    # keeps the code cleaner by making it clear what is happening.
    print("VEXPlaySound:" + sound_name)
    wait(5, MSEC)

# add a small delay to make sure we don't print in the middle of the REPL header
wait(200, MSEC)
# clear the console to make sure we don't have the REPL in the console
print("\033[2J")

#endregion VEXcode Generated Robot Configuration

# Main autonomous logic
def when_started1():
    while True:
        # Start turning right to look for object
        drivetrain.set_drive_velocity(30, PERCENT)
        drivetrain.turn(RIGHT)

        # Object detection loop
        while True:
            # Check line tracker first
            if line_tracker_h.reflectivity() < 10:  # adjust threshold if needed
                drivetrain.stop()
                # Turn 180 degrees
                drivetrain.turn_for(RIGHT, 180, DEGREES)
                # Drive forward after turn
                drivetrain.drive_for(FORWARD, 12, INCHES)
                break  # Exit this inner loop and resume top loop

            # Check distance sensor for object
            object_size = distance_20.object_size()
            if object_size == ObjectSizeType.MEDIUM or object_size == ObjectSizeType.LARGE:
                drivetrain.stop()
                drivetrain.drive_for(FORWARD, 20, INCHES)

                # Set motor group velocity
                motor_group_5.set_velocity(50, PERCENT)

                # Spin forward for 1 second
                motor_group_5.spin(FORWARD)
                wait(1, SECONDS)
                motor_group_5.stop()

                # Then reverse for 1 second
                motor_group_5.spin(REVERSE)
                wait(1, SECONDS)
                motor_group_5.stop()

                break  # Exit inner loop to continue scanning again

            wait(100, MSEC)

# Run the program
when_started1()
