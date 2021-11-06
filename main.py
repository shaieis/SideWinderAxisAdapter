import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame
import vgamepad
import time

WHEEL_DISCONNECTED = 1
PYGAME_QUIT = 2

# button mapping maps keys 0 to 7 of the sidewinder wheel to the virtual XBox360 buttons. all possible buttons are
# located in vgamepad

button_map = [vgamepad.XUSB_BUTTON.XUSB_GAMEPAD_A,
              vgamepad.XUSB_BUTTON.XUSB_GAMEPAD_B,
              vgamepad.XUSB_BUTTON.XUSB_GAMEPAD_X,
              vgamepad.XUSB_BUTTON.XUSB_GAMEPAD_Y,
              vgamepad.XUSB_BUTTON.XUSB_GAMEPAD_LEFT_THUMB,
              vgamepad.XUSB_BUTTON.XUSB_GAMEPAD_RIGHT_THUMB,
              vgamepad.XUSB_BUTTON.XUSB_GAMEPAD_START,
              vgamepad.XUSB_BUTTON.XUSB_GAMEPAD_BACK]


# ============================ initialization of gamepad and wheel ============================

def init_virtual_gamepad():
    return vgamepad.VX360Gamepad()


def find_sidewinder(device_index):
    pygame.joystick.init()
    joystick = pygame.joystick.Joystick(device_index)
    if "SideWinder Precision Racing Wheel" in pygame.joystick.Joystick(device_index).get_name():
        return joystick

    return None


def wait_for_sidewinder():
    while True:
        event = pygame.event.wait()
        if event.type == pygame.JOYDEVICEADDED:
            sidewinder = find_sidewinder(event.device_index)
            if sidewinder is not None:
                return sidewinder


# ============================ handle buttons and axis ============================

def handle_button(event, virtual_gp):
    # mapping sidewinder to xbox360
    button_map = [vgamepad.XUSB_BUTTON.XUSB_GAMEPAD_A,
                  vgamepad.XUSB_BUTTON.XUSB_GAMEPAD_B,
                  vgamepad.XUSB_BUTTON.XUSB_GAMEPAD_X,
                  vgamepad.XUSB_BUTTON.XUSB_GAMEPAD_Y,
                  vgamepad.XUSB_BUTTON.XUSB_GAMEPAD_LEFT_THUMB,
                  vgamepad.XUSB_BUTTON.XUSB_GAMEPAD_RIGHT_THUMB,
                  vgamepad.XUSB_BUTTON.XUSB_GAMEPAD_START,
                  vgamepad.XUSB_BUTTON.XUSB_GAMEPAD_BACK]

    button = button_map[event.button]

    if event.type == pygame.JOYBUTTONUP:
        virtual_gp.release_button(button)
    elif event.type == pygame.JOYBUTTONDOWN:
        virtual_gp.press_button(button)

    virtual_gp.update()


def handle_axis(joystick, virtual_gp):
    steering = joystick.get_axis(0)
    gas_pedal = joystick.get_axis(1)
    brake_pedal = joystick.get_axis(2)

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
        sidewinder = wait_for_sidewinder()
        print("SideWinder found!")
        ret_val = main_loop(sidewinder, virtual_gp)

    print("Quitting")


if __name__ == "__main__":
    main()




