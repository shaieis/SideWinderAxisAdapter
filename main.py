import os
import vgamepad
import time

os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"  # workaround to hide pygame prompt. should stay before pygame import
import pygame

# the sctipt detects the SideWinder wheel by searching the following substring:
SIDEWINDER_NAME_SUBSTR = "SideWinder Precision Racing Wheel"

# button mapping maps keys 0 to 7 of the sidewinder wheel to the virtual XBox360 buttons. all possible buttons are
# located in vgamepad

BUTTON_MAP = [vgamepad.XUSB_BUTTON.XUSB_GAMEPAD_A,
              vgamepad.XUSB_BUTTON.XUSB_GAMEPAD_B,
              vgamepad.XUSB_BUTTON.XUSB_GAMEPAD_X,
              vgamepad.XUSB_BUTTON.XUSB_GAMEPAD_Y,
              vgamepad.XUSB_BUTTON.XUSB_GAMEPAD_LEFT_THUMB,
              vgamepad.XUSB_BUTTON.XUSB_GAMEPAD_RIGHT_THUMB,
              vgamepad.XUSB_BUTTON.XUSB_GAMEPAD_START,
              vgamepad.XUSB_BUTTON.XUSB_GAMEPAD_BACK]

# axis values:
STEERING_AXIS = 0
GAS_PEDAL_AXIS = 1
BRAKE_PEDAL_AXIS = 2

# return values
WHEEL_DISCONNECTED = 1
PYGAME_QUIT = 2
# ============================ initialization of gamepad and wheel ============================

def init_virtual_gamepad():
    return vgamepad.VX360Gamepad()


def find_sidewinder(device_index):
    pygame.joystick.init()
    joystick = pygame.joystick.Joystick(device_index)
    if SIDEWINDER_NAME_SUBSTR in joystick.get_name():
        return joystick

    return None


def wait_for_sidewinder():
    # when pygame starts running it issues a JOYDEVICEADDED event for each connected joystick
    while True:
        event = pygame.event.wait()
        if event.type == pygame.JOYDEVICEADDED:
            sidewinder = find_sidewinder(event.device_index)
            if sidewinder is not None:
                return sidewinder


# ============================ handle buttons and axis ============================

def handle_button(event, virtual_gp):
    if event.button >= len(BUTTON_MAP):
        print("Button " + event.button + " out of range")
        return

    button = BUTTON_MAP[event.button]  # mapping sidewinder to xbox360

    if event.type == pygame.JOYBUTTONUP:
        virtual_gp.release_button(button)
    elif event.type == pygame.JOYBUTTONDOWN:
        virtual_gp.press_button(button)

    virtual_gp.update()


def handle_axis(joystick, virtual_gp):
    steering = joystick.get_axis(STEERING_AXIS)
    gas_pedal = joystick.get_axis(GAS_PEDAL_AXIS)
    brake_pedal = joystick.get_axis(BRAKE_PEDAL_AXIS)

    # gas pedal axis values: not pressed (1.0) to pressed (-1.0)
    # brake pedal axis values: not pressed (1.0) to pressed (-1.0)
    y = (brake_pedal - gas_pedal) / 2

    virtual_gp.left_joystick_float(x_value_float=steering, y_value_float=y)
    virtual_gp.update()


# ============================ main and main_loop ============================

def main_loop(sidewinder, virtual_gp):
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return PYGAME_QUIT

            if hasattr(event, 'instance_id') and event.instance_id == sidewinder.get_instance_id():

                if event.type in (pygame.JOYBUTTONUP, pygame.JOYBUTTONDOWN):  # button press / release
                    handle_button(event, virtual_gp)

                elif event.type == pygame.JOYAXISMOTION:  # axis moved
                    handle_axis(sidewinder, virtual_gp)

                elif event.type == pygame.JOYDEVICEREMOVED and event.instance_id == sidewinder.get_instance_id():
                    print("SideWinder wheel disconnected")  # wheel disconnected
                    return WHEEL_DISCONNECTED

        time.sleep(0.0166)  # 60 fps


def main():
    print("Setting up a virtual XBox360 gamepad")
    virtual_gp = init_virtual_gamepad()

    pygame.init()

    ret_val = WHEEL_DISCONNECTED
    while ret_val is WHEEL_DISCONNECTED:
        print("Searching for a SideWinder wheel...")
        sidewinder = wait_for_sidewinder()  # this also detects all joysticks that are already connected when the script starts
        print("SideWinder found!")
        ret_val = main_loop(sidewinder, virtual_gp)

    print("Quitting")


if __name__ == "__main__":
    main()




