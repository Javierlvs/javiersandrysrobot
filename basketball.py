#region VEXcode Generated Robot Configuration
from vex import *
import urandom

# Brain should be defined by default
brain=Brain()

# Robot configuration code
bumper_e = Bumper(brain.three_wire_port.e)
controller_1 = Controller(PRIMARY)
bumper_d = Bumper(brain.three_wire_port.d)
left_motor_a = Motor(Ports.PORT3, GearSetting.RATIO_6_1, False)
left_motor_b = Motor(Ports.PORT10, GearSetting.RATIO_6_1, False)
left_drive_smart = MotorGroup(left_motor_a, left_motor_b)
right_motor_a = Motor(Ports.PORT1, GearSetting.RATIO_6_1, True)
right_motor_b = Motor(Ports.PORT2, GearSetting.RATIO_6_1, True)
right_drive_smart = MotorGroup(right_motor_a, right_motor_b)
drivetrain = DriveTrain(left_drive_smart, right_drive_smart, 319.19, 295, 40, MM, 1)
motor_group_9_motor_a = Motor(Ports.PORT9, GearSetting.RATIO_18_1, False)
motor_group_9_motor_b = Motor(Ports.PORT8, GearSetting.RATIO_18_1, False)
motor_group_9 = MotorGroup(motor_group_9_motor_a, motor_group_9_motor_b)
motor_5 = Motor(Ports.PORT5, GearSetting.RATIO_36_1, True)


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



# define variables used for controlling motors based on controller inputs
controller_1_left_shoulder_control_motors_stopped = True
controller_1_right_shoulder_control_motors_stopped = True
drivetrain_l_needs_to_be_stopped_controller_1 = False
drivetrain_r_needs_to_be_stopped_controller_1 = False

# define a task that will handle monitoring inputs from controller_1
def rc_auto_loop_function_controller_1():
    global drivetrain_l_needs_to_be_stopped_controller_1, drivetrain_r_needs_to_be_stopped_controller_1, controller_1_left_shoulder_control_motors_stopped, controller_1_right_shoulder_control_motors_stopped, remote_control_code_enabled
    # process the controller input every 20 milliseconds
    # update the motors based on the input values
    while True:
        if remote_control_code_enabled:
            
            # calculate the drivetrain motor velocities from the controller joystick axies
            # left = axis3 + axis1
            # right = axis3 - axis1
            drivetrain_left_side_speed = controller_1.axis3.position() + controller_1.axis1.position()
            drivetrain_right_side_speed = controller_1.axis3.position() - controller_1.axis1.position()
            
            # check if the value is inside of the deadband range
            if drivetrain_left_side_speed < 5 and drivetrain_left_side_speed > -5:
                # check if the left motor has already been stopped
                if drivetrain_l_needs_to_be_stopped_controller_1:
                    # stop the left drive motor
                    left_drive_smart.stop()
                    # tell the code that the left motor has been stopped
                    drivetrain_l_needs_to_be_stopped_controller_1 = False
            else:
                # reset the toggle so that the deadband code knows to stop the left motor next
                # time the input is in the deadband range
                drivetrain_l_needs_to_be_stopped_controller_1 = True
            # check if the value is inside of the deadband range
            if drivetrain_right_side_speed < 5 and drivetrain_right_side_speed > -5:
                # check if the right motor has already been stopped
                if drivetrain_r_needs_to_be_stopped_controller_1:
                    # stop the right drive motor
                    right_drive_smart.stop()
                    # tell the code that the right motor has been stopped
                    drivetrain_r_needs_to_be_stopped_controller_1 = False
            else:
                # reset the toggle so that the deadband code knows to stop the right motor next
                # time the input is in the deadband range
                drivetrain_r_needs_to_be_stopped_controller_1 = True
            
            # only tell the left drive motor to spin if the values are not in the deadband range
            if drivetrain_l_needs_to_be_stopped_controller_1:
                left_drive_smart.set_velocity(drivetrain_left_side_speed, PERCENT)
                left_drive_smart.spin(FORWARD)
            # only tell the right drive motor to spin if the values are not in the deadband range
            if drivetrain_r_needs_to_be_stopped_controller_1:
                right_drive_smart.set_velocity(drivetrain_right_side_speed, PERCENT)
                right_drive_smart.spin(FORWARD)
            # check the buttonL1/buttonL2 status
            # to control motor_group_9
            if controller_1.buttonL1.pressing():
                motor_group_9.spin(FORWARD)
                controller_1_left_shoulder_control_motors_stopped = False
            elif controller_1.buttonL2.pressing():
                motor_group_9.spin(REVERSE)
                controller_1_left_shoulder_control_motors_stopped = False
            elif not controller_1_left_shoulder_control_motors_stopped:
                motor_group_9.stop()
                # set the toggle so that we don't constantly tell the motor to stop when
                # the buttons are released
                controller_1_left_shoulder_control_motors_stopped = True
            # check the buttonR1/buttonR2 status
            # to control motor_5
            if controller_1.buttonR1.pressing():
                motor_5.spin(FORWARD)
                controller_1_right_shoulder_control_motors_stopped = False
            elif controller_1.buttonR2.pressing():
                motor_5.spin(REVERSE)
                controller_1_right_shoulder_control_motors_stopped = False
            elif not controller_1_right_shoulder_control_motors_stopped:
                motor_5.stop()
                # set the toggle so that we don't constantly tell the motor to stop when
                # the buttons are released
                controller_1_right_shoulder_control_motors_stopped = True
        # wait before repeating the process
        wait(20, MSEC)

# define variable for remote controller enable/disable
remote_control_code_enabled = True

rc_auto_loop_thread_controller_1 = Thread(rc_auto_loop_function_controller_1)

#endregion VEXcode Generated Robot Configuration

remote_control_code_enabled = True
disable_timer = 0

def when_started1():
    global disable_timer, remote_control_code_enabled
    disable_timer = 3
    remote_control_code_enabled = True
    brain.screen.set_pen_color(Color.PURPLE)
    brain.screen.set_fill_color(Color.PURPLE)
    brain.screen.draw_rectangle(0, 0, 479, 239)

def onevent_bumper_e_pressed_0():
    global disable_timer, remote_control_code_enabled
    remote_control_code_enabled = False
    drivetrain.stop()
    brain.screen.set_fill_color(Color.RED)
    brain.screen.draw_rectangle(0, 0, 479, 239)
    wait(disable_timer, SECONDS)
    remote_control_code_enabled = True
    brain.screen.set_fill_color(Color.PURPLE)
    brain.screen.draw_rectangle(0, 0, 479, 239)
    disable_timer = disable_timer * 2

def onevent_bumper_d_pressed_0():
    global disable_timer, remote_control_code_enabled
    remote_control_code_enabled = False
    drivetrain.stop()
    brain.screen.set_fill_color(Color.RED)
    brain.screen.draw_rectangle(0, 0, 479, 239)
    wait(disable_timer, SECONDS)
    remote_control_code_enabled = True
    brain.screen.set_fill_color(Color.PURPLE)
    brain.screen.draw_rectangle(0, 0, 479, 239)
    disable_timer = disable_timer * 2

# system event handlers
bumper_e.pressed(onevent_bumper_e_pressed_0)
bumper_d.pressed(onevent_bumper_d_pressed_0)
# add 15ms delay to make sure events are registered correctly.
wait(15, MSEC)

when_started1()
