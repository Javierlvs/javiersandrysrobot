
from vex import *
import urandom

#region VEXcode Generated Robot Configuration

# Brain should be defined by default
brain = Brain()

# Robot configuration code
left_motor_a = Motor(Ports.PORT1, GearSetting.RATIO_18_1, False)
left_motor_b = Motor(Ports.PORT3, GearSetting.RATIO_18_1, False)
left_drive_smart = MotorGroup(left_motor_a, left_motor_b)
right_motor_a = Motor(Ports.PORT2, GearSetting.RATIO_18_1, True)
right_motor_b = Motor(Ports.PORT4, GearSetting.RATIO_18_1, True)
right_drive_smart = MotorGroup(right_motor_a, right_motor_b)
drivetrain = DriveTrain(left_drive_smart, right_drive_smart, 319.19, 295, 40, MM, 1)
motor_group_5_motor_a = Motor(Ports.PORT5, GearSetting.RATIO_36_1, False)
motor_group_5_motor_b = Motor(Ports.PORT6, GearSetting.RATIO_36_1, True)
motor_group_5 = MotorGroup(motor_group_5_motor_a, motor_group_5_motor_b)
distance_20 = Distance(Ports.PORT20)
optical_9 = Optical(Ports.PORT9)
controller_1 = Controller(PRIMARY)

# wait for rotation sensor to fully initialize
wait(30, MSEC)

# Make random actually random
def initializeRandomSeed():
    wait(100, MSEC)
    random = brain.battery.voltage(MV) + brain.battery.current(CurrentUnits.AMP) * 100 + brain.timer.system_high_res()
    urandom.seed(int(random))

initializeRandomSeed()

def play_vexcode_sound(sound_name):
    print("VEXPlaySound:" + sound_name)
    wait(5, MSEC)

wait(200, MSEC)
print("\033[2J")

# Control toggle variable
remote_control_code_enabled = True

# Controller input handling
controller_1_right_shoulder_control_motors_stopped = True
drivetrain_l_needs_to_be_stopped_controller_1 = False
drivetrain_r_needs_to_be_stopped_controller_1 = False

# define a task that will handle monitoring inputs from controller_1
def rc_auto_loop_function_controller_1():
    global drivetrain_l_needs_to_be_stopped_controller_1, drivetrain_r_needs_to_be_stopped_controller_1, controller_1_right_shoulder_control_motors_stopped, remote_control_code_enabled
    while True:
        if remote_control_code_enabled:
            left_speed = controller_1.axis3.position() + controller_1.axis1.position()
            right_speed = controller_1.axis3.position() - controller_1.axis1.position()

            if abs(left_speed) < 5:
                if drivetrain_l_needs_to_be_stopped_controller_1:
                    left_drive_smart.stop()
                    drivetrain_l_needs_to_be_stopped_controller_1 = False
            else:
                drivetrain_l_needs_to_be_stopped_controller_1 = True

            if abs(right_speed) < 5:
                if drivetrain_r_needs_to_be_stopped_controller_1:
                    right_drive_smart.stop()
                    drivetrain_r_needs_to_be_stopped_controller_1 = False
            else:
                drivetrain_r_needs_to_be_stopped_controller_1 = True

            if drivetrain_l_needs_to_be_stopped_controller_1:
                left_drive_smart.set_velocity(left_speed, PERCENT)
                left_drive_smart.spin(FORWARD)

            if drivetrain_r_needs_to_be_stopped_controller_1:
                right_drive_smart.set_velocity(right_speed, PERCENT)
                right_drive_smart.spin(FORWARD)

            if controller_1.buttonR1.pressing():
                motor_group_5.spin(FORWARD)
                controller_1_right_shoulder_control_motors_stopped = False
            elif controller_1.buttonR2.pressing():
                motor_group_5.spin(REVERSE)
                controller_1_right_shoulder_control_motors_stopped = False
            elif not controller_1_right_shoulder_control_motors_stopped:
                motor_group_5.stop()
                controller_1_right_shoulder_control_motors_stopped = True

        wait(20, MSEC)

# Start the controller input thread
rc_auto_loop_thread_controller_1 = Thread(rc_auto_loop_function_controller_1)

# Autonomous behavior
def autonomous_loop():
    while True:
        if controller_1.buttonA.pressing():
            drivetrain.stop()
            global remote_control_code_enabled
            remote_control_code_enabled = True
            while controller_1.buttonA.pressing():
                wait(10, MSEC)
            break  # Exit autonomous mode

        optical_9.set_light_power(100, PERCENT)
        optical_9.set_light(True)
        color = optical_9.color()

        if color == Color.BLUE:
            drivetrain.set_drive_velocity(50, PERCENT)
            drivetrain.turn_for(RIGHT, 180, DEGREES)
            drivetrain.drive_for(FORWARD, 10, INCHES)
            wait(500, MSEC)

        drivetrain.set_drive_velocity(30, PERCENT)
        drivetrain.turn(RIGHT)

        while True:
            if controller_1.buttonA.pressing():
                remote_control_code_enabled = True
                drivetrain.stop()
                while controller_1.buttonA.pressing():
                    wait(10, MSEC)
                return

            object_size = distance_20.object_size()
            if object_size in [ObjectSizeType.MEDIUM, ObjectSizeType.LARGE]:
                drivetrain.stop()
                drivetrain.drive_for(REVERSE, 20, INCHES)

                motor_group_5.set_velocity(50, PERCENT)
                motor_group_5.spin(REVERSE)
                wait(1.5, SECONDS)
                motor_group_5.stop()
                motor_group_5.spin(FORWARD)
                wait(1.45, SECONDS)
                motor_group_5.stop()
                break

            optical_9.set_light_power(100, PERCENT)
            optical_9.set_light(True)
            color = optical_9.color()
            if color == Color.BLUE:
                drivetrain.stop()
                drivetrain.turn_for(RIGHT, 180, DEGREES)
                drivetrain.drive_for(FORWARD, 10, INCHES)
                wait(500, MSEC)
                break

            wait(100, MSEC)

# Main loop for toggling control modes
def main_loop():
    global remote_control_code_enabled
    while True:
        if controller_1.buttonB.pressing():
            remote_control_code_enabled = False
            while controller_1.buttonB.pressing():
                wait(10, MSEC)
            autonomous_loop()

        wait(50, MSEC)

# Start the main loop
main_loop()
